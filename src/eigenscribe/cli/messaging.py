"""
messaging.py

Terminal messaging, semantic status alerts, ANSI 256-color palette styling, and
gradient banner generators for the Scriber Core frontend suite.

The conceptual story follows the Eigenscribe architectural standard:
What exists -> What you're allowed to call -> How it works -> Proof it works.

Author: Eigenscribe & Scriber Labs
Date: November 17, 2026
"""

from __future__ import annotations

import os
import re
import sys
from typing import Final, Sequence

import click

from eigenscribe.frontend.colors import COLOR_PALETTE, Color, RGB, hex_to_rgb
from eigenscribe.frontend.gradients import GRADIENT_PRESETS, multi_gradient

try:
    from .vt_mode import enable_vt_mode
except ImportError:
    from eigenscribe.cli.vt_mode import enable_vt_mode


_HAS_CLICK: Final[bool] = True


__all__: list[str] = [
    # Core messaging
    "cli_message",
    "cli_echo",
    "cli_rule",
    "cli_banner",
    # Semantic level helpers
    "cli_info",
    "cli_success",
    "cli_warning",
    "cli_error",
    "cli_highlight",
    # Render formatters (string returning)
    "render_message",
    "render_echo",
    "render_rule",
    "render_banner",
    # Gradients & Colors re-exports
    "multi_gradient",
    "GRADIENT_PRESETS",
    "PRIMARY_GRADIENT",
    "SECONDARY_GRADIENT",
    "Color",
    "RGB",
    "hex_to_rgb",
    # Palettes & Styling maps
    "EIGENSCRIBE_PALETTE",
    "STYLE_MAP",
    "ansi_256",
    "supports_256_color",
    # CLI & Smoke tests
    "cli",
    "main",
    "run_smoke_test",
]


# -----------------------------------------------------------------------------------------------------------
# 🎭 Typing helpers / constants (define once, use Final)
# -----------------------------------------------------------------------------------------------------------

PRIMARY_GRADIENT: Final[tuple[str, ...]] = GRADIENT_PRESETS["eigenscribe"]
SECONDARY_GRADIENT: Final[tuple[str, ...]] = GRADIENT_PRESETS["purple_gradient"]

# Eigenscribe brand palette mapped to ANSI 256-color indices
EIGENSCRIBE_PALETTE: Final[dict[str, int]] = {
    # --- Blues & Cosmic Foundations (Primary domain) ---
    "eigen_cosmic_void": 16,  # Deep cosmic void black
    "eigen_cosmic_navy": 17,  # Deep cosmic navy
    "eigen_blue_dark": 25,  # Deep navy blue
    "eigen_blue": 27,  # Core Eigenscribe blue
    "eigen_blue_bright": 33,  # Bright electric blue
    "eigen_azure": 32,  # Azure blue
    "eigen_cyan": 51,  # Electric cyan for info
    "eigen_cyan_light": 81,  # Light cyan accent
    "eigen_cyan_pure": 51,  # Pure cyan
    "eigen_luminous_cyan": 123,  # Luminous ice-cyan
    "eigen_sephirah_cyan": 123,  # Legacy alias
    "eigen_sky": 39,  # EIGEN Sky Blue
    # --- Vibrant 10-Node Spectrum ---
    "eigen_node_0": 230,  # 0. Crown / White-Gold
    "eigen_node_1": 51,  # 1. Electric Cyan
    "eigen_node_2": 45,  # 2. Bright Cyan
    "eigen_node_3": 39,  # 3. Sky Blue
    "eigen_node_4": 27,  # 4. Royal Cobalt
    "eigen_node_5": 220,  # 5. Radiant Amber Gold
    "eigen_node_6": 129,  # 6. Electric Purple
    "eigen_node_7": 93,  # 7. Deep Violet
    "eigen_node_8": 205,  # 8. Vibrant Neon Pink
    "eigen_node_9": 40,  # 9. Vivid Emerald Green
    # Legacy node aliases
    "sephirah_keter": 230,
    "sephirah_chokhmah": 51,
    "sephirah_binah": 45,
    "sephirah_chesed": 39,
    "sephirah_gevurah": 27,
    "sephirah_tiferet": 220,
    "sephirah_netzach": 129,
    "sephirah_hod": 93,
    "sephirah_yesod": 205,
    "sephirah_malkuth": 40,
    # --- 4-Color Vibrant Accent Set ---
    "eigen_accent_green": 83,  # Bright lime-green
    "eigen_accent_blue": 33,  # Cobalt accent blue
    "eigen_accent_magenta": 206,  # Vivid magenta
    "eigen_accent_amber": 215,  # Warm amber
    # --- Purples (Secondary domain) ---
    "eigen_purple_dark": 55,  # Deep violet
    "eigen_purple": 129,  # Core Eigenscribe purple
    "eigen_purple_bright": 141,  # Bright magenta-purple
    "eigen_magenta": 163,  # Magenta for highlights
    "eigen_synthwave_purple": 99,  # Synthwave indigo-violet
    # --- Pinks (Accent domain) ---
    "eigen_pink": 212,  # Soft pink accent
    "eigen_pink_bright": 199,  # Bright pink for emphasis
    "eigen_hot_pink": 198,  # Hot neon pink
    # --- Greens (Success domain) ---
    "eigen_green_dark": 22,  # Deep forest green
    "eigen_green": 35,  # Core green
    "eigen_green_bright": 41,  # Bright success green
    "eigen_mint": 121,  # Mint green accent
    # --- Oranges/Ambers (Warning domain) ---
    "eigen_amber": 214,  # Amber warning
    "eigen_orange": 208,  # Core orange
    "eigen_orange_bright": 202,  # Bright orange accent
    "eigen_coral": 209,  # Coral orange
    # --- Reds (Error domain) ---
    "eigen_red": 160,  # Soft red for errors
    "eigen_red_bright": 196,  # Bright red for critical errors
    # --- Neutrals ---
    "eigen_white": 189,  # Soft white
    "eigen_gray": 145,  # Medium gray
    "eigen_gray_dark": 102,  # Dark gray for dimmed text
}

