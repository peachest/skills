/**
 * pi-insight — System prompt & session diagnostic extension.
 *
 * Commands:
 *   /insight-dump         — Dump current system prompt text only
 *   /insight-dump-session — Dump complete session context: system prompt,
 *                           system prompt options, all entries, and the
 *                           messages array actually sent to the LLM
 *
 * The system prompt is global (affected by global settings.json),
 * NOT recorded in session JSONL, so must be obtained via ctx.getSystemPrompt().
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { mkdirSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const INSIGHT_DIR = join(homedir(), ".pi", "agent", "insight");
const DUMP_PATH = join(INSIGHT_DIR, "system-prompt-dump.txt");
const SESSION_DUMP_PATH = join(INSIGHT_DIR, "session-dump.json");

export default function (pi: ExtensionAPI): void {
  pi.registerCommand("insight-dump", {
    description: "Dump current system prompt for pi-insight analysis",
    handler: async (_args: string, ctx) => {
      const prompt = ctx.getSystemPrompt();
      if (!prompt) {
        ctx.ui.notify("System prompt is empty.", "warning");
        return;
      }

      mkdirSync(INSIGHT_DIR, { recursive: true });
      writeFileSync(DUMP_PATH, prompt, "utf-8");

      ctx.ui.notify(
        `System prompt (${prompt.length} chars) written to ${DUMP_PATH}`,
        "info",
      );
    },
  });

  pi.registerCommand("insight-dump-session", {
    description:
      "Dump complete session context (system prompt + entries + LLM messages) as JSON",
    handler: async (_args: string, ctx) => {
      const sm = ctx.sessionManager;

      // --- Gather all the pieces ---

      const systemPrompt = ctx.getSystemPrompt() ?? "";

      // Structured inputs that build the system prompt
      let systemPromptOptions: unknown = null;
      try {
        systemPromptOptions = ctx.getSystemPromptOptions();
      } catch {
        // getSystemPromptOptions only available in command context
      }

      // Session metadata
      const header = sm.getHeader();
      const sessionId = sm.getSessionId();
      const sessionFile = sm.getSessionFile() ?? null;
      const sessionName = sm.getSessionName() ?? null;
      const cwd = sm.getCwd();
      const leafId = sm.getLeafId();

      // All raw entries (full tree, not just active branch)
      const allEntries = sm.getEntries();

      // Active branch entries with compaction applied
      const contextEntries = sm.buildContextEntries();

      // Messages array as sent to the LLM
      let llmContext: unknown = null;
      try {
        llmContext = sm.buildSessionContext();
      } catch {
        // buildSessionContext may not be available in all contexts
      }

      // Model & thinking level
      const model = ctx.model;
      const thinkingLevel = ctx.thinkingLevel;

      // --- Assemble the dump ---

      const dump = {
        _meta: {
          dumpedAt: new Date().toISOString(),
          schemaVersion: 1,
          description:
            "Complete session context dump from pi-insight. Contains system prompt, structured prompt options, raw session entries, and the messages array sent to the LLM.",
        },
        session: {
          id: sessionId,
          name: sessionName,
          cwd,
          sessionFile,
          leafId,
          header,
          model: model
            ? { provider: model.provider, id: model.id, name: model.name }
            : null,
          thinkingLevel,
        },
        systemPrompt: {
          length: systemPrompt.length,
          text: systemPrompt,
          options: systemPromptOptions,
        },
        entries: {
          total: allEntries.length,
          contextActive: contextEntries.length,
          all: allEntries,
          activeBranch: contextEntries,
        },
        llmContext,
      };

      // --- Write ---

      mkdirSync(INSIGHT_DIR, { recursive: true });
      const json = JSON.stringify(dump, null, 2);
      writeFileSync(SESSION_DUMP_PATH, json, "utf-8");

      const sizeKB = (Buffer.byteLength(json, "utf-8") / 1024).toFixed(1);
      ctx.ui.notify(
        `Session dump (${sizeKB} KB, ${allEntries.length} entries) → ${SESSION_DUMP_PATH}`,
        "info",
      );
    },
  });
}
