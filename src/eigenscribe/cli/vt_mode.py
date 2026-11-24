"""
vt_mode.py

Windows Virtual Terminal (VT) mode enablement for the Eigenscribe CLI.
Provides a function to enable ANSI/VT100 escape sequence support on Windows
consoles. Called at CLI invocation time, not at import time, to avoid side
effects during module loading.

The conceptual story follows the Eigenscribe architectural standard:
What exists -> What you're allowed to call -> How it works -> Proof it works.

Author: Eigenscribe & Scriber Labs
Date: November 19, 2026
"""

from __future__ import annotations

import os
import sys


__all__: list[str] = [
    "enable_vt_mode",
    "run_smoke_test",
]


# -----------------------------------------------------------------------------------------------------------
# 2️⃣ Public API (functions users are meant to call)
# -----------------------------------------------------------------------------------------------------------


def enable_vt_mode() -> None:
    """Enable ANSI/VT100 Virtual Terminal Processing on Windows consoles.

    The ctypes API declarations use Windows pointer-sized handles and DWORD
    console modes. Redirected streams are left unchanged when they do not have
    an associated console.

    On non-Windows platforms, this is a no-op.
    """
    if sys.platform != "win32":
        return

    # Configure the console API signatures before passing handles or mode pointers.
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32
        kernel32.GetStdHandle.argtypes = [wintypes.DWORD]
        kernel32.GetStdHandle.restype = wintypes.HANDLE
        kernel32.GetConsoleMode.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
        kernel32.GetConsoleMode.restype = wintypes.BOOL
        kernel32.GetFileType.argtypes = [wintypes.HANDLE]
        kernel32.GetFileType.restype = wintypes.DWORD
        kernel32.SetConsoleMode.argtypes = [wintypes.HANDLE, wintypes.DWORD]
        kernel32.SetConsoleMode.restype = wintypes.BOOL

        handle = kernel32.GetStdHandle(-11)
        mode = wintypes.DWORD()
        if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
            kernel32.SetConsoleMode(handle, mode.value | 0x0004)
            _configure_stdout_encoding()
        elif os.environ.get("MSYSTEM") and kernel32.GetFileType(handle) == 0x0003:
            _configure_stdout_encoding()
    except Exception:
        pass


def _configure_stdout_encoding() -> None:
    """Use UTF-8 unless the user explicitly selected a Python I/O encoding."""
    if "PYTHONIOENCODING" in os.environ or not hasattr(sys.stdout, "reconfigure"):
        return

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


# -----------------------------------------------------------------------------------------------------------
# 4️⃣ 💨 Smoke tests / example usage (proof it works)
# -----------------------------------------------------------------------------------------------------------


def run_smoke_test() -> bool:
    """Validate that VT mode enablement runs without error.

    Returns
    -------
    bool
        True if enable_vt_mode() completes without raising.
    """
    print("💨 Running src/eigenscribe/cli/vt_mode.py smoke tests...")

    # Verify enable_vt_mode does not raise
    enable_vt_mode()

    # Verify platform detection
    assert sys.platform in ("win32", "linux", "darwin"), f"Unexpected platform: {sys.platform!r}"

    print("✅ src/eigenscribe/cli/vt_mode.py smoke tests passed successfully.\n")
    return True


# -----------------------------------------------------------------------------------------------------------
# 🔥 Entry point
# -----------------------------------------------------------------------------------------------------------


def main() -> None:
    """Orchestrate VT mode smoke test output."""
    success = run_smoke_test()
    if not success:
        raise ValueError("VT mode validation failed during smoke test checks.")


if __name__ == "__main__":
    main()