# Semantic style map: maps message levels to palette keys
STYLE_MAP: Final[dict[str, str]] = {
    "info": "sky_info",
    "success": "success_emerald",
    "warning": "warning_amber",
    "error": "error_crimson",
    "highlight": "bright_pink",
    "banner_title": "node-3",
    "banner_sub": "node-6",
    "rule": "eigen_blue",
}

_EIGENSCRIBE_COLOR_TOKENS: Final[dict[str, str]] = {
    "eigen_cosmic_void": "deep_plum",
    "eigen_cosmic_navy": "midnight_navy",
    "eigen_blue_dark": "deep_ocean_blue",
    "eigen_blue": "eigen_blue",
    "eigen_blue_bright": "electric_blue",
    "eigen_azure": "skyline_blue",
    "eigen_cyan": "node-2",
    "eigen_cyan_light": "ice_blue",
    "eigen_cyan_pure": "electric_cyan",
    "eigen_luminous_cyan": "ice_blue",
    "eigen_sephirah_cyan": "node-2",
    "eigen_sky": "node-3",
    "eigen_node_0": "node-0",
    "eigen_node_1": "node-1",
    "eigen_node_2": "node-2",
    "eigen_node_3": "node-3",
    "eigen_node_4": "node-4",
    "eigen_node_5": "node-5",
    "eigen_node_6": "node-6",
    "eigen_node_7": "node-7",
    "eigen_node_8": "node-8",
    "eigen_node_9": "node-9",
    "sephirah_keter": "node-0",
    "sephirah_chokhmah": "node-1",
    "sephirah_binah": "node-2",
    "sephirah_chesed": "node-3",
    "sephirah_gevurah": "node-4",
    "sephirah_tiferet": "node-5",
    "sephirah_netzach": "node-6",
    "sephirah_hod": "node-7",
    "sephirah_yesod": "node-8",
    "sephirah_malkuth": "node-9",
    "eigen_accent_green": "bright_green",
    "eigen_accent_blue": "cornflower",
    "eigen_accent_magenta": "bright_magenta",
    "eigen_accent_amber": "golden_amber",
    "eigen_purple_dark": "dark_violet",
    "eigen_purple": "node-6",
    "eigen_purple_bright": "bright_purple",
    "eigen_magenta": "bright_magenta",
    "eigen_synthwave_purple": "cosmic_iris",
    "eigen_pink": "soft_rose",
    "eigen_pink_bright": "bright_pink",
    "eigen_hot_pink": "hot_pink",
    "eigen_green_dark": "green_dark",
    "eigen_green": "pine",
    "eigen_green_bright": "bright_green",
    "eigen_mint": "pale_mint",
    "eigen_amber": "warning_amber",
    "eigen_orange": "tangerine",
    "eigen_orange_bright": "coral_orange",
    "eigen_coral": "coral_orange",
    "eigen_red": "deep_rose",
    "eigen_red_bright": "error_crimson",
    "eigen_white": "text_white",
    "eigen_gray": "slate",
    "eigen_gray_dark": "text_muted",
}

