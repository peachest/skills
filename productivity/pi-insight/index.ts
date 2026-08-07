/**
 * pi-insight — System prompt diagnostic extension.
 *
 * Provides /insight-dump command to dump the current system prompt
 * to a known location for analysis by the pi-insight skill.
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
}
