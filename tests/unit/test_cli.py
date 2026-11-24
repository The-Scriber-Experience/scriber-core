# tests/test_cli.py
"""
test_cli.py

Automated tests for the Eigenscribe CLI baseline suite (`eigenscribe`).
Verifies command invocation, arguments, styling output, diagnostics, and exit codes.
"""

from __future__ import annotations

import importlib
import re
import click
from click.testing import CliRunner
import pytest

from eigenscribe import __version__ as PACKAGE_VERSION
from eigenscribe.cli import (
    COLOR_PALETTE,
    build_color_entries,
    format_color_swatch,
    format_colored_name,
    print_colors_table,
    render_colors_table,
    run_cli_smoke_test,
)
from eigenscribe.cli.branding import CLI_VERSION
from eigenscribe.cli.colors_table import cli as colors_table_cli
from eigenscribe.cli.main import cli_group, main as cli_entrypoint
from eigenscribe.frontend import __version__ as FRONTEND_VERSION
from eigenscribe.frontend.colors import hex_to_rgb

cli_main_module = importlib.import_module("eigenscribe.cli.main")


@pytest.fixture
def runner() -> CliRunner:
    """Create a click CLI test runner."""
    return CliRunner()


def test_cli_help(runner: CliRunner) -> None:
    """Verify eigenscribe --help prints signature banners and subcommands."""
    result = runner.invoke(cli_group, ["--help"])
    assert result.exit_code == 0
    assert "Eigenscribe CLI" in result.output
    assert "info" in result.output
    assert "gradient" in result.output
    assert "colors" in result.output
    assert "banner" in result.output
    assert "theme" in result.output
    assert "mermaid" in result.output
    assert "doctor" in result.output


def test_cli_entrypoint_preserves_colors_in_help(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Verify the executable entry point keeps ANSI colors when Click renders help."""
    monkeypatch.setattr("eigenscribe.cli.main.enable_vt_mode", lambda: None)
    monkeypatch.setattr("sys.argv", ["eigenscribe", "--help"])

    with pytest.raises(SystemExit) as exc_info:
        cli_entrypoint()

    assert exc_info.value.code == 0
    assert "\033[" in capsys.readouterr().out


def test_cli_version(runner: CliRunner) -> None:
    """Verify eigenscribe --version outputs version badge."""
    result = runner.invoke(cli_group, ["--version"])
    assert result.exit_code == 0
    plain_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert f"eigenscribe v{PACKAGE_VERSION}" in plain_output
    assert FRONTEND_VERSION == CLI_VERSION == PACKAGE_VERSION


def test_cli_no_args_brand_header(runner: CliRunner) -> None:
    """Verify eigenscribe invoked with no args renders banner header."""
    result = runner.invoke(cli_group, [])
    assert result.exit_code == 0
    assert "SCRIBER CORE" in result.output or "Eigenscribe CLI" in result.output


@pytest.mark.parametrize(
    ("installed_version", "msystem", "should_warn"),
    [
        ((8, 4), "UCRT64", True),
        ((8, 5), "UCRT64", False),
        ((8, 4), None, False),
    ],
)
def test_msys_click_compatibility_warning(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    installed_version: tuple[int, int],
    msystem: str | None,
    should_warn: bool,
) -> None:
    """Warn only when an older Click is used from Windows MSYS terminals."""
    monkeypatch.setattr(cli_main_module.sys, "platform", "win32")
    monkeypatch.setattr(cli_main_module, "_installed_click_version", lambda: installed_version)
    if msystem is None:
        monkeypatch.delenv("MSYSTEM", raising=False)
    else:
        monkeypatch.setenv("MSYSTEM", msystem)

    cli_main_module._warn_for_unsupported_msys_click()

    captured = capsys.readouterr()
    if should_warn:
        assert "Click <8.5" in captured.err
        assert "uv sync --extra dev" in captured.err
    else:
        assert captured.err == ""


def test_default_screen_preserves_logo_and_command_truecolor(runner: CliRunner) -> None:
    """Keep the default screen's logo gradient and command color as exact RGB ANSI."""
    result = runner.invoke(cli_group, [])
    assert result.exit_code == 0

    assert "\033[1;38;2;0;232;255m _____" in result.output
    assert "\033[1;38;2;121;82;245m|_____|" in result.output
    assert "\033[1;38;2;16;185;129mcolors-table" in result.output
    assert "\033[38;5;" not in result.output


def test_cli_info_command(runner: CliRunner) -> None:
    """Verify eigenscribe info presents a concise package and command overview."""
    result = runner.invoke(cli_group, ["info"])
    assert result.exit_code == 0
    plain = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "EIGENSCRIBE INFO" in plain
    assert f"Version: {CLI_VERSION}" in plain
    assert "COMMON COMMANDS" in plain
    assert "COLOR AND THEME SOURCES" in plain
    assert "COLOR_PALETTE" in plain


def test_cli_gradient_command(runner: CliRunner) -> None:
    """Verify eigenscribe gradient generates multi-stop gradient outputs."""
    res_default = runner.invoke(cli_group, ["gradient", "Testing Eigenscribe", "-p", "cyberpunk"])
    assert res_default.exit_code == 0
    assert "Testing Eigenscribe" in re.sub(r"\x1b\[[0-9;]*m", "", res_default.output)
    assert "\033[" in res_default.output

    res_stops = runner.invoke(cli_group, ["gradient", "Custom Stops", "-s", "#00ffff", "-s", "#ff00c3"])
    assert res_stops.exit_code == 0
    assert "Custom Stops" in re.sub(r"\x1b\[[0-9;]*m", "", res_stops.output)

    res_list = runner.invoke(cli_group, ["gradient", "--list-presets"])
    assert res_list.exit_code == 0
    plain_list = re.sub(r"\x1b\[[0-9;]*m", "", res_list.output)
    assert "GRADIENT PRESETS" in plain_list
    assert "electric" in plain_list
    assert "eigenscribe" in plain_list
    assert "aurora" in plain_list
    assert "#00e8ff" in plain_list
    assert "#008eff" in plain_list
    assert "#6f78fa" in plain_list
    assert "#5e17eb" in plain_list


def test_gradient_preset_preview_colors_only_the_swatch(runner: CliRunner) -> None:
    """Keep gradient colors confined to each preview swatch, not labels or stop codes."""
    result = runner.invoke(cli_group, ["gradient", "--list-presets"])
    assert result.exit_code == 0
    aurora_line = next(
        line
        for line in result.output.splitlines()
        if "aurora" in re.sub(r"\x1b\[[0-9;]*m", "", line)
    )

    plain_line = re.sub(r"\x1b\[[0-9;]*m", "", aurora_line)
    assert plain_line.startswith("  [aurora")
    assert "\033[1;38;2;6;182;212m" in aurora_line
    assert "\033[1;38;2;132;204;22m" in aurora_line
    assert plain_line.endswith("#06b6d4  #10b981  #84cc16")


def test_cli_colors_command(runner: CliRunner) -> None:
    """Verify eigenscribe colors displays canonical tokens and optional node spectrum."""
    result = runner.invoke(cli_group, ["colors", "--all-256", "--spectrum"])
    assert result.exit_code == 0
    plain = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "CANONICAL COLOR TOKENS" in plain
    assert "VIBRANT 10-NODE SPECTRUM" in plain
    assert "0. Divine White-Gold" in plain
    assert "9. Vivid Emerald Green" in plain
    for node in range(10):
        red, green, blue = hex_to_rgb(COLOR_PALETTE[f"node-{node}"])
        assert f"\033[48;2;{red};{green};{blue}m" in result.output


def test_cli_banner_command(runner: CliRunner) -> None:
    """Verify eigenscribe banner creates formatted rule-bordered banners."""
    result = runner.invoke(cli_group, ["banner", "MY EXPERIMENT", "--subtitle", "Trial Run 01"])
    assert result.exit_code == 0
    plain = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "MY EXPERIMENT" in plain
    assert "Trial Run 01" in plain
    assert "\033[1;38;2;" in result.output  # Styled with PRIMARY_GRADIENT


def test_cli_banner_uses_requested_preset_and_width(runner: CliRunner) -> None:
    """Use the selected gradient preset and width for the banner rule."""
    result = runner.invoke(
        cli_group,
        ["banner", "Aurora", "--preset", "aurora", "--width", "42"],
    )

    assert result.exit_code == 0
    assert "\033[1;38;2;6;182;212m" in result.output
    plain = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "─" * 42 in plain


def test_cli_theme_command(runner: CliRunner) -> None:
    """Verify eigenscribe theme exports summary, rcParams, and CSS variables."""
    res_summary = runner.invoke(cli_group, ["theme", "-f", "summary"])
    assert res_summary.exit_code == 0
    plain_summary = re.sub(r"\x1b\[[0-9;]*m", "", res_summary.output)
    assert "PLOTTING & GRAPHICS THEME" in plain_summary
    assert "Theme Engine Parameters" in plain_summary

    res_rc = runner.invoke(cli_group, ["theme", "-f", "rcparams"])
    assert res_rc.exit_code == 0
    assert "rcParams" in res_rc.output

    res_css = runner.invoke(cli_group, ["theme", "-f", "css"])
    assert res_css.exit_code == 0
    assert ":root {" in res_css.output
    assert "--color-" in res_css.output


def test_cli_mermaid_command(runner: CliRunner) -> None:
    """Verify eigenscribe mermaid generates diagrams and directives."""
    res_sample = runner.invoke(cli_group, ["mermaid", "--sample"])
    assert res_sample.exit_code == 0
    assert "flowchart TD" in res_sample.output

    res_init = runner.invoke(cli_group, ["mermaid", "--init"])
    assert res_init.exit_code == 0
    assert "%%{init:" in res_init.output


def test_cli_doctor_command(runner: CliRunner) -> None:
    """Verify eigenscribe doctor performs and passes all diagnostics."""
    result = runner.invoke(cli_group, ["doctor"])
    assert result.exit_code == 0
    plain = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "EIGENSCRIBE DOCTOR" in plain
    assert "[PASS]" in plain
    assert "checks passed successfully" in plain


def test_cli_colors_table_direct_command(runner: CliRunner) -> None:
    """Verify colors_table CLI prints table with colored swatches and names."""
    res = runner.invoke(colors_table_cli, [])
    assert res.exit_code == 0
    plain_output = re.sub(r"\x1b\[[0-9;]*m", "", res.output)
    assert "SCRIBER CORE COLOR PALETTE TABLE" in plain_output
    assert "\033[1;38;2;" in res.output or "\033[38;2;" in res.output
    assert "deep_pine" in res.output
    assert "node-1" in res.output
    assert "#00ffff" in res.output

    # Test sorting and formatting options
    res_sorted = runner.invoke(colors_table_cli, ["--sort", "name", "--reverse"])
    assert res_sorted.exit_code == 0
    assert "warning_amber" in res_sorted.output

    # Test style options
    res_ascii = runner.invoke(colors_table_cli, ["--style", "ascii", "--no-header"])
    assert res_ascii.exit_code == 0
    assert "|" in res_ascii.output

    # Test smoke-test flag
    res_smoke = runner.invoke(colors_table_cli, ["--smoke-test"])
    assert res_smoke.exit_code == 0
    assert "smoke tests passed" in res_smoke.output


def test_cli_colors_table_eigenscribe_integration(runner: CliRunner) -> None:
    """Verify eigenscribe colors --table displays the full COLOR_PALETTE table."""
    result = runner.invoke(cli_group, ["colors", "--table"])
    assert result.exit_code == 0
    plain_output = re.sub(r"\x1b\[[0-9;]*m", "", result.output)
    assert "SCRIBER CORE COLOR PALETTE TABLE" in plain_output
    assert "Rendered" in result.output
    assert "aurora_green" in plain_output
    assert "green_pond" in plain_output
    assert "sleeping_beauty" in plain_output


def test_colors_table_rendering_helpers() -> None:
    """Verify build_color_entries, swatch formatting, and table render functions."""
    entries = build_color_entries()
    assert len(entries) == len(COLOR_PALETTE)
    assert entries[0].index == 1

    swatch = format_color_swatch((0, 255, 255), width=6)
    assert "\033[38;2;0;255;255m██████\033[0m" == swatch

    colored_name = format_colored_name("pure_cyan", (0, 255, 255))
    assert "\033[1;38;2;0;255;255mpure_cyan\033[0m" == colored_name

    rendered = render_colors_table()
    plain_rendered = re.sub(r"\x1b\[[0-9;]*m", "", rendered)
    assert "SCRIBER CORE COLOR PALETTE TABLE" in plain_rendered
    assert run_cli_smoke_test() is True
