/**
 * pi-herdr-peer — thin pi-extension shell over the multi-agent-collab peer scripts.
 *
 * Registers herdr_send / herdr_resolve / herdr_peer as LLM tools. Auto-fills the
 * sender identity (pane from $HERDR_PANE_ID, runtime from $HERDR_SESSION) so the
 * model only composes content. All logic lives in the python scripts — this file
 * is an adapter only (single source of truth, no drift).
 *
 * Scripts: ~/.pi/agent/skills/multi-agent-collab/scripts/ (override: HERDR_PEER_SCRIPTS)
 * Protocol: /skill:multi-agent-collab (five-part prompt; followUp default; steer opt-in)
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";
import { StringEnum } from "@earendil-works/pi-ai";
import { existsSync, mkdtempSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, basename } from "node:path";
import { fileURLToPath } from "node:url";

// Script-engine resolution order (pitfall-proof: no absolute HOME paths):
//   1. HERDR_PEER_SCRIPTS env — dev override
//   2. package-bundled skills/ (if this repo is ever installed with skills in the pi manifest)
//   3. npx chain install targets: ~/.pi/agent/skills/<name>/ and ~/.agents/skills/<name>/
// Docs: package.json (this repo) explains why skills are NOT in the pi manifest.
function resolveScripts(): string {
	const skillScripts = "multi-agent-collab/scripts";
	const candidates = [
		process.env.HERDR_PEER_SCRIPTS,
		join(dirname(dirname(fileURLToPath(import.meta.url))), "skills", "in-progress", "multi-agent-collab", "scripts"),
		join(process.env.HOME || "", ".pi", "agent", "skills", "multi-agent-collab", "scripts"),
		join(process.env.HOME || "", ".agents", "skills", "multi-agent-collab", "scripts"),
	].filter(Boolean) as string[];
	for (const dir of candidates) {
		if (existsSync(join(dir, "herdr-send.py"))) return dir;
	}
	throw new Error(
		`peer scripts not found (searched: ${candidates.join(", ")}). ` +
		`Install: npx skills add -g . -s multi-agent-collab -a pi -y (from this repo), or set HERDR_PEER_SCRIPTS.`
	);
}

const SCRIPTS = resolveScripts();

const UUID_RE = /([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/;

export default function (pi: ExtensionAPI) {
	function senderIdentity(ctx: any): string | null {
		const pane = process.env.HERDR_PANE_ID;
		if (!pane) return null; // orca / non-herdr terminal: caller adds identity in message
		const file: string | undefined = ctx.sessionManager?.getSessionFile?.();
		const uuid = file?.match(UUID_RE)?.[1];
		const name = (ctx.sessionManager?.getSessionName?.() as string | undefined)
			|| basename(ctx.cwd || process.cwd());
		const id = uuid ? `${name} ${uuid.slice(0, 8)}` : name;
		return `${id} (${pane})`;
	}

	function parseEnvelope(raw: string, script: string): any {
		try {
			const d = JSON.parse(raw);
			if (d && typeof d === "object" && "error" in d) {
				throw new Error(`${script}: ${JSON.stringify(d.error)}`);
			}
			return d;
		} catch (ex: any) {
			if (ex instanceof SyntaxError) {
				throw new Error(`${script} returned non-JSON: ${raw.slice(0, 300)}`);
			}
			throw ex;
		}
	}

	pi.registerTool({
		name: "herdr_send",
		label: "herdr send",
		description:
			"Deliver a prompt to a peer herdr agent pane. FollowUp by default: waits for the peer to reach idle/done (bounded, 30min, then fails without sending) and delivers as a clean new task; pass steer=true to deliver immediately mid-task (corrections/blockers only). Message MUST follow the five-part shape: [caller identity] (auto-prepended via --from) / [context] / [tasks] / [output + reply]. Receipt (agent_status/revision) is returned on delivery.",
		promptSnippet: "Send a protocol-shaped prompt to a peer herdr agent (followUp default, steer opt-in)",
		promptGuidelines: [
			"Use herdr_send for peer dispatches and receipts instead of hand-rolled `herdr agent prompt` — it enforces quoting, error-first envelopes, and the caller-identity section.",
			"herdr_send runs in followUp mode by default; pass steer=true only for corrections/blockers/answers the peer must see mid-task.",
		],
		parameters: Type.Object({
			to: Type.String({ description: "Target pane id, e.g. w3:p2 (runtime-qualified targets: use runtime param)" }),
			message: Type.String({ description: "Message body, five-part shape. [caller identity] is auto-prepended — do not write it yourself." }),
			steer: Type.Optional(Type.Boolean({ description: "true = deliver immediately mid-task (steer). Default false = followUp (wait for idle/done, up to 30min)." })),
			runtime: Type.Optional(Type.String({ description: "herdr session name when the peer lives in another runtime (default/dev/agent...). Omit for current runtime." })),
			wait_ms: Type.Optional(Type.Number({ description: "After sending, wait up to this many ms for the peer's settle state and return it." })),
		}),
		async execute(_toolCallId, params, signal, _onUpdate, ctx) {
			const pane = process.env.HERDR_PANE_ID;
			const from = senderIdentity(ctx);
			if (!from) {
				throw new Error(
					"No $HERDR_PANE_ID in this environment (orca or plain shell?). " +
					"herdr_send targets herdr runtimes; for orca peers see the orca-routing reference."
				);
			}
			const dir = mkdtempSync(join(tmpdir(), "herdr-send-"));
			const msgFile = join(dir, "message.md");
			writeFileSync(msgFile, params.message, "utf-8");

			const args = [join(SCRIPTS, "herdr-send.py"), params.to, msgFile, "--from", from];
			if (params.steer) args.push("--steer");
			if (params.runtime) args.push("--runtime", params.runtime);
			if (params.wait_ms != null) args.push("--wait", String(params.wait_ms));

			// followup gate may block up to 30min + settle wait
			const timeout = (params.wait_ms ?? 0) + 31 * 60 * 1000;
			const res = await pi.exec("python3", args, { timeout, signal });
			const receipt = parseEnvelope(res.stdout.trim() || res.stderr.trim(), "herdr-send");
			return {
				content: [{ type: "text", text: JSON.stringify(receipt, null, 2) }],
				details: receipt,
			};
		},
	});

	pi.registerTool({
		name: "herdr_resolve",
		label: "herdr resolve",
		description:
			"Resolve a peer's herdr address from any fragment: session UUID (full or 8+ char prefix), session jsonl path, pane id, cwd fragment, or terminal-title fragment. Scans ALL running herdr runtimes by default and tags each match with its runtime — pane ids are runtime-local, so qualify before dispatching. Use this whenever you only know a session id and need the pane to send to.",
		promptSnippet: "Find a peer herdr pane from a session UUID / name / cwd fragment",
		promptGuidelines: [
			"Use herdr_resolve to turn a session id or repo name into a pane address before calling herdr_send; matches carry the runtime field — pass it as herdr_send's runtime param when it differs from yours.",
		],
		parameters: Type.Object({
			query: Type.String({ description: "Session UUID (8+ chars ok), pane id, cwd fragment, or title fragment" }),
			runtime: Type.Optional(Type.String({ description: "Narrow to one herdr session name (default/dev/agent...). Default: all running runtimes." })),
		}),
		async execute(_toolCallId, params, signal) {
			const args = [join(SCRIPTS, "herdr-resolve.py"), params.query];
			if (params.runtime) args.push("--runtime", params.runtime);
			const res = await pi.exec("python3", args, { timeout: 60_000, signal });
			const raw = res.stdout.trim() || res.stderr.trim();
			const parsed = parseEnvelope(raw, "herdr-resolve");
			if (parsed.count === 0) {
				throw new Error(
					`No peer matches "${params.query}" in ${(parsed.runtimes_queried || []).join(", ")}` +
					(parsed.errors ? `; errors: ${JSON.stringify(parsed.errors)}` : "")
				);
			}
			return {
				content: [{ type: "text", text: JSON.stringify(parsed, null, 2) }],
				details: parsed,
			};
		},
	});

	pi.registerTool({
		name: "herdr_peer",
		label: "herdr peer",
		description:
			"Bootstrap a new named peer agent in one step: splits a pane beside the current one (geometry-aware), starts a pi agent in it, and returns its pane id. Name must match [a-z][a-z0-9_-]{0,31}. Dispatch the five-part bootstrap prompt to the returned pane with herdr_send.",
		promptSnippet: "Create a new peer pi agent pane and return its address",
		promptGuidelines: [
			"Use herdr_peer to spawn a peer, then herdr_send to dispatch its bootstrap prompt — never pane split + agent start by hand.",
		],
		parameters: Type.Object({
			name: Type.String({ description: "Peer agent name, [a-z][a-z0-9_-]{0,31}" }),
			cwd: Type.String({ description: "Working directory for the peer (absolute path)" }),
			direction: Type.Optional(StringEnum(["right", "down"] as const, { description: "Split direction; default right (wide caller pane) / down for tall" })),
		}),
		async execute(_toolCallId, params, signal) {
			const args = [join(SCRIPTS, "herdr-peer.sh"), params.name, params.cwd];
			if (params.direction) args.push(params.direction);
			const res = await pi.exec("bash", args, { timeout: 120_000, signal });
			const peer = parseEnvelope(res.stdout.trim() || res.stderr.trim(), "herdr-peer");
			return {
				content: [{ type: "text", text: JSON.stringify(peer, null, 2) }],
				details: peer,
			};
		},
	});
}
