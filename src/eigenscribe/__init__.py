# src/eigenscribe/__init__.py
"""
eigenscribe

Single top-level import namespace for the Scriber Labs & Eigenscribe workspace
baseline. The design-token / gradient frontend and the CLI suite are bundled as
subpackages (``eigenscribe.frontend`` and ``eigenscribe.cli``) under one package
root, so the distribution no longer installs generic top-level ``frontend`` /
``cli`` packages that could collide with other projects.

Author: Eigenscribe & Scriber Labs
Date: November 20, 2026
"""

from __future__ import annotations

from typing import Final

__version__: Final[str] = "2.0.1"

from . import frontend
from . import cli

__all__: list[str] = [
    "__version__",
    "frontend",
    "cli",
]
