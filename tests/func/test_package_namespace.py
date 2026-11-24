"""Functional checks for the public Eigenscribe package and CLI launchers."""

from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path
import re
import subprocess
import sys

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PROJECT_ROOT / "src"


def _run_python(
    *arguments: str,
    extra_env: dict[str, str] | None = None,
    set_utf8_encoding: bool = True,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(SOURCE_ROOT) + (
        os.pathsep + existing_pythonpath if existing_pythonpath else ""
    )
    env["PYTHONIOENCODING"] = "utf-8"
    if extra_env:
        env.update(extra_env)
    if not set_utf8_encoding:
        env.pop("PYTHONIOENCODING", None)
    return subprocess.run(
        [sys.executable, *arguments],
        cwd=PROJECT_ROOT,
        env=env,
        check=False,
        capture_output=True,
        encoding="utf-8",
        text=True,
    )


def test_eigenscribe_namespace_imports() -> None:
    result = _run_python(
        "-c",
        "import importlib.metadata as metadata; import importlib.util; import eigenscribe; "
        "from eigenscribe import cli, frontend; from eigenscribe.cli.branding import CLI_VERSION; "
        "assert importlib.util.find_spec('scriber_core') is None; "
        "assert eigenscribe.__version__ == frontend.__version__ == CLI_VERSION; "
        "assert metadata.version('scriber-core') == eigenscribe.__version__; "
        "assert cli.__all__; assert frontend.__all__",
    )

    assert result.returncode == 0, result.stderr


def test_distribution_declares_eigenscribe_console_script() -> None:
    distribution = importlib.metadata.distribution("scriber-core")
    entry_points = {
        entry_point.name: entry_point.value
        for entry_point in distribution.entry_points
        if entry_point.group == "console_scripts"
    }

    assert entry_points["eigenscribe"] == "eigenscribe.cli.main:main"


def test_distribution_requires_click_with_truecolor_safe_windows_output() -> None:
    distribution = importlib.metadata.distribution("scriber-core")
    requirements = distribution.requires or []

    assert any(requirement.lower().startswith("click>=8.5") for requirement in requirements)


def test_top_level_module_launcher() -> None:
    result = _run_python("-m", "eigenscribe", "--help")

    assert result.returncode == 0, result.stderr
    assert "Eigenscribe CLI" in result.stdout


def test_cli_module_launcher() -> None:
    result = _run_python("-m", "eigenscribe.cli", "--help")

    assert result.returncode == 0, result.stderr
    assert "Eigenscribe CLI" in result.stdout


def test_direct_gradient_module_runs_smoke_test_with_truecolor() -> None:
    script = SOURCE_ROOT / "eigenscribe" / "frontend" / "gradients.py"
    result = _run_python(str(script))

    assert result.returncode == 0, result.stderr
    assert "gradients.py smoke tests passed" in result.stdout
    assert "\033[1;38;2;" in result.stdout or "\033[38;2;" in result.stdout


def test_direct_messaging_module_runs_smoke_test_with_truecolor() -> None:
    script = SOURCE_ROOT / "eigenscribe" / "cli" / "messaging.py"
    result = _run_python(str(script))

    assert result.returncode == 0, result.stderr
    assert "messaging.py smoke tests passed" in result.stdout
    assert "\033[1;38;2;" in result.stdout or "\033[38;2;" in result.stdout


def test_cli_gradient_command_emits_truecolor() -> None:
    result = _run_python("-m", "eigenscribe", "gradient", "TrueColor smoke")

    assert result.returncode == 0, result.stderr
    plain_output = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
    assert "TrueColor smoke" in plain_output
    assert "\033[1;38;2;" in result.stdout


def test_default_cli_preserves_logo_and_command_truecolor_in_subprocess() -> None:
    result = _run_python("-m", "eigenscribe", extra_env={"TERM": "xterm-256color"})

    assert result.returncode == 0, result.stderr
    assert "\033[1;38;2;0;232;255m _____" in result.stdout
    assert "\033[1;38;2;121;82;245m|_____|" in result.stdout
    assert "\033[1;38;2;16;185;129mcolors-table" in result.stdout
    assert "\033[38;5;" not in result.stdout


@pytest.mark.skipif(sys.platform != "win32", reason="Windows MSYS pipe handling only")
def test_msys_subprocess_preserves_utf8_and_truecolor_without_encoding_override() -> None:
    result = _run_python(
        "-m",
        "eigenscribe",
        extra_env={"MSYSTEM": "UCRT64"},
        set_utf8_encoding=False,
    )

    assert result.returncode == 0, result.stderr
    assert "🔱" in result.stdout
    assert "\033[1;38;2;0;232;255m _____" in result.stdout
    assert "\033[1;38;2;121;82;245m|_____|" in result.stdout
    assert "\033[1;38;2;16;185;129mcolors-table" in result.stdout
    assert "\033[38;5;" not in result.stdout