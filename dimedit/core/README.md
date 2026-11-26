# Core modules (not released)

The following core modules are not released:

- **Per-token decoupling and identity enhancement**: foreground-conditioned query–key
  bridge, trigger reweighting, reference foreground KV anchoring, and conditional
  identity lock.
- **Identity-orthogonal motion injection**: projected source velocity correction with
  boundary-aware fusion (edge guard).
- **Few-step streaming acceleration**: endpoint-preserving eight-step sampling and
  pre-inference LoRA merging.

The editing LoRA is publicly released. The public pipeline calls `dimedit.core.apply_edit`; the placeholder raises `CoreNotReleasedError`.
