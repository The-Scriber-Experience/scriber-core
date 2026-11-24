# src/eigenscribe/frontend/colors.py
"""
colors.py

Centralized color definitions, eigenscribe palettes, design tokens, and golden ratio
gradient interpolation engine for CLI formatting, Matplotlib plotting, mermaid diagrams,
and UI styling.

Author: Eigenscribe
Date: November 14, 2026
Last Updated: November 18, 2026
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from typing import Final, TypeAlias

import math

__all__: list[str] = [
    "RGB",
    "Color",
    "COLOR_PALETTE",
    "GOLDEN_RATIO",
    "PHI",
    "GOLDEN_RATIO_INVERSE",
    "hex_to_rgb",
    "interpolate_rgb",
    "generate_golden_ratio_gradient",
    "render_golden_ratio_gradient",
    "run_smoke_test",
]

# -----------------------------------------------------------------------------------------------------------
# 0️⃣ / 🎭 Definitions, Constants & Types
# -----------------------------------------------------------------------------------------------------------

RGB: TypeAlias = tuple[int, int, int]
Color: TypeAlias = str | RGB

# ➗ Golden Ratio Constants (phi = (1 + sqrt(5)) / 2)
GOLDEN_RATIO: Final[float] = (1.0 + 5.0**0.5) / 2.0  # ≈ 1.618033988749895
PHI: Final[float] = GOLDEN_RATIO
GOLDEN_RATIO_INVERSE: Final[float] = GOLDEN_RATIO - 1.0  # 1/φ ≈ 0.618033988749895

# -----------------------------------------------------------------------------------------------------------
# 🎨 Canonical Color Palette
# COLOR_PALETTE is the sole source of authored hex colors for the package.
# -----------------------------------------------------------------------------------------------------------

# Values are unique: roles and visual families are represented by token names at
# their call sites instead of maintaining parallel color dictionaries.
COLOR_PALETTE: Final[dict[str, str]] = {
    "junie_lime": "#a7c957",
    "aurora_green": "#84cc16",
    "bright_chartreuse": "#70e000",
    "slime_green": "#31ff48",
    "neon_green": "#30ff40",
    "bright_green": "#28d728",
    "node-9": "#00c853",
    "deep_green": "#038b00",
    "green_dark": "#035100",
    "deep_pine": "#071a12",
    "forest_teal": "#064e38",
    "pine": "#059669",
    "success_emerald": "#10b981",
    "ibm_green": "#309592",
    "tropical_teal": "#03e8bd",
    "cyan_green": "#00f5d4",
    "green_pond": "#1ed966",
    "green_jade": "#00ff7f",
    "green_light": "#57ffbc",
    "pale_mint": "#b4ffcf",
    "electric_lagoon": "#1ef6eb",
    "electric_cyan": "#00ffee",
    "node-1": "#00ffff",
    "bright_cyan": "#00f0ff",
    "node-2": "#00e8ff",
    "reef_cyan": "#1ed9f6",
    "sleeping_beauty": "#06b6d4",
    "ibm_cyan": "#2ca9e6",
    "azure_splash": "#1eb2f6",
    "node-3": "#14b5ff",
    "sky_info": "#38bdf8",
    "sky_cyan": "#4cc9f0",
    "ice_blue": "#b8f6ff",
    "midnight_navy": "#06152b",
    "deep_ocean_blue": "#003b73",
    "node-4": "#0070eb",
    "eigen_blue": "#008eff",
    "cerulean_surge": "#1e8af6",
    "skyline_blue": "#0a95eb",
    "electric_blue": "#00a6ff",
    "sky_blue": "#3a98ff",
    "cornflower": "#1e7bf6",
    "azure_sky": "#1e6ff6",
    "royal_blue": "#1e62f6",
    "strong_blue": "#0355e8",
    "twilight_indigo": "#1e3bf6",
    "dusk_violet_blue": "#291ef6",
    "midnight_indigo": "#1e22f6",
    "ibm_indigo": "#4361ee",
    "periwinkle_blue": "#5280ff",
    "midwest_indigo": "#6f78fa",
    "deep_indigo": "#3a0ca3",
    "deep_plum": "#120a24",
    "dark_violet": "#3b176e",
    "deep_iris": "#3b1ef6",
    "cosmic_violet": "#4b1ef6",
    "cosmic_iris": "#501ef6",
    "node-7": "#5e17eb",
    "deep_purple": "#7c5cff",
    "node-6": "#7952f5",
    "nebula_purple": "#781ef6",
    "bright_violet": "#7c3aed",
    "amethyst": "#7c1ef6",
    "ibm_purple": "#844ccc",
    "royal_purple": "#7209b7",
    "bright_purple": "#a855f7",
    "neon_orchid": "#a01ef6",
    "studio_purple": "#9c1ef6",
    "vivid_orchid": "#bc1ef6",
    "pale_lilac": "#d8b4fe",
    "black_cherry": "#210817",
    "dark_berry": "#7c174f",
    "deep_rose": "#ad1457",
    "vivid_pink": "#f72585",
    "ibm_pink": "#fe28a2",
    "bright_pink": "#ff40a1",
    "node-8": "#ff66b3",
    "soft_rose": "#ff76a1",
    "pale_orchid_pink": "#ffb4f6",
    "heliotrope": "#dd1ef6",
    "neon_magenta": "#f61eef",
    "bright_magenta": "#ff00c3",
    "hot_pink": "#ff007b",
    "error_crimson": "#d7263d",
    "dusty_peach": "#e7a697",
    "soft_coral": "#f77f64",
    "orange_soft": "#f78166",
    "peach_coral": "#f79764",
    "tangerine": "#ff8855",
    "coral_orange": "#ff783d",
    "apricot": "#ff9d57",
    "golden_amber": "#feb639",
    "warning_amber": "#f7c548",
    "node-5": "#ffd94a",
    "yellow_orange": "#ffd166",
    "ibm_black": "#161616",
    "dark_slate": "#0d1117",
    "card_black": "#161b22",
    "grid_gray": "#21262d",
    "ibm_gray": "#262625",
    "border_gray": "#30363d",
    "charcoal": "#1e293b",
    "granite": "#264653",
    "slate": "#64748b",
    "text_muted": "#8b949e",
    "text_white": "#e6edf3",
    "ibm_white": "#f4f4f4",
    "ghost_white": "#f8fafc",
    "node-0": "#fff9d6",
    "cosmic_center": "#0a0f1f",
    "cosmic_void": "#050812",
    "pure_black": "#000000",
    "ice_cyan": "#c8f8ff",
    "text_primary": "#f0f6fc",
    "text_subtle": "#6e7681",
    "accent_green": "#38fe52",
    "accent_blue": "#3881fe",
    "accent_magenta": "#fe38e4",
    "accent_amber": "#feb538",
}

# -----------------------------------------------------------------------------------------------------------
# 1️⃣ Public API
# -----------------------------------------------------------------------------------------------------------


def hex_to_rgb(hex_color: str) -> RGB:
    """
    Convert a six-digit hex color string, with or without leading '#', to an (R, G, B) tuple.

    Parameters
    ----------
    hex_color : str
        Hex color string (e.g. '#00a6ff' or '00a6ff').

    Returns
    -------
    RGB
        Tuple of three integer color channels (0 to 255).

    Raises
    ------
    ValueError
        If hex_color is not a valid 6-digit hexadecimal color string.
    """
    value = hex_color.removeprefix("#")
    if re.fullmatch(r"[0-9a-fA-F]{6}", value) is None:
        raise ValueError(f"Expected a six-digit hex color, got {hex_color!r}")

    return (
        int(value[0:2], 16),
        int(value[2:4], 16),
        int(value[4:6], 16),
    )


def interpolate_rgb(
    color_a: Color,
    color_b: Color,
    factor: float,
    *,
    use_golden_easing: bool = True,
) -> RGB:
    """
    Interpolate smoothly between two RGB colors using a normalized factor in [0.0, 1.0].

    Parameters
    ----------
    color_a : Color
        Starting color as a 6-digit hex string or (R, G, B) integer tuple.
    color_b : Color
        Ending color as a 6-digit hex string or (R, G, B) integer tuple.
    factor : float
        Interpolation progress parameter clamped to [0.0, 1.0].
    use_golden_easing : bool, default=True
        Whether to apply golden ratio curvature easing.

    Returns
    -------
    RGB
        Interpolated (R, G, B) integer tuple with channels bounded in [0, 255].
    """
    rgb_a = _normalize_color(color_a)
    rgb_b = _normalize_color(color_b)

    clamped_factor = max(0.0, min(1.0, float(factor)))
    eased_factor = (
        _golden_ratio_ease(clamped_factor) if use_golden_easing else clamped_factor
    )

    r = round(rgb_a[0] + (rgb_b[0] - rgb_a[0]) * eased_factor)
    g = round(rgb_a[1] + (rgb_b[1] - rgb_a[1]) * eased_factor)
    b = round(rgb_a[2] + (rgb_b[2] - rgb_a[2]) * eased_factor)

    return (
        max(0, min(255, r)),
        max(0, min(255, g)),
        max(0, min(255, b)),
    )


def generate_golden_ratio_gradient(
    colors: Sequence[Color] | None = None,
    length: int | None = None,
    *,
    use_golden_easing: bool = True,
) -> list[RGB]:
    """
    Generate a continuous sequence of RGB color stops implementing the Golden Ratio.

    The total sample count is proportioned according to the Golden Ratio
    (length = round(N * GOLDEN_RATIO)) when `length` is omitted, and interpolates
    through all provided color stops using golden ratio curvature transitions.

    Parameters
    ----------
    colors : Sequence[Color] | None, default=None
        Sequence of color stops (hex codes or RGB tuples). If None, all colors in
        COLOR_PALETTE are utilized.
    length : int | None, default=None
        Total number of output RGB color samples. If None, derived from the number
        of stops via the golden ratio.
    use_golden_easing : bool, default=True
        Whether to apply golden ratio curvature easing across color transitions.

    Returns
    -------
    list[RGB]
        List of interpolated (R, G, B) tuples.

    Raises
    ------
    ValueError
        If fewer than two color stops are supplied or requested length < 1.
    """
    if colors is None:
        palette_colors: Sequence[Color] = tuple(COLOR_PALETTE.values())
    else:
        palette_colors = colors

    if len(palette_colors) < 2:
        raise ValueError("Golden ratio gradient requires at least two color stops.")

    rgb_stops = [_normalize_color(c) for c in palette_colors]
    num_stops = len(rgb_stops)

    if length is None:
        target_length = max(2, round(num_stops * GOLDEN_RATIO))
    else:
        if length < 1:
            raise ValueError(f"Length must be a positive integer, got {length}.")
        target_length = length

    if target_length == 1:
        return [rgb_stops[0]]

    segments = num_stops - 1
    gradient_samples: list[RGB] = []

    for i in range(target_length):
        progress = i / (target_length - 1)
        scaled_pos = progress * segments
        seg_idx = min(int(scaled_pos), segments - 1)
        seg_frac = scaled_pos - seg_idx

        sample_rgb = interpolate_rgb(
            rgb_stops[seg_idx],
            rgb_stops[seg_idx + 1],
            seg_frac,
            use_golden_easing=use_golden_easing,
        )
        gradient_samples.append(sample_rgb)

    return gradient_samples


def render_golden_ratio_gradient(
    colors: Sequence[Color] | None = None,
    length: int | None = None,
    block_char: str = "█",
    *,
    bold: bool = False,
    use_golden_easing: bool = True,
) -> str:
    """
    Render a smooth ANSI TrueColor gradient using the provided colors proportioned
    by the Golden Ratio.

    Parameters
    ----------
    colors : Sequence[Color] | None, default=None
        Sequence of color stops. Defaults to all colors in COLOR_PALETTE.
    length : int | None, default=None
        Total character width of the rendered gradient bar. If None, derived from
        the number of stops via the golden ratio.
    block_char : str, default="█"
        Character glyph rendered for each gradient column.
    bold : bool, default=False
        Whether to apply ANSI bold styling.
    use_golden_easing : bool, default=True
        Whether to apply golden ratio curvature easing.

    Returns
    -------
    str
        ANSI TrueColor formatted string with terminal color reset appended.
    """
    rgb_samples = generate_golden_ratio_gradient(
        colors=colors,
        length=length,
        use_golden_easing=use_golden_easing,
    )
    style = "1;" if bold else ""
    output_chars: list[str] = [
        f"\033[{style}38;2;{r};{g};{b}m{block_char}" for r, g, b in rgb_samples
    ]
    output_chars.append("\033[0m")
    return "".join(output_chars)


# -----------------------------------------------------------------------------------------------------------
# 2️⃣ Private Helpers
# -----------------------------------------------------------------------------------------------------------


def _golden_ratio_ease(t: float) -> float:
    """
    Compute golden ratio curvature easing: u = t^phi / (t^phi + (1 - t)^phi).

    Parameters
    ----------
    t : float
        Linear normalized position in [0.0, 1.0].

    Returns
    -------
    float
        Symmetrically eased progress value in [0.0, 1.0].
    """
    if t <= 0.0:
        return 0.0
    if t >= 1.0:
        return 1.0

    t_phi = math.pow(t, GOLDEN_RATIO)
    one_minus_t_phi = math.pow(1.0 - t, GOLDEN_RATIO)
    denom = t_phi + one_minus_t_phi
    if denom == 0.0:
        return t
    return t_phi / denom


def _normalize_color(color: Color) -> RGB:
    """
    Validate and convert a hex string or RGB tuple into a verified (R, G, B) tuple.

    Parameters
    ----------
    color : Color
        A six-digit hex string or an (R, G, B) tuple.

    Returns
    -------
    RGB
        Validated (R, G, B) tuple with integer channels in [0, 255].

    Raises
    ------
    ValueError
        If channels are invalid, non-integer, or out of range.
    """
    if isinstance(color, str):
        return hex_to_rgb(color)

    if (
        len(color) != 3
        or any(not isinstance(ch, int) or isinstance(ch, bool) for ch in color)
        or any(not 0 <= ch <= 255 for ch in color)
    ):
        raise ValueError(
            f"RGB colors must contain three integers from 0 to 255: {color!r}"
        )

    return color


# -----------------------------------------------------------------------------------------------------------
# 3️⃣ Smoke Tests / Example Usage
# -----------------------------------------------------------------------------------------------------------


def run_smoke_test() -> bool:
    """
    Validate the canonical color definitions and render a golden-ratio palette gradient.

    Every hex value in COLOR_PALETTE is checked for validity before the full palette
    is rendered as a smooth gradient line.

    Returns
    -------
    bool
        True if all checks pass.
    """
    print("Running colors.py smoke tests...")

    # 1. Validate every hex value in the flat palette
    for name, hex_value in COLOR_PALETTE.items():
        rgb = hex_to_rgb(hex_value)
        assert all(0 <= c <= 255 for c in rgb), f"Channel out of range for {name}"

    # 2. Render the canonical palette
    print()
    gradient = render_golden_ratio_gradient(tuple(COLOR_PALETTE.values()))
    print(f"  COLOR_PALETTE: {gradient}")

    print("\nSmoke tests passed.")
    return True


def _run_smoke_test() -> None:
    """Internal smoke test runner matching existing interface."""
    run_smoke_test()


# -----------------------------------------------------------------------------------------------------------
# 🔥 Entry Point
# -----------------------------------------------------------------------------------------------------------


def main() -> None:
    """Execute module smoke tests and output the palette gradient."""
    _run_smoke_test()


if __name__ == "__main__":
    main()
