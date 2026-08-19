# Chunking Strategy Comparison

Consulted when tuning `STRATEGY` or understanding boundary quality.

Test audio: 88-minute vLLM tech talk, 1127 silence segments.

| Strategy | Max deviation | Avg silence at cut | Min silence at cut |
|----------|-------------|-------------------|-------------------|
| dp | 52.9s | 2.56s | 1.08s |
| greedy | 111.2s | 1.15s | 0.50s |
| weighted | 54.7s | 2.89s | 1.53s |
| threshold | 203.4s | 2.93s | 1.51s |

DP cost function: `α × |chunk_dur - target|/target + β × 1/(1+silence_dur)`

- **dp** — globally optimal partition. Most uniform chunks. Default.
- **greedy** — nearest-silence per target. Fast, local optimum.
- **weighted** — scores by distance + silence duration. Picks longer pauses.
- **threshold** — filters silences < `MIN_SILENCE_SCORE` seconds, then greedy. For very chatty speakers.
