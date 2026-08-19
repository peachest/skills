# LLM Cleanup for ASR Transcripts

Prompt template and pre-marking workflow for Step 3. Reached when the agent
is about to clean a raw ASR transcript.

## Pre-marking low-confidence segments

The verbose_json output includes `avg_logprob` per segment. Before sending
to the LLM, mark segments with `avg_logprob < -1.0` as `[音频不清]` so the
LLM preserves them rather than guessing.

The transcribe console already lists these segments with absolute
timestamps. The per-chunk JSON in `chunks/transcripts/chunk_XXX.json`
contains the full segment metadata for programmatic pre-marking.

## Prompt template

```
你是中文技术演讲转录校对助手。
主题：{title}
已知术语：{glossary_terms}

规则：
1. 修正同音字错误（如 VM→vLLM, Eboot→Prefill）
2. 添加标点符号
3. 按语义分段
4. 不要改变原意
5. 不要添加信息
6. 不要删除内容

原始文本：
{raw_text}
```

For long transcripts (>4000 chars), split and process sequentially.
