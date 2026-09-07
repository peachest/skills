# Trace Signals

The waste and friction signals a diagnosis hunts in a trace, with the cost
arithmetic each demands. Entry indices (`[31]`, `[37]`) come from the trace
index; the session-JSONL format primer (usage fields, entry structure) lives
in the `skill-call-extract` skill's `references/session-jsonl.md` — read it
first if the trace format is unfamiliar.

## Waste signals

1. **Re-emission** — the same large payload written into tool-call arguments
   across multiple turns (e.g. a full claim set, file content, plan). Detect:
   repeated `CALL ... argLen=<large>` entries with near-identical sizes, or the
   same distinct tokens (IDs, keys) recurring in args. Cost = sum of the
   duplicate rounds' `output` tokens.
2. **Prefix-cache collapse** — `cacheR` on an assistant message drops sharply
   vs the previous one (e.g. 60K → 27K) while `in=` spikes: the whole context
   was re-read uncached. Big `in=` with low `cacheR` on adjacent turns marks
   the re-read; the entry that grew the context usually sits just before it.
3. **Tool failure loops** — same tool called repeatedly with similar args;
   results containing error/exception text. Count rounds until first success.
4. **Verbose error echo** — one tool result re-stating the same error per item
   (e.g. 30 identical validation failures). Cost = result bytes re-read every
   subsequent turn.
5. **Wall-clock stalls** — large gaps between adjacent entry timestamps with
   no tool call in between (model thinking / retry) or one tool call taking
   minutes.

## Reporting rules

- **Name the arithmetic.** "Turns [31] and [37] each emitted the 30-claim
  set; output 3668 + 2347 tokens, the second round was pure waste" is a
  finding; "a lot of tokens were wasted" is not.
- **Attribute cause where visible**: skill design (verbose error output,
  missing assembly tool) vs harness/environment (network, model provider,
  quota). The route depends on the attribution — only skill-design causes
  route to skill changes.
