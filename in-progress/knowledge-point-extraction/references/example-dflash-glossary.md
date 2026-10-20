# DFlash (arXiv 2602.06036) — Block-Diffusion Drafting for Speculative Decoding

DRAFT glossary extracted from the paper's LaTeX source only (`~/papers/spec-decoding/2602.06036-dflash/source/`). Every entry carries: anchor (tex:line + quote ≤15 words), layer tag, and first-seen-in lineage **as claimed by this source**.

**Layer-tag legend** — `paper-only`: defined/used in the paper text; `code-only`: n/a this pass; `both`: reserved until the DFlash code is cross-checked (not done here); `interpretation`: the canonical spelling/contrast is the extractor's sharpening, the underlying wording is the source's.

## Language

### Inherited speculative-decoding frame

**Target model ($\mathcal{M}_t$)**:
The large autoregressive LLM whose outputs define correctness: it prefills, exposes hidden features, verifies drafts, and emits the bonus token.
_Anchor_: sections/preliminaries.tex:15 — "accelerates inference of a target model $\mathcal{M}_t$"
_Layer_: paper-only
_Lineage_: speculative decoding; source cites leviathan2023 (sections/related.tex:5)

**Draft model / drafter ($\mathcal{M}_d$)**:
The lightweight model that proposes γ future tokens per cycle; in DFlash it is a block diffusion model conditioned on target features.
_Anchor_: sections/intro.tex:5 — "a lightweight draft model to speculate a sequence of future tokens"
_Layer_: paper-only
_Lineage_: leviathan2023 per source (sections/related.tex:5)

**Verification (verify)**:
Parallel checking of the whole draft proposal by the target model in one pass.
_Anchor_: sections/intro.tex:5 — "verified in parallel by the large target model"
_Layer_: paper-only
_Lineage_: leviathan2023 per source

**Speculation budget (γ)**:
Number of draft tokens proposed per decoding cycle; drafting cost in AR grows linearly in γ.
_Anchor_: sections/preliminaries.tex:31 — "grow linearly with the speculation budget $\gamma$"
_Layer_: paper-only
_Lineage_: speculative decoding frame (τ ∈ [1, γ+1], preliminaries.tex:21). ⚠ Symbol collision: the same γ is reused as loss-decay rate (sections/method.tex:53) — see Negative space.

**Bonus token**:
The one extra token the target emits beyond accepted drafts each cycle; the next cycle's draft always conditions on it.
_Anchor_: sections/method.tex:39 — "the bonus token from the previous verification step"
_Layer_: paper-only
_Lineage_: standard speculative decoding practice; used uncited in the source

