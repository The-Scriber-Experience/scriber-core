# tests/test_frontend_styling.py
"""
test_frontend_styling.py

Test suite verifying Scriber Core frontend design tokens, palettes,
and ANSI TrueColor gradient engine.
"""

from __future__ import annotations

from pathlib import Path

from eigenscribe.cli.messaging import cli_banner, cli_info, cli_success
from eigenscribe import frontend as frontend_module
from eigenscribe.frontend import colors as colors_module
from eigenscribe.frontend import the_scriber_experience as tse_module
from eigenscribe.frontend.the_scriber_experience import plots as plots_module
from eigenscribe.frontend.the_scriber_experience.plots import get_eigenscribe_rcparams
from eigenscribe.frontend.the_scriber_experience.plots import theme as plot_theme

from eigenscribe.frontend import (
    COLOR_PALETTE,
    GOLDEN_RATIO,
    GOLDEN_RATIO_INVERSE,
    GRADIENT_PRESETS,
    PHI,
    compute_golden_ratio_stop_positions,
    generate_golden_ratio_gradient,
    hex_to_rgb,
    interpolate_rgb,
    multi_gradient,
    render_golden_ratio_gradient,
    run_colors_smoke_test,
)


def test_color_palette_validity() -> None:
    """Verify canonical tokens are valid, unique hex colors used by gradients."""
    assert len(COLOR_PALETTE) > 0
    assert len(set(COLOR_PALETTE.values())) == len(COLOR_PALETTE)
    for name, hex_val in COLOR_PALETTE.items():
        rgb = hex_to_rgb(hex_val)
        assert len(rgb) == 3
        assert all(0 <= ch <= 255 for ch in rgb)
    palette_values = set(COLOR_PALETTE.values())
    assert all(
        stop in palette_values
        for stops in GRADIENT_PRESETS.values()
        for stop in stops
    )


def test_node_spectrum_and_sephirah_aliases_use_canonical_palette() -> None:
    """Keep plotting spectra palette-derived without duplicate EIGEN lists."""
    expected_nodes = {f"node_{node}": COLOR_PALETTE[f"node-{node}"] for node in range(10)}
    expected_sephirah_nodes = list(expected_nodes.values())
    expected_sephirah_labels = expected_sephirah_nodes.copy()
    expected_sephirah_labels[5] = COLOR_PALETTE["sky_cyan"]

    assert plot_theme.EIGEN_NODES == expected_nodes
    assert plot_theme.SEPHIRAH_NODE_COLORS == expected_sephirah_nodes
    assert plot_theme.SEPHIRAH_LABEL_COLORS == expected_sephirah_labels
    assert not hasattr(colors_module, "EIGEN_NODE_COLORS")
    assert not hasattr(colors_module, "EIGEN_LABEL_COLORS")
    assert not hasattr(frontend_module, "EIGEN_NODE_COLORS")
    assert not hasattr(frontend_module, "EIGEN_LABEL_COLORS")
    assert not hasattr(tse_module, "EIGEN_NODE_COLORS")
    assert not hasattr(tse_module, "EIGEN_LABEL_COLORS")
    assert not hasattr(plots_module, "EIGEN_NODE_COLORS")
    assert not hasattr(plots_module, "EIGEN_LABEL_COLORS")
    assert not hasattr(plot_theme, "EIGEN_NODE_COLORS")
    assert not hasattr(plot_theme, "EIGEN_LABEL_COLORS")


def test_added_palette_tokens_and_aurora_preset_match_reference_doc() -> None:
    """Verify canonical cosmic/accent additions and gradient catalog are documented."""
    additions = {
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
    for name, hex_value in additions.items():
        assert COLOR_PALETTE[name] == hex_value

    assert GRADIENT_PRESETS["aurora"] == ("#06b6d4", "#10b981", "#84cc16")

    reference = (Path(__file__).resolve().parents[2] / "docs" / "colors-and-gradients.md").read_text(
        encoding="utf-8"
    )
    assert len(COLOR_PALETTE) == 119
    assert "Complete Primitive Palette Table (119 tokens)" in reference
    for name, hex_value in additions.items():
        assert f"| `{name}` | `{hex_value}` |" in reference
    aurora_stops = " → ".join(f"`{color}`" for color in GRADIENT_PRESETS["aurora"])
    assert f"**`aurora`** | {aurora_stops}" in reference


def test_gradient_engine() -> None:
    """Verify multi_gradient output formatting, presets, and golden ratio proportioning."""
    assert len(GRADIENT_PRESETS) >= 6

    # 1. Test golden ratio stop positions
    stops_4 = compute_golden_ratio_stop_positions(4)
    assert len(stops_4) == 4
    assert stops_4[0] == 0.0
    assert stops_4[-1] == 1.0
    # Verify segment proportions decrease from left to right (blue -> purple -> pink)
    seg1 = stops_4[1] - stops_4[0]
    seg2 = stops_4[2] - stops_4[1]
    seg3 = stops_4[3] - stops_4[2]
    assert seg1 > seg2 > seg3
    assert abs((seg2 / seg1) - GOLDEN_RATIO_INVERSE) < 1e-6
    assert abs((seg3 / seg2) - GOLDEN_RATIO_INVERSE) < 1e-6

    # 2. Test multi_gradient with golden ratio scaling
    out = multi_gradient("Test Hello", GRADIENT_PRESETS["electric"], golden_ratio_scale=True)
    assert "\033[0m" in out
    assert len(out) > len("Test Hello")

    # 3. Test multi_gradient without golden ratio scaling
    out_linear = multi_gradient("Test Hello", GRADIENT_PRESETS["electric"], golden_ratio_scale=False)
    assert "\033[0m" in out_linear

    # Empty string handling
    assert multi_gradient("") == ""


def test_cli_messaging() -> None:
    """Verify CLI messaging helpers run without exception."""
    cli_info("Testing info message")
    cli_success("Testing success message")
    cli_banner("TEST APP", "Test subtitle")


def test_plot_theme_rcparams() -> None:
    """Verify Matplotlib rcParams dictionary generation."""
    rc = get_eigenscribe_rcparams(cosmic=False)
    assert isinstance(rc, dict)
    assert "figure.facecolor" in rc
    assert rc["figure.facecolor"] == "#0d1117"


def test_golden_ratio_gradient_and_smoke_test() -> None:
    """Verify golden ratio constants, gradient generation, rendering, and smoke tests."""
    assert abs(GOLDEN_RATIO - 1.618033988749895) < 1e-9
    assert abs(PHI - GOLDEN_RATIO) < 1e-9
    assert abs(GOLDEN_RATIO_INVERSE - (1.0 / GOLDEN_RATIO)) < 1e-9

    all_colors = list(COLOR_PALETTE.values())
    expected_len = round(len(all_colors) * GOLDEN_RATIO)
    samples = generate_golden_ratio_gradient(all_colors)
    assert len(samples) == expected_len
    for rgb in samples:
        assert len(rgb) == 3
        assert all(0 <= ch <= 255 for ch in rgb)

    rendered = render_golden_ratio_gradient(all_colors)
    assert "\033[38;2;" in rendered
    assert "\033[0m" in rendered

    # Interpolate RGB helper check
    mid_rgb = interpolate_rgb("#000000", "#ffffff", 0.5)
    assert mid_rgb == (128, 128, 128)

    # Smoke test execution
    assert run_colors_smoke_test() is True