# Fallback 16-color map for terminals that don't support 256 colors
_FALLBACK_16: Final[dict[str, str]] = {
    "info": "bright_cyan",
    "success": "bright_green",
    "warning": "bright_yellow",
    "error": "bright_red",
    "highlight": "bright_magenta",
    "banner_title": "bright_blue",
    "banner_sub": "bright_magenta",
    "rule": "bright_blue",
}


# -----------------------------------------------------------------------------------------------------------
# 1️⃣ Core definitions (what exists) — Color Detection & ANSI Helpers
# -----------------------------------------------------------------------------------------------------------


def supports_256_color() -> bool:
    """
    Detect whether the current terminal supports 256-color output.

    Returns
    -------
    bool
        True if the terminal appears to support 256 colors.
    """
    colorterm = os.environ.get("COLORTERM", "")
    if "256color" in colorterm or "truecolor" in colorterm or "24bit" in colorterm:
        return True

    # Windows 10+ with modern terminals (Windows Terminal, Conhost with VT)
    if sys.platform == "win32":
        return True

    # Fallback: check TERM env var
    term = os.environ.get("TERM", "")
    return "256color" in term or "xterm" in term or "screen" in term or "vt100" in term


def ansi_256(color_name: str, text: str, bold: bool = False) -> str:
    """
    Wrap text with ANSI 256-color escape codes using the Eigenscribe palette.

    Parameters
    ----------
    color_name : str
        Key from EIGENSCRIBE_PALETTE (e.g., 'eigen_blue', 'eigen_purple').
    text : str
        The text to colorize.
    bold : bool, default=False
        Whether to apply bold weight.

    Returns
    -------
    str
        The ANSI-escaped string ready for terminal output.

    Examples
    --------
    >>> ansi_256("eigen_blue", "Hello, world!", bold=True)
    '\\x1b[1;38;5;27mHello, world!\\x1b[0m'
    """
    color_index = EIGENSCRIBE_PALETTE.get(color_name)
    if color_index is None:
        return text

    bold_code = "1;" if bold else ""
    return f"\033[{bold_code}38;5;{color_index}m{text}\033[0m"


def _ansi_truecolor(color_name: str, text: str, bold: bool = False) -> str:
    """Render a canonical palette token or legacy palette alias in TrueColor."""
    token = _EIGENSCRIBE_COLOR_TOKENS.get(color_name, color_name)
    hex_code = COLOR_PALETTE.get(token)
    if hex_code is None:
        return text

    red, green, blue = hex_to_rgb(hex_code)
    bold_code = "1;" if bold else ""
    return f"\033[{bold_code}38;2;{red};{green};{blue}m{text}\033[0m"


def _ansi_256_raw(fg_index: int, text: str, bold: bool = False) -> str:
    """
    Apply a raw 256-color index directly (for dynamic color generation).

    Parameters
    ----------
    fg_index : int
        ANSI 256-color index (0-255).
    text : str
        The text to colorize.
    bold : bool, default=False
        Whether to apply bold weight.

    Returns
    -------
    str
        The ANSI-escaped string.
    """
    bold_code = "1;" if bold else ""
    return f"\033[{bold_code}38;5;{fg_index}m{text}\033[0m"


# -----------------------------------------------------------------------------------------------------------
# 2️⃣ Public API (functions users are meant to call)
# -----------------------------------------------------------------------------------------------------------


def render_message(msg: str, level: str = "info", bold: bool = False) -> str:
    """
    Format a styled message string using the Eigenscribe semantic color palette.

    Parameters
    ----------
    msg : str
        Message content to format.
    level : str, default='info'
        Semantic level key from STYLE_MAP.
    bold : bool, default=False
        Whether to format the text in bold weight.

    Returns
    -------
    str
        Styled message string with ANSI codes.
    """
    color_key = STYLE_MAP.get(level, STYLE_MAP["info"])
    return _ansi_truecolor(color_key, msg, bold=bold)


def cli_message(msg: str, level: str = "info", bold: bool = False) -> None:
    """
    Print a styled message using the Eigenscribe semantic color palette.

    Emits the canonical 24-bit RGB color for the selected semantic level.

    Parameters
    ----------
    msg : str
        Message content to display.
    level : str, default='info'
        Semantic level key from STYLE_MAP.
    bold : bool, default=False
        Whether to format the text in bold weight.
    """
    _echo(render_message(msg, level=level, bold=bold))


def render_echo(
    msg: str,
    color: str | None = None,
    bold: bool = False,
    level: str | None = None,
) -> str:
    """
    Format arbitrary text with a specific Eigenscribe palette color or semantic level.

    Parameters
    ----------
    msg : str
        Message content to format.
    color : str, optional
        Direct palette key from COLOR_PALETTE or a legacy Eigenscribe alias.
    bold : bool, default=False
        Whether to apply bold weight.
    level : str, optional
        Fallback semantic level if color is not provided.

    Returns
    -------
    str
        Styled text string.
    """
    if color is not None:
        return _ansi_truecolor(color, msg, bold=bold)
    if level is not None:
        return render_message(msg, level=level, bold=bold)
    return msg


def cli_echo(
    msg: str,
    color: str | None = None,
    bold: bool = False,
    level: str | None = None,
) -> None:
    """
    Print arbitrary text with a specific Eigenscribe palette color or semantic level.

    Parameters
    ----------
    msg : str
        Message content to display.
    color : str, optional
        Direct palette key (e.g., 'eigen_blue', 'eigen_pink').
        If provided, takes precedence over `level`.
    bold : bool, default=False
        Whether to apply bold weight.
    level : str, optional
        Fallback semantic level if `color` is not provided.

    Examples
    --------
    >>> cli_echo("My name is ", color="eigen_white")  # doctest: +SKIP
    >>> cli_echo("EigenBeast", color="eigen_purple", bold=True)  # doctest: +SKIP
    """
    if color is not None:
        _echo(render_echo(msg, color=color, bold=bold))
    elif level is not None:
        cli_message(msg, level=level, bold=bold)
    else:
        _echo(msg)


def render_rule(char: str = "─", width: int = 60, level: str = "rule") -> str:
    """
    Render a horizontal rule line with semantic coloring.

    Parameters
    ----------
    char : str, default='─'
        Character to repeat for the rule line.
    width : int, default=60
        Number of characters wide.
    level : str, default='rule'
        Semantic color level.

    Returns
    -------
    str
        Styled rule string.
    """
    line = char * width
    return render_message(line, level=level)


def cli_rule(char: str = "─", width: int = 60, level: str = "rule") -> None:
    """
    Print a horizontal rule line with semantic coloring.

    Parameters
    ----------
    char : str, default='─'
        Character to repeat for the rule line.
    width : int, default=60
        Number of characters wide.
    level : str, default='rule'
        Semantic color level.
    """
    line = char * width
    cli_message(line, level=level)


def render_banner(
    title: str,
    subtitle: str | None = None,
    width: int = 60,
    colors: Sequence[str] = PRIMARY_GRADIENT,
) -> str:
    """
    Render a styled banner header with Eigenscribe gradient colors and divider rule.

    Parameters
    ----------
    title : str
        Main banner title.
    subtitle : str, optional
        Optional secondary subtitle line.
    width : int, default=60
        Horizontal divider width.
    colors : sequence of str, default=PRIMARY_GRADIENT
        Canonical hex colors for the title gradient.

    Returns
    -------
    str
        Formatted banner string.
    """
    lines: list[str] = ["", multi_gradient(title, colors=colors, bold=True)]
    if subtitle:
        lines.append(multi_gradient(subtitle, colors=SECONDARY_GRADIENT, bold=False))
    lines.append(render_rule(char="─", width=width, level="rule"))
    lines.append("")
    return "\n".join(lines)


def cli_banner(title: str, subtitle: str | None = None) -> None:
    """
    Print a styled banner header with Eigenscribe PRIMARY_GRADIENT colors.

    Parameters
    ----------
    title : str
        Main banner title.
    subtitle : str, optional
        Optional secondary subtitle line.

    Examples
    --------
    >>> cli_banner("EIGENBEAST BATTLE", "The Non-Copyright Generic Beast Game")  # doctest: +SKIP
    """
    _echo("")
    _echo(multi_gradient(title, colors=PRIMARY_GRADIENT, bold=True))

    if subtitle:
        _echo(multi_gradient(subtitle, colors=SECONDARY_GRADIENT, bold=False))

    cli_rule(level="rule")
    _echo("")


def cli_info(msg: str) -> None:
    """
    Print an informational prompt (Electric Cyan) with informational emoji anchor.

    Parameters
    ----------
    msg : str
        Informational message string.
    """
    cli_message(f"ℹ️  {msg}", level="info")


def cli_success(msg: str) -> None:
    """
    Print a success confirmation (Bright Green) with checkmark emoji anchor.

    Parameters
    ----------
    msg : str
        Success message string.
    """
    cli_message(f"✅ {msg}", level="success", bold=True)


def cli_warning(msg: str) -> None:
    """
    Print a warning notification (Amber) with warning emoji anchor.

    Parameters
    ----------
    msg : str
        Warning message string.
    """
    cli_message(f"⚠️  {msg}", level="warning")


def cli_error(msg: str) -> None:
    """
    Print an error alert (Bright Red) with error emoji anchor.

    Parameters
    ----------
    msg : str
        Error message string.
    """
    cli_message(f"❌ {msg}", level="error", bold=True)


def cli_highlight(msg: str) -> None:
    """
    Print an emphasized highlight message (Bright Pink) with sparkles emoji anchor.

    Parameters
    ----------
    msg : str
        Highlight message string.
    """
    cli_message(f"✨ {msg}", level="highlight", bold=True)


# -----------------------------------------------------------------------------------------------------------
# 3️⃣ Private helpers (how it works)
# -----------------------------------------------------------------------------------------------------------


def _echo(text: str) -> None:
    """Print text using click.echo if available, otherwise fall back to print."""
    enable_vt_mode()
    try:
        if _HAS_CLICK:
            click.echo(text, color=True)
        else:
            print(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        safe_text = text.encode(encoding, errors="replace").decode(encoding)
        if _HAS_CLICK:
            click.echo(safe_text, color=True)
        else:
            print(safe_text)


def _secho(text: str, fg: str | None = None, bold: bool = False) -> None:
    """Print styled text using click.secho if available, otherwise fall back to print."""
    if _HAS_CLICK:
        click.secho(text, fg=fg, bold=bold)
    else:
        print(text)


# -----------------------------------------------------------------------------------------------------------
# 4️⃣ 💨 Smoke tests / example usage (proof it works)
# -----------------------------------------------------------------------------------------------------------


def run_smoke_test() -> bool:
    """
    Execute smoke test assertions for frontend messaging and ANSI 256-color palette.

    Returns
    -------
    bool
        True if all verification assertions succeed.
    """
    _echo("💨 Running src/eigenscribe/cli/messaging.py smoke tests...")

    # 1. Palette completeness assertions
    assert len(EIGENSCRIBE_PALETTE) >= 40
    assert EIGENSCRIBE_PALETTE["eigen_cyan"] == 51
    assert EIGENSCRIBE_PALETTE["eigen_blue"] == 27
    assert EIGENSCRIBE_PALETTE["eigen_purple"] == 129
    assert EIGENSCRIBE_PALETTE["eigen_green_bright"] == 41
    assert EIGENSCRIBE_PALETTE["eigen_amber"] == 214
    assert EIGENSCRIBE_PALETTE["eigen_red_bright"] == 196
    assert EIGENSCRIBE_PALETTE["eigen_pink_bright"] == 199

    # 2. ANSI 256 formatting assertions
    formatted = ansi_256("eigen_cyan", "Test Message", bold=True)
    assert "\033[1;38;5;51mTest Message\033[0m" == formatted

    plain_fallback = ansi_256("non_existent_key", "Fallback text")
    assert plain_fallback == "Fallback text"

    raw_formatted = _ansi_256_raw(45, "Raw Index")
    assert "\033[38;5;45mRaw Index\033[0m" == raw_formatted

    # 3. Message rendering assertions
    rendered_info = render_message("Information Alert", level="info")
    assert "38;2;56;189;248m" in rendered_info
    assert "Information Alert" in rendered_info

    rendered_banner = render_banner("BANNER TITLE", "Banner Subtitle")
    plain_banner = re.sub(r"\x1b\[[0-9;]*m", "", rendered_banner)
    assert "BANNER TITLE" in plain_banner
    assert "Banner Subtitle" in plain_banner
    assert "─" in rendered_banner

    rendered_rule = render_rule("═", width=40, level="rule")
    assert "═" * 40 in rendered_rule

    rendered_echo = render_echo("Echo String", color="eigen_pink", bold=True)
    assert "1;38;2;255;118;161m" in rendered_echo

    # 4. Interactive visual smoke test
    cli_banner("SCRIBER CORE FRONTEND MESSAGING TEST", "256-Color & TrueColor Verification")
    cli_info("Info message — Electric Cyan")
    cli_success("Success message — Bright Green")
    cli_warning("Warning message — Amber")
    cli_error("Error message — Bright Red")
    cli_highlight("Highlight message — Bright Pink")
    cli_rule()

    _echo("✅ src/eigenscribe/cli/messaging.py smoke tests passed successfully.\n")
    return True


# -----------------------------------------------------------------------------------------------------------
# 🔥 Entry point
# -----------------------------------------------------------------------------------------------------------


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx: click.Context) -> None:
    """
    🔱 Scriber Core Frontend Messaging & Terminal Styling Suite.
    """
    if ctx.invoked_subcommand is None:
        run_smoke_test()


