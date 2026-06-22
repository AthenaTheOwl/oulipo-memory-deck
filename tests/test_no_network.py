"""R-OMD-010: the deck refuses to open sockets.

defense in depth:
1. source-level grep -- no network-related imports anywhere in the
   oulipo_memory_deck package.
2. runtime monkeypatch -- replace socket.socket and assert no instance
   is created while running swap + render + validate paths.
"""

from __future__ import annotations

import socket
from pathlib import Path

import pytest

from oulipo_memory_deck.render import render_all
from oulipo_memory_deck.swap import load_dictionary, swap
from oulipo_memory_deck.validate import validate_all


FORBIDDEN_IMPORTS = ("urllib", "requests", "http.client", "socket")


def test_package_source_has_no_network_imports(repo_root):
    pkg_dir = repo_root / "oulipo_memory_deck"
    offenders = []
    for path in pkg_dir.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        for needle in FORBIDDEN_IMPORTS:
            if f"import {needle}" in text:
                offenders.append((path.name, needle))
            if f"from {needle}" in text:
                offenders.append((path.name, needle))
    assert offenders == [], f"network imports leaked in: {offenders}"


def test_swap_opens_no_sockets(repo_root, monkeypatch):
    def _boom(*a, **kw):
        raise AssertionError("socket.socket() called -- no network allowed")

    monkeypatch.setattr(socket, "socket", _boom)
    words, _v, _s = load_dictionary("common-nouns-v1", repo_root)
    out = swap("the kettle sits on the stove.", words)
    assert out == "the drawer sits on the spoon."


def test_render_opens_no_sockets(repo_root, tmp_path: Path, monkeypatch):
    def _boom(*a, **kw):
        raise AssertionError("socket.socket() called -- no network allowed")

    monkeypatch.setattr(socket, "socket", _boom)
    out = tmp_path / "print.html"
    code = render_all(repo_root, out)
    assert code == 0


def test_validate_opens_no_sockets(repo_root, monkeypatch, capsys):
    def _boom(*a, **kw):
        raise AssertionError("socket.socket() called -- no network allowed")

    monkeypatch.setattr(socket, "socket", _boom)
    code = validate_all(repo_root)
    assert code == 0
