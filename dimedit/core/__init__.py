"""Core identity-motion decoupling modules.

The implementation of per-token decoupling and identity enhancement, identity-orthogonal
motion injection, and few-step streaming acceleration is not released.
The public pipeline calls :func:`apply_edit`; this placeholder keeps the public interface
stable.
"""

from __future__ import annotations

from typing import Any


class CoreNotReleasedError(NotImplementedError):
    """Raised when the withheld core modules are requested."""


_RELEASE_NOTE = (
    "The core identity-motion decoupling modules are not included in this "
    "release. See https://github.com/sqsiqi/DIM-Edit for updates."
)


def apply_edit(**kwargs: Any) -> Any:
    """Apply the reference-guided edit.

    This placeholder keeps the public call signature stable. The released public
    interface does not include per-token decoupling and identity enhancement,
    identity-orthogonal motion injection, or few-step streaming acceleration.
    """

    raise CoreNotReleasedError(_RELEASE_NOTE)
