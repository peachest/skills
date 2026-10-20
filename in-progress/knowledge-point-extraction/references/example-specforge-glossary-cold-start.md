# SpecForge — Domain Glossary

Source: arXiv 2603.18567 (ICML 2026) — an open-source, production-oriented framework for training speculative-decoding draft models with first-class EAGLE-3 support, plus the SpecBundle draft-model release. Anchors are `sections/*.tex:LINE` in the arXiv source tarball. `Inherits` tags mark lineage the paper itself credits.

## Language

### Algorithm layer — inherited speculative-decoding vocabulary

**Speculative decoding**:
Replacing serial single-token generation with parallel verification of candidate token sequences, converting sequential generation into a batch-processing problem.
_Inherits_: Leviathan et al. 2022 (formalization); Chen et al. 2023.
_Anchor_: sections/3-background.tex:5
_Avoid_: assisted generation, speculative inference

**Target model**:
The large LLM whose forward pass verifies draft proposals and yields the final accepted tokens.
_Anchor_: sections/3-background.tex:5

**Draft model**:
The lightweight model that proposes short candidate token sequences for the target to verify; in the EAGLE-3 setting typically a one-layer Transformer at 3–5% of the target's size.
_Anchor_: sections/3-background.tex:5; sections/4-challenges.tex:3; sections/5-methods.tex:46
_Avoid_: small model, auxiliary model

**Speculation**:
A short sequence of tokens proposed by the draft model in one cycle.
_Anchor_: sections/3-background.tex:5
_Avoid_: guess, rollout

**Verification**:
Scoring all draft proposals in a single target-model forward pass, accepting or rejecting each.
_Anchor_: sections/3-background.tex:5

**Acceptance rate (α)**:
Per-token probability that a draft token matches what the target would have produced; fundamentally limited by the KL divergence between draft and target distributions.
_Anchor_: sections/3-background.tex:9,15
_Avoid_: accuracy, agreement (also: α is reused as the softmax attention weight inside the TTT algorithm — sections/3-background.tex, Algorithm 1 — context disambiguates)

**Acceptance length**:
The realized number of tokens accepted per target forward pass; the paper's headline measurement, used without formal definition.
_Inherits_: EAGLE-2 metric lineage.
_Anchor_: sections/6-experiments.tex:234,271
_Avoid_: conflating with acceptance rate (α is per-token; acceptance length is per-cycle)

**Draft cost (c)**:
Ratio of draft-model cost to target-model cost; speedup requires c ≪ 1.
_Anchor_: sections/3-background.tex:16

**Speculation length (γ)**:
Number of draft tokens proposed per cycle; there is an optimal γ for any given α and c.
_Anchor_: sections/3-background.tex:17
_Avoid_: "number of speculative steps" / "number of draft tokens" — the paper uses those as distinct inference-time knobs in the MoE table (sections/6-experiments.tex:263); reserve γ for the abstract quantity

**Tree Attention**:
Masked attention structure where each candidate token attends only to its ancestors, letting one forward pass evaluate multiple hypotheses in parallel.
_Inherits_: Medusa.
_Anchor_: sections/3-background.tex:27

**Multi-token prediction heads**:
Lightweight heads running parallel to the LM head that reuse target-model features — zero-latency but non-autoregressive drafting.
_Inherits_: Medusa.
_Anchor_: sections/3-background.tex:27

**Feature-level extrapolation**:
Drafting by autoregressively predicting future hidden-state representations in feature space, projected to token logits by a linear layer.
_Inherits_: EAGLE, under the feature-uncertainty hypothesis (hidden-state trajectories are smoother and more predictable than discrete token jumps; also credited to GliDe with WaFe).
_Anchor_: sections/3-background.tex:29

**Training-Time Testing (TTT)**:
Simulating multiple steps of autoregressive token generation during training: at each step the model attends to the training prefix plus the tokens generated in previous steps, reducing error accumulation.
_Inherits_: EAGLE-3.
_Anchor_: sections/3-background.tex:59; Algorithm 1

**TTT length**:
How many simulated autoregressive steps run inside one training forward pass; fixed at 7 in original EAGLE-3, shown here to be task-dependent (3 suffices for chat, ≈13 for math/code).
_Anchor_: sections/6-experiments.tex:271,273
_Avoid_: "number of draft tokens" (inference-time knob), unqualified "steps"

### System layer — SpecForge's own vocabulary

**Target–draft decoupling**:
Splitting the target and draft models into separate modules with distinct execution backends and parallelization strategies, instead of wrapping both in one parallelized module.
_Anchor_: sections/5-methods.tex:36–40; the rejected unified design at sections/4-challenges.tex:3
_Avoid_: unified parallelism (names the rejected design)

**Hybrid parallelism**:
The concrete pairing after decoupling: inference-engine parallelism (tensor/expert/pipeline via SGLang) for the target, FSDP/ZeRO for the draft.
_Anchor_: sections/5-methods.tex:42–48

**Prefill stage**:
Training stage one: running the target over the entire input sequence to generate hidden states — the same execution pattern as inference prefill, and the dominant bottleneck when done naïvely.
_Anchor_: sections/4-challenges.tex:9–14
_Avoid_: bare "stage 1"

**Execution backend**:
One of three interchangeable implementations for target hidden-state generation: Hugging Face, SGLang, or Custom (team-written).
_Anchor_: sections/6-experiments.tex:49–56
_Avoid_: "model runner" (that names SGLang's component, sections/5-methods.tex:48)

**Co-located / disaggregated**:
Whether the decoupled target and draft run on the same GPUs or distinct ones; all reported experiments are co-located.
_Anchor_: sections/5-methods.tex:50

**BlockMask**:
FlexAttention's data structure marking which attention blocks are skippable, partially computed, or fully computed; SpecForge builds one per TTT step from a causal-plus-suffix mask.
_Inherits_: PyTorch FlexAttention.
_Anchor_: sections/5-methods.tex:55–78,96

**Sparse Tree Attention**:
SpecForge's name for computing TTT attention via FlexAttention's streaming form instead of materializing attention logits, which accounted for 80% of activation memory.
_Anchor_: sections/5-methods.tex:88–96
_Avoid_: "optimized attention kernel" (loose phrasing used in experiments, sections/6-experiments.tex:72)

**Memory-efficient gradient computation**:
The custom Triton backward for the masked-softmax loss that overwrites the logits tensor in place with gradients (30–40% memory reduction).
_Anchor_: sections/5-methods.tex:103–105; Algorithm 3
_Avoid_: "in-place backward" unqualified

**Data regeneration**:
Re-generating a dataset's assistant responses with the target model (temperature 0.8) before training the draft; overturns EAGLE's low-data-sensitivity claim.
_Anchor_: sections/6-experiments.tex:110,234
_Inherits_: counter-claim against EAGLE (Li et al. 2024).
_Avoid_: data augmentation, distillation

**SpecBundle**:
The released suite of production-grade EAGLE-3 draft models for mainstream open-source LLMs, trained with SpecForge.
_Anchor_: main.tex:77; sections/6-experiments.tex:104
_Avoid_: "checkpoints" generically

**MoE draft variants**:
The three MoE draft architectures ablated against the dense draft — Same Params, Same FLOPS, MoE with shared experts; all three lose to dense.
_Anchor_: sections/6-experiments.tex:282–294
