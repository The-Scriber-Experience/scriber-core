"""Tests for Windows console virtual-terminal initialization."""

from __future__ import annotations

import sys
from types import SimpleNamespace

import pytest

from eigenscribe.cli import vt_mode


class _FakeFunction:
    def __init__(self, result: int) -> None:
        self.result = result
        self.argtypes: list[object] | None = None
        self.restype: object | None = None
        self.calls: list[tuple[object, ...]] = []

    def __call__(self, *args: object) -> int:
        self.calls.append(args)
        if len(args) > 1 and hasattr(args[1], "value"):
            args[1].value = 0x0001
        return self.result


class _FakeDword:
    def __init__(self, value: int = 0) -> None:
        self.value = value


def test_enable_vt_mode_is_noop_off_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """Do not touch console APIs on non-Windows systems."""
    monkeypatch.setattr(vt_mode.sys, "platform", "linux")

    assert vt_mode.enable_vt_mode() is None


@pytest.mark.parametrize(
    ("msystem", "pythonioencoding", "file_type", "expected_reconfigure"),
    [
        ("UCRT64", None, 3, True),
        ("UCRT64", "cp1252", 3, False),
        ("UCRT64", None, 1, False),
        (None, None, 3, False),
    ],
)
def test_enable_vt_mode_configures_utf8_only_for_msys_pipes(
    monkeypatch: pytest.MonkeyPatch,
    msystem: str | None,
    pythonioencoding: str | None,
    file_type: int,
    expected_reconfigure: bool,
) -> None:
    """Use UTF-8 for MSYS pipes, but preserve explicit encodings and file redirects."""
    get_std_handle = _FakeFunction(1234)
    get_console_mode = _FakeFunction(0)
    get_file_type = _FakeFunction(file_type)
    set_console_mode = _FakeFunction(1)
    reconfigure_calls: list[dict[str, str]] = []
    kernel32 = SimpleNamespace(
        GetStdHandle=get_std_handle,
        GetConsoleMode=get_console_mode,
        GetFileType=get_file_type,
        SetConsoleMode=set_console_mode,
    )
    fake_ctypes = SimpleNamespace(
        windll=SimpleNamespace(kernel32=kernel32),
        byref=lambda value: value,
        POINTER=lambda value_type: ("pointer", value_type),
        wintypes=SimpleNamespace(DWORD=_FakeDword, HANDLE=object(), BOOL=object()),
    )
    monkeypatch.setitem(sys.modules, "ctypes", fake_ctypes)
    monkeypatch.setattr(vt_mode.sys, "platform", "win32")
    monkeypatch.setattr(
        vt_mode.sys,
        "stdout",
        SimpleNamespace(reconfigure=lambda **kwargs: reconfigure_calls.append(kwargs)),
    )
    if msystem is None:
        monkeypatch.delenv("MSYSTEM", raising=False)
    else:
        monkeypatch.setenv("MSYSTEM", msystem)
    if pythonioencoding is None:
        monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    else:
        monkeypatch.setenv("PYTHONIOENCODING", pythonioencoding)

    assert vt_mode.enable_vt_mode() is None

    assert get_file_type.calls == ([(1234,)] if msystem else [])
    expected_calls = [{"encoding": "utf-8", "errors": "replace"}] if expected_reconfigure else []
    assert reconfigure_calls == expected_calls


@pytest.mark.parametrize(("console_mode_result", "set_mode_calls"), [(1, 1), (0, 0)])
def test_enable_vt_mode_uses_pointer_sized_console_handle(
    monkeypatch: pytest.MonkeyPatch,
    console_mode_result: int,
    set_mode_calls: int,
) -> None:
    """Set VT on a real console handle and leave redirected streams alone."""
    get_std_handle = _FakeFunction(1234)
    get_console_mode = _FakeFunction(console_mode_result)
    set_console_mode = _FakeFunction(1)
    get_file_type = _FakeFunction(0)
    reconfigure_calls: list[dict[str, str]] = []
    kernel32 = SimpleNamespace(
        GetStdHandle=get_std_handle,
        GetConsoleMode=get_console_mode,
        GetFileType=get_file_type,
        SetConsoleMode=set_console_mode,
    )
    handle_type = object()
    bool_type = object()
    fake_ctypes = SimpleNamespace(
        windll=SimpleNamespace(kernel32=kernel32),
        byref=lambda value: value,
        POINTER=lambda value_type: ("pointer", value_type),
        wintypes=SimpleNamespace(DWORD=_FakeDword, HANDLE=handle_type, BOOL=bool_type),
    )
    monkeypatch.setitem(sys.modules, "ctypes", fake_ctypes)
    monkeypatch.setattr(vt_mode.sys, "platform", "win32")
    monkeypatch.delenv("MSYSTEM", raising=False)
    monkeypatch.delenv("PYTHONIOENCODING", raising=False)
    monkeypatch.setattr(
        vt_mode.sys,
        "stdout",
        SimpleNamespace(reconfigure=lambda **kwargs: reconfigure_calls.append(kwargs)),
    )

    assert vt_mode.enable_vt_mode() is None

    assert get_std_handle.restype is handle_type
    assert get_std_handle.argtypes == [_FakeDword]
    assert get_std_handle.calls == [(-11,)]
    assert get_console_mode.argtypes == [handle_type, ("pointer", _FakeDword)]
    assert set_console_mode.argtypes == [handle_type, _FakeDword]
    assert get_console_mode.restype is bool_type
    assert set_console_mode.restype is bool_type
    assert len(set_console_mode.calls) == set_mode_calls
    assert len(reconfigure_calls) == set_mode_calls
    if set_mode_calls:
        assert set_console_mode.calls[0][1] == 0x0005