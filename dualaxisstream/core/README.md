# Core modules (not released)

The following core modules are not released:

- **Per-token decoding and identity enhancement** (per-token foreground/background bridge, value boosting, reference-first-frame KV anchoring, identity lock, and edge guard).
- **Identity-orthogonal motion injection**.
- **Inference acceleration** (endpoint-preserving schedule and LoRA merging).

The editing LoRA is publicly released. The public pipeline calls `dualaxisstream.core.apply_edit`; the placeholder raises `CoreNotReleasedError`.