**Acceptance length (τ)**:
Expected number of accepted tokens per decoding cycle, including the bonus token; the paper's primary draft-quality metric (reported as "average acceptance length").
_Anchor_: sections/preliminaries.tex:21 — "expected number of accepted tokens per cycle, including the bonus token"
_Avoid_: acceptance rate — used loosely in abstract/intro/conclusion for the same quantity; only τ is ever defined (sharpening is the extractor's)
_Layer_: interpretation (canonical choice); the term itself is the paper's
_Lineage_: latency decomposition "Following" sadhukhan2025/MagicDec (sections/preliminaries.tex:17)

**Per-token latency (L)** and **speedup (η)**:
L = (T_draft + T_verify)/τ; η = L_target/L. Speedup improves only by raising τ or cutting T_draft — the paper's whole design space hangs on this identity.
_Anchor_: sections/preliminaries.tex:19-23 — "L = (T_draft + T_verify)/τ"; "the resulting speedup is η"
_Layer_: paper-only
_Lineage_: sadhukhan2025 (MagicDec), cited at preliminaries.tex:17

**t_step vs t_parallel**:
t_step = latency of one sequential forward pass; t_parallel = latency of generating a whole block in parallel. The efficiency claim is t_parallel ≪ γ·t_step.
_Anchor_: sections/preliminaries.tex:31,39 — "making $t_{\text{parallel}} \ll \gamma \cdot t_{\text{step}}$"
_Layer_: paper-only
_Lineage_: this paper's AR-vs-diffusion comparison (preliminaries §2.2)

**Lossless**:
The claim that speculation leaves the output exactly what the target would produce. Asserted throughout, never formally defined.
_Anchor_: sections/abstract.tex:6 — "over 6$\times$ lossless acceleration"
_Layer_: paper-only
_Lineage_: speculative decoding property, inherited uncited. See Negative space: no definition, no verification algorithm.

### DFlash drafting mechanism

**DFlash**:
The framework: a lightweight block diffusion drafter conditioned on target-model features, verified by the frozen target LLM.
_Anchor_: sections/abstract.tex:5 — "a speculative decoding framework that employs a lightweight block diffusion model"
_Layer_: paper-only
_Lineage_: this paper (macros.tex:98 coins `\method` = DFlash)

**Block diffusion model / block diffusion drafter**:
A diffusion LM that denoises a block of masked tokens simultaneously, block-by-block — blending parallelism with AR structure.
_Anchor_: sections/related.tex:11 — "denoising sequences block-by-block, blending parallelism with autoregressive structure"
_Layer_: paper-only
_Lineage_: arriola2025 (Block Diffusion), plus Fast-dLLM v2 / SDAR (related.tex:11)

**Draft block (masked block / token block)**:
The γ-sized unit predicted in parallel: one clean anchor position plus masked positions, denoised together.
_Anchor_: sections/method.tex:19 — "predicts the next token block using a block-level diffusion process"
_Avoid_: token block, masked block — the paper alternates all three spellings
_Layer_: interpretation (unified name); wording is the source's
_Lineage_: block diffusion (arriola2025) via related.tex:11

**Block size (BS; train BS / test BS)**:
Number of tokens in a draft block. May differ between training and inference with a one-way generalization: trained-large → infer-small works, not the reverse.
_Anchor_: sections/exp.tex:346 — "generalizes well to smaller inference-time block sizes… the reverse does not hold"
_Layer_: paper-only
_Lineage_: DFlash coinage in this sense (ablation sections/exp.tex:309-348)

**Parallel diffusion drafting**:
All masked positions of a block decoded in parallel in a single forward pass — the mechanism that makes T_draft ≈ t_parallel.
_Anchor_: sections/method.tex:19 — "decoded in parallel in a single forward pass"
_Layer_: paper-only
_Lineage_: DFlash coinage (mechanism name)

**Diffusion adapter**:
Role framing: the draft model as a small module that adapts the target's deep features into parallel block predictions, rather than reasoning from scratch.
_Anchor_: sections/method.tex:55 — "a lightweight diffusion adapter tightly aligned with the target"
_Layer_: paper-only
_Lineage_: DFlash coinage (metaphor; intro.tex:22 and method.tex:55)

**Denoising steps**:
Diffusion refinement iterations. DFlash's reframing claims confinement to drafting "permits aggressive reduction" of them.
_Anchor_: sections/conclusion.tex:6 — "permits aggressive reduction in denoising steps"
_Layer_: paper-only
_Lineage_: dLLM concept via nie2025/LLaDA (related.tex:11). See Negative space: the actual inference step count is never stated.

### Conditioning — the "target knows best" stack

**Target hidden features (hidden features / hidden representations / hidden states)**:
Per-layer internal states extracted from a fixed set of target layers (default: 5 layers, uniform from 2nd to 3rd-to-last), which implicitly encode future tokens.
_Anchor_: sections/exp.tex:9 — "extracted from 5 layers uniformly selected between the second layer and the third-to-last"
_Avoid_: hidden representations, context features — loose aliases in the same sections
_Layer_: paper-only
_Lineage_: feature-level context from frozen target = EAGLE series (related.tex:5); "LLM knows the future" observation cited to samragh2025 (intro.tex:22, method.tex:11)

**Target context feature**:
The fused conditioning signal: concatenated hidden features projected once via shared W_c then RMSNorm'd into the draft hidden dimension; shared by all draft layers.
_Anchor_: sections/method.tex:13 — "a compact target context feature, which is then used to condition"
_Layer_: paper-only
_Lineage_: DFlash coinage; fusion formula appendix.tex:48-54 (RMSNorm(W_c[H^(l1);…;H^(l5)]))

**KV injection (target-feature KV injection)**:
Conditioning mechanism: inject the fused target context feature into the Key and Value projections of every draft layer; stored in the draft KV cache, reused across drafting iterations; target features bypass draft Q, output projection, and FFN.
_Anchor_: sections/method.tex:17 — "directly inject it into the Key and Value projections of every draft model layer"
_Layer_: paper-only
_Lineage_: DFlash coinage; mechanism detail appendix.tex:45-71

**Input fusion**:
The rejected contrast: fuse target features with draft token embeddings at the input only (attributed to EAGLE-3); target information dilutes as draft depth grows.
_Anchor_: sections/method.tex:15 — "fuse these features with the draft model's token embeddings and feed them only as inputs"
_Layer_: paper-only
_Lineage_: EAGLE-3, per source (method.tex:15); ablated at exp.tex:352-396

**Prefill pass**:
The target's standard prompt pass that produces the first token; the inference-time moment when hidden features are extracted.
_Anchor_: sections/method.tex:13 — "the target model first performs a standard prefill pass"
_Layer_: paper-only
_Lineage_: general LLM inference vocabulary, uncited

**"The target knows best"**:
Design thesis: target hidden features implicitly contain multiple future tokens, so conditioning a small drafter beats training it from scratch.
_Anchor_: sections/intro.tex:22 — "Our key insight is simple: the target knows best"
_Layer_: paper-only
_Lineage_: slogan coined here; observation credited to samragh2025 (intro.tex:22)

### Training

**Anchor token**:
A randomly sampled clean response token that starts a training block; the remaining block positions are masked.
_Anchor_: sections/method.tex:39 — "randomly sample anchor tokens from the response, use each anchor as the first position"
_Layer_: paper-only
_Lineage_: DFlash coinage in this sense (512 anchors per sequence, appendix.tex:7)

**Mask token (m)**:
Marks the in-block positions the draft model predicts in parallel.
_Anchor_: sections/method.tex:29 — "mask tokens $m$ (green) mark positions for parallel prediction"
_Layer_: paper-only
_Lineage_: masked diffusion vocabulary (arriola2025 context)

**Invisible tokens**:
Attention-mask entries in the training layout that enforce causal consistency and prevent inter-block information leakage.
_Anchor_: sections/method.tex:29 — "Invisible tokens (white) denote the attention mask"
_Layer_: paper-only
_Lineage_: DFlash coinage (figure-3 naming)

**Sparse attention mask**:
Training attention pattern: bidirectional within a block and toward injected context features, cross-block attention disallowed — enabling many blocks per forward/backward via Flex Attention.
_Anchor_: sections/method.tex:41 — "processed jointly using a sparse attention mask"
_Layer_: paper-only
_Lineage_: implemented with Flex Attention (dong2024, cited method.tex:41)

**Anchor-sampled masked blocks** (paper heading: "Random sampling of masked blocks"):
Training block construction: sample anchors, mask the rest, predict block_size − 1 tokens — mirroring inference, where drafts always condition on the target's bonus token. Replaces standard uniform block partitioning.
_Anchor_: sections/method.tex:39 — "directly matches inference-time behavior"
_Layer_: paper-only
_Lineage_: DFlash coinage; contrast "standard block diffusion training" (method.tex:37, arriola2025); ablated appendix.tex:157-176

**Loss decay (position-dependent loss weighting)**:
Per-token weight w_k = exp(−(k−1)/γ) emphasizing early block positions, because an early error invalidates all later tokens in the block.
_Anchor_: sections/method.tex:51 — "w_k = exp(−(k−1)/γ)"
_Avoid_: suffix decay — a non-source alias; the paper says "loss decay" / "exponentially decaying weight"
_Layer_: paper-only
_Lineage_: DFlash coinage; decay-γ values appendix.tex:7 (7/5/4 for block size 16/10/8); ablated appendix.tex:145-154

**Shared embedding and LM head**:
Draft shares the target's token embedding layer and LM head, both frozen; only draft Transformer layers train.
_Anchor_: sections/method.tex:55 — "shares the token embedding layer and language modeling head with the target"
_Layer_: paper-only
_Lineage_: DFlash coinage in this form

**Online training / offline training**:
Online: target hidden features computed on the fly per training step. Offline: features precomputed and cached, then loaded.
_Anchor_: sections/appendix.tex:9 — "target hidden features are precomputed and cached"
_Layer_: paper-only
_Lineage_: DFlash coinage (implementation split)

**Training-time test**:
Attributed cost mechanism making EAGLE-3-style long-context draft training expensive; used here uncited and unexplained.
_Anchor_: sections/method.tex:44 — "challenging for methods such as EAGLE-3 due to their costly training-time test"
_Layer_: paper-only
_Lineage_: EAGLE series per source attribution (not defined in this paper)

**Target alignment**:
Constructing the training set from the target model's own responses instead of the original dataset, so drafts match the target's distribution.
_Anchor_: sections/exp.tex:7 — "responses generated by the target model for better target alignment"
_Layer_: paper-only
_Lineage_: DFlash coinage (data-strategy sense)

**Tree size / draft steps / top-k (EAGLE-3 config)**:
Baseline EAGLE-3 knobs: tree size 16 matches DFlash's block size 16 "for a fair drafting-budget comparison"; 60 is EAGLE-3's paper setting.
_Anchor_: sections/exp.tex:17 — "tree size of 16, which matches \method with block size 16"
_Layer_: paper-only
_Lineage_: EAGLE-2/3 per source (related.tex:5: "adaptive drafting trees")

## Negative space — what the source does NOT define, does NOT state, or rejects

- **"Lossless" is never defined**: asserted (abstract.tex:6, intro.tex:5, conclusion.tex:4) but no formal statement, no verification/rejection-sampling algorithm anywhere (incl. appendix). The losslessness guarantee rests entirely on inherited speculative-decoding lore.
- **Inference-time denoising step count is never stated**: method.tex:19 says masked positions decode "in a single forward pass", and conclusion.tex:6 argues the reframing "permits aggressive reduction in denoising steps" — but the actual number of denoising iterations at inference is never given.
- **Verification under non-greedy sampling is unspecified**: temp=1 results are reported (exp.tex:19-21) but the acceptance/sampling rule at temperature > 0 is never described.
- **"native MTP" baseline is undefined and uncited**: appendix.tex:79 uses it ("DFlash consistently improves over native MTP") with no definition, no reference, no config.
- **Spec-v1 / Spec-v2 scheduling overlap are used, not defined**: SGLang internals (exp.tex:133, exp.tex:251 — incl. "Spec-v2 does not support tree-based drafting for EAGLE-3"); no explanation of what they are.
- **γ is overloaded**: γ = speculation budget (preliminaries.tex:31) and γ = loss-decay rate (method.tex:53). Appendix.tex:7 resolves decay values (7/5/4 for BS 16/10/8) — decay-γ tracks block size, not the token budget; the collision is never acknowledged.
- **Adaptive block-size scheduling explicitly deferred**: "We leave adaptive block-size scheduling to future work" (exp.tex:348).
- **Explicit rejections** (argued against, with evidence): naive block-diffusion drafter without target features — 2–3× ceiling (method.tex:9, tab:naive_diffusion appendix.tex:11-39); input-fusion-only conditioning (method.tex:15, ablation exp.tex:352-396); massive ~7B dLLM drafters (intro.tex:18, related.tex:19); small AR models mimicking diffusion (PARD, intro.tex:18); TiDAR's joint training as "not yet lossless" (related.tex:15); uniform block partitioning for training (method.tex:37).
- **Comparison coverage gap admitted**: no head-to-head with other dLLM-based speculative methods "due to lack of open-source implementation" (exp.tex:11).
