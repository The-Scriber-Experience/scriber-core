"""
colors.py

Gold Standard color module for the eigenscribe frontend: canonical color
tokens, design values, and the golden ratio gradient
interpolation engine for CLI formatting, Matplotlib plotting, mermaid diagrams,
and UI styling.

The conceptual story follows the repository's 'Rule of Thumb':
What exists (the palette) -> what you're allowed to call (hex_to_rgb and the
gradient API) -> how it works (validation, easing, interpolation) ->
proof it works (palette gradient rendering).

Author: Eigenscribe
Review status: Reviewed and maintained by Eigenscribe.
Date: November 14, 2026
Last Updated: November 18, 2026
"""

from __future__ import annotations

import math
import re
import sys
from collections.abc import Sequence
from typing import Final, TypeAlias

from eigenscribe.frontend.colors import COLOR_PALETTE

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

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
# 🎭 Typing helpers / constants (define once, use Final)
# -----------------------------------------------------------------------------------------------------------

RGB: TypeAlias = tuple[int, int, int]
Color: TypeAlias = str | RGB

GOLDEN_RATIO: Final[float] = (1.0 + 5.0**0.5) / 2.0  # ≈ 1.618033988749895
PHI: Final[float] = GOLDEN_RATIO
GOLDEN_RATIO_INVERSE: Final[float] = GOLDEN_RATIO - 1.0  # 1/φ ≈ 0.618033988749895


# -----------------------------------------------------------------------------------------------------------
# 1️⃣ Core definitions (what exists)
# COLOR_PALETTE is imported from the package and remains the only authored hex palette.
# -----------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------
# 2️⃣ Public API (functions users are meant to call)
# -----------------------------------------------------------------------------------------------------------


def hex_to_rgb(hex_color: str) -> RGB:
    """Convert a six-digit hex color string to an (R, G, B) tuple.

    Parameters
    ----------
    hex_color : str
        Six-digit hexadecimal color string, typically from COLOR_PALETTE.

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
    """Interpolate smoothly between two RGB colors using a factor in [0.0, 1.0].

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
    """Generate a continuous sequence of RGB stops proportioned by the golden ratio.

    The total sample count defaults to round(N * GOLDEN_RATIO) for N color stops,
    interpolating through all provided stops with golden ratio curvature transitions.

    Parameters
    ----------
    colors : Sequence[Color] | None, default=None
        Sequence of color stops (hex codes or RGB tuples). If None, all colors in
        COLOR_PALETTE are utilized.
    length : int | None, default=None
        Total number of output RGB samples. If None, derived from the number of
        stops via the golden ratio.
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
    """Render a smooth ANSI TrueColor gradient bar proportioned by the golden ratio.

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
# 3️⃣ Private helpers (how it works)
# -----------------------------------------------------------------------------------------------------------


def _golden_ratio_ease(t: float) -> float:
    """Compute golden ratio curvature easing: u = t^phi / (t^phi + (1 - t)^phi).

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
    """Validate and convert a hex string or RGB tuple into an (R, G, B) tuple.

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
# 4️⃣ 💨 Smoke tests / example usage (proof it works)
# -----------------------------------------------------------------------------------------------------------


def run_smoke_test() -> bool:
    """Validate canonical color tokens and render one gradient from the palette.

    Every palette hex value is checked for validity before the complete palette is
    rendered as a smooth gradient line.

    Returns
    -------
    bool
        True if all validation checks pass.
    """
    print("Running colors.py smoke tests...")

    # Validate every hex value in the flat palette
    is_valid: bool = True
    for name, hex_value in COLOR_PALETTE.items():
        rgb = hex_to_rgb(hex_value)
        if not all(0 <= c <= 255 for c in rgb):
            is_valid = False
            print(f"  ✗ Channel out of range for {name}: {hex_value}")

    # Render the canonical palette
    print()
    gradient = render_golden_ratio_gradient(tuple(COLOR_PALETTE.values()))
    print(f"  COLOR_PALETTE: {gradient}")

    print("\n✅💨Smoke tests passed." if is_valid else "\nSmoke tests FAILED.")
    return is_valid


# -----------------------------------------------------------------------------------------------------------
# 🔥 Entry point
# -----------------------------------------------------------------------------------------------------------


def main() -> None:
    """Orchestrate palette validation and gradient demonstration output.

    Never contains raw color math logic directly.
    """
    success = run_smoke_test()
    if not success:
        raise ValueError("Palette validation failed during smoke test checks.")


if __name__ == "__main__":
    main()
