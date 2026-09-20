/**
 * Replay template: run sampled historical queries against 2+ backend "legs".
 * Copy into your compare workspace, implement one leg function per backend,
 * then: NODE_USE_ENV_PROXY=1 npx tsx replay.mts [--limit N] [--legs a,b]
 *
 * Encoded rules (do not remove):
 * - One JSON file per (query, leg) under results/, resumable via skip-if-exists.
 * - NODE_USE_ENV_PROXY=1 is REQUIRED on corporate networks: node fetch ignores
 *   http_proxy env by default and fetch-based legs fail in <1s without it.
 * - Prefer importing the competitor's own exported code path over re-implementing it.
 * - Politeness sleep between queries; record raw payload, latency, error.
 */
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const BASE = process.cwd();
const OUT = join(BASE, "results");
mkdirSync(OUT, { recursive: true });

const args = process.argv.slice(2);
const getArg = (name: string, dflt?: string) => {
	const i = args.indexOf(name);
	return i >= 0 ? args[i + 1] : dflt;
};
const LEGS = (getArg("--legs", "legA,legB")!).split(",");
const LIMIT = Number(getArg("--limit", "999"));

interface Q { bucket: string; query: string }
const queries: Q[] = JSON.parse(readFileSync(join(BASE, "sample.json"), "utf8")).slice(0, LIMIT);
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
const safe = (s: string) => s.replace(/[^a-zA-Z0-9]+/g, "-").slice(0, 50);

// ---- legs: one function per backend. Return {ms, raw|results, error?}. ----

async function legA(query: string) {
	// e.g. incumbent CLI: execFileSync("python3", [CLI, "search", query, "--max_results", "8"], {encoding:"utf8", timeout:60_000, maxBuffer:16*1024*1024})
	throw new Error("implement legA");
}

async function legB(query: string) {
	// e.g. competitor API: fetch(..., {signal: AbortSignal.timeout(60_000)}) — remember NODE_USE_ENV_PROXY=1
	throw new Error("implement legB");
}

const LEG_FN: Record<string, (q: string) => Promise<unknown>> = { legA, legB };

// ---- runner ----

let done = 0;
for (const { bucket, query } of queries) {
	const stem = safe(query);
	for (const leg of LEGS) {
		const f = join(OUT, `${stem}__${leg}.json`);
		if (existsSync(f)) continue;
		const t0 = Date.now();
		let payload: unknown;
		try {
			payload = await LEG_FN[leg](query);
		} catch (e: any) {
			payload = { error: String(e?.message ?? e).slice(0, 500) };
		}
		writeFileSync(f, JSON.stringify({ bucket, query, leg, at: new Date().toISOString(), ms: Date.now() - t0, ...payload }, null, 1));
		done++;
		const p = payload as any;
		process.stdout.write(`[${done}] ${leg} ${query.slice(0, 60)} -> ${p?.error ? "ERR " + String(p.error).slice(0, 80) : "ok"}\n`);
	}
	await sleep(1200);
}
console.log(`replay done: ${done} new result files in ${OUT}`);
