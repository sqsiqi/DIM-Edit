# Method

DIM-Edit edits a source video according to a reference image and a text prompt. The
source video supplies the scene, the camera path, and the motion; the reference supplies
the target object's appearance. The edited foreground must follow the reference, while
the background and the source motion stay unchanged.

The method is built on a few-step streaming video generator. A source branch and a noisy
target branch are processed in parallel with shared transformer weights, and the edit is
controlled at the token level rather than by a single global blend rate.

## Why a global blend is not enough

For a self-attention layer, let `K_src` and `K_trg` be the source and target keys. A
streaming editor with a global schedule blends them as

```text
K_hat_trg = beta(t) * K_trg + (1 - beta(t)) * K_src,
```

where `beta(t)` is shared by every spatial token. The foreground edit energy and the
background deviation energy are

```text
E_F = sum_{i in F} ||K_hat_trg_i - K_src_i||^2,
E_B = sum_{i in B} ||K_hat_trg_i - K_src_i||^2.
```

Because `K_hat_trg_i - K_src_i = beta(t) * (K_trg_i - K_src_i)`, the ratio

```text
E_B / E_F = sum_{i in B} Delta_i / sum_{i in F} Delta_i
```

is independent of `beta(t)`. A stronger edit therefore multiplies the foreground change
and the background perturbation by the same factor. The two cannot be controlled
independently with a scalar schedule.

## Per-token decoupling and identity enhancement

The global schedule is replaced by a per-token rate. A foreground indicator is derived
from the trigger phrase's cross-attention response, propagated over the stream, and
merged with the target foreground mask. The foreground-conditioned query–key bridge
assigns a higher target contribution to foreground tokens, while background tokens keep
the native rate and stay source-anchored. The background is preserved structurally by the
source branch; no explicit background anchor is needed.

### Foreground identity enhancement

Three complementary operations strengthen the edited identity:

1. **Trigger reweighting** amplifies the target prompt's cross-attention response on
   foreground rows and trigger columns, then renormalizes those rows before value
   aggregation. It increases the relative contribution of foreground text features and
   does not directly rescale the value tensor.
2. **Reference foreground KV anchoring** appends the reference foreground keys and values
   to the target attention context, repeated `nrep` times. Only foreground keys and values
   are retained, so the reference background never becomes an identity source.
3. **Conditional identity lock** raises the foreground target contribution in later
   streaming chunks when the edited foreground is compact, preventing source keys from
   pulling the identity back. The gate follows streaming progress, not denoising progress.

## Identity-orthogonal motion injection

A strong edit can overwrite the temporal correspondence carried by the source keys, so
the foreground may freeze or move incorrectly. The source velocity correction contains an
appearance component and a motion component. Let `Delta v = v_gt - v_src` be the source
correction and `e_hat = v_trg - v_src` the edit direction. The method removes the
edit-direction component from the low-pass-filtered correction:

```text
v_mot = LP(Delta v) - (<LP(Delta v), e_hat> / (||e_hat||^2 + eps)) * e_hat.
```

The residual is approximately orthogonal to the instantaneous edit direction (exactly
orthogonal without regularization for nonzero directions). It is injected into the
foreground velocity with a cosine ramp, so the source dynamics are restored without
pulling the appearance back toward the source. The background receives the raw source
correction.

### Boundary support for velocity fusion

The edge guard dilates the reference foreground support and takes its union with the
dynamic foreground mask, closing tokenization gaps at the object boundary. It activates
when denoising progress and foreground area meet their thresholds. Unlike the identity
lock, it controls velocity-fusion support rather than the attention blend rate.

## Few-step streaming acceleration

The method uses endpoint-preserving sampling: a small number of model evaluations are
placed between the initial noise level and a retained low-noise terminal timestep, so the
terminal model evaluation is kept as the step count decreases. In the paper, eight steps
with terminal timestep 66 replace fifteen steps to zero.

The editing LoRA is merged into the base weights before inference, which removes the
per-layer adapter overhead and reduces peak memory. No optimization is performed per
video.

## Differences from streaming baselines

Streaming editors such as StreamEdit apply one global blending schedule to every token
and handle the background implicitly. DIM-Edit separates the two regions and the two
factors: the per-token bridge decides where the reference identity acts, the identity
enhancement modules make the edit stable, and the orthogonal motion field decides what
part of the source correction acts. The background is preserved structurally, and the
method requires no per-video optimization.
