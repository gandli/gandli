# rl-paint-with-code

> Train a language model with reinforcement learning (GRPO) to write p5.brush JavaScript sketches that render watercolour paintings. The code *is* the artefact — editable, composable, reproducible.

**Status:** 💭 Abandoned — hardware/budget constraints
**Reference:** [Surya Narreddi — Training AI to Paint with Code](https://surya.website/rling-qwen-to-paint-with-code)

## The itch

Image generation today is a black box: prompt → image. You can't edit the canvas, only re-prompt. What if the model wrote code instead of pixels? The code is the artefact, the code is editable, and you can change what the model produced without going back to the prompt.

## What the reference project did

| Component | Detail |
|---|---|
| Base model | Qwen2.5 (7B) fine-tuned with GRPO |
| Renderer | p5.brush (watercolour brush library) in Puppeteer sandbox → PNG |
| Judge | Pairwise comparison: rollout vs 2 reference pool images, judge model picks better watercolour |
| Reward | 4-component: compile gate (0.05) + length check (0.05) + HPSv3 (0.30) + pairwise judge (0.60) |
| Reference pool | 1,664 hand-rated images → 117 love-tier → 581 in active pool |
| System prompt | 8-method allowlist, zero API docs — evolved via GEPA (200 iterations) |
| Training cost | Thousands of rollouts × GPU compute + VLM judge API calls |

## Why this was abandoned

| Requirement | What we have | Gap |
|---|---|---|
| GPU for GRPO training | Mac M1 / Mac mini (no CUDA) | ❌ No viable training hardware |
| Budget ($thousands) | $0 | ❌ Cloud GPUs + API judge calls not free |
| Reference pool (~1,000 rated images) | 0 | ❌ Hours of manual rating needed |
| p5.brush sandbox (Puppeteer + headless Chrome) | ✅ Possible locally | OK |
| Pairwise judge model (VLM) | 9Router API available | ✅ Available but cost accumulates |

The core bottleneck is hardware: GRPO training requires a GPU with meaningful VRAM (8+ GPU-hours minimum even for a 7B model). Without at least a rented A100/4090, the training loop can't run at all. The reference pool and judge model are secondary blockers that become solvable once compute is solved.

## What was learned

- **Pairwise scoring beats absolute scoring** — relative judgment ("which is better?") opens dynamic range vs 0-10 scale
- **Short opinionated allowlist > long API docs** — 400-line p5.brush reference caused API hallucination; 8-method allowlist fixed it
- **Correlated rewards plateau the model** — 9 signals with 0.85-0.95 correlation collapsed to 4; reward climbed 3× faster
- **Code length saturates quickly** — binary length gate (0.05) is enough; continuous ramp produced zero gradient after step 30

## Future path

If a GPU (rented or otherwise) becomes available, this project is viable at ~$500-1,000 budget for a first training run. The reference pool can be seeded from existing model outputs (no need for human-made watercolour paintings — the original project generated all 1,664 pool images from frontier models). The key non-negotiable is the GPU — everything else follows.

## References

- [Surya Narreddi — Training AI to Paint with Code](https://surya.website/rling-qwen-to-paint-with-code)
- [p5.brush library](https://github.com/antiboredom/p5.brush)
- [GRPO paper](https://arxiv.org/abs/2402.03300)
- [HPSv3 (Human Preference Score v3)](https://github.com/tgxs002/HPSv3)