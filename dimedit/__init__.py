"""DIM-Edit public package.

The core identity-motion decoupling modules are withheld in this pre-release.
See :mod:`dimedit.core` for the release note and the core hook.
"""

from .pipeline import DIMEditPipeline
from .core import CoreNotReleasedError

__all__ = ["DIMEditPipeline", "CoreNotReleasedError"]
__version__ = "0.1.0"
