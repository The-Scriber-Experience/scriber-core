# src/eigenscribe/frontend/__init__.py
"""
frontend

Frontend, design tokens, ANSI TrueColor gradient engine, and styling subsystems
conforming to the Eigenscribe and Scriber Labs design system.

Author: Eigenscribe & Scriber Labs
Date: November 15, 2026
"""

from __future__ import annotations

from typing import Final

from eigenscribe import __version__ as _package_version

from . import colors, gradients, the_scriber_experience
from .colors import (
    COLOR_PALETTE,
    GOLDEN_RATIO,
    PHI,
    GOLDEN_RATIO_INVERSE,
    Color,
    RGB,
    generate_golden_ratio_gradient,
    hex_to_rgb,
    interpolate_rgb,
    render_golden_ratio_gradient,
    run_smoke_test as run_colors_smoke_test,
)
from .gradients import (
    GRADIENT_PRESETS,
    compute_golden_ratio_stop_positions,
    multi_gradient,
)
from .the_scriber_experience import (
    apply_cosmic_theme,
    apply_theme,
    create_eigenscribe_colormap,
    create_plotly_base_figure,
    get_eigenscribe_rcparams,
    mermaid,
    plot_eigenscribe_heatmap,
    plots,
    register_colormaps,
)

__version__: Final[str] = _package_version

__all__: list[str] = [
    "__version__",
    # Subpackages
    "colors",
    "gradients",
    "the_scriber_experience",
    "plots",
    "mermaid",
    # Types & Core
    "RGB",
    "Color",
    "GOLDEN_RATIO",
    "PHI",
    "GOLDEN_RATIO_INVERSE",
    "hex_to_rgb",
    "interpolate_rgb",
    "generate_golden_ratio_gradient",
    "render_golden_ratio_gradient",
    "run_colors_smoke_test",
    # Palettes & Tokens
    "COLOR_PALETTE",
    # Gradients & Rendering
    "GRADIENT_PRESETS",
    "compute_golden_ratio_stop_positions",
    "multi_gradient",
    # Plots
    "apply_theme",
    "apply_cosmic_theme",
    "get_eigenscribe_rcparams",
    "create_eigenscribe_colormap",
    "register_colormaps",
    "plot_eigenscribe_heatmap",
    "create_plotly_base_figure",
]