@cli.command(name="banner", help="Print a styled TrueColor gradient banner header.")
@click.argument("title")
@click.option("--subtitle", "-s", default=None, help="Optional secondary subtitle.")
def banner_cmd(title: str, subtitle: str | None) -> None:
    """Print a styled banner."""
    cli_banner(title, subtitle)


@cli.command(name="info", help="Print an informational prompt message.")
@click.argument("message")
def info_cmd(message: str) -> None:
    """Print info message."""
    cli_info(message)


@cli.command(name="success", help="Print a success confirmation message.")
@click.argument("message")
def success_cmd(message: str) -> None:
    """Print success message."""
    cli_success(message)


@cli.command(name="warning", help="Print a warning notification message.")
@click.argument("message")
def warning_cmd(message: str) -> None:
    """Print warning message."""
    cli_warning(message)


@cli.command(name="error", help="Print an error alert message.")
@click.argument("message")
def error_cmd(message: str) -> None:
    """Print error message."""
    cli_error(message)


@cli.command(name="highlight", help="Print an emphasized highlight message.")
@click.argument("message")
def highlight_cmd(message: str) -> None:
    """Print highlight message."""
    cli_highlight(message)


@cli.command(name="palette", help="Display the Eigenscribe TrueColor palette showcase.")
def palette_cmd() -> None:
    """Display the named palette using canonical TrueColor values."""
    cli_rule()
    cli_echo("🎨 Eigenscribe TrueColor Palette Showcase:", color="eigen_white", bold=True)
    cli_rule()
    groups: dict[str, list[str]] = {
        "🔵 Blues": [
            "eigen_blue_dark",
            "eigen_blue",
            "eigen_blue_bright",
            "eigen_cyan",
            "eigen_cyan_light",
        ],
        "🟣 Purples": [
            "eigen_purple_dark",
            "eigen_purple",
            "eigen_purple_bright",
            "eigen_magenta",
        ],
        "🩷 Pinks": ["eigen_pink", "eigen_pink_bright", "eigen_hot_pink"],
        "🟢 Greens": [
            "eigen_green_dark",
            "eigen_green",
            "eigen_green_bright",
            "eigen_mint",
        ],
        "🟠 Oranges": ["eigen_amber", "eigen_orange", "eigen_orange_bright", "eigen_coral"],
        "🔴 Reds": ["eigen_red", "eigen_red_bright"],
        "⚪ Neutrals": ["eigen_white", "eigen_gray", "eigen_gray_dark"],
    }
    for label, colors in groups.items():
        parts = [render_echo(c, color=c) for c in colors]
        _echo(f"  {label}: {' '.join(parts)}")
    cli_rule()


@cli.command(name="smoke-test", help="Run deterministic messaging smoke tests.")
def smoke_test_cmd() -> None:
    """Run messaging smoke tests."""
    run_smoke_test()


def main() -> None:
    """Entry point for standalone execution."""
    enable_vt_mode()
    if _HAS_CLICK:
        cli()
    else:
        run_smoke_test()


if __name__ == "__main__":
    main()
