"""render: produces a single static print.html with all cards inline."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from oulipo_memory_deck.render import render_all, render_deck


def test_render_deck_returns_html_with_all_cards(repo_root):
    cards_dir = repo_root / "cards" / "objects"
    cards = [yaml.safe_load(p.read_text(encoding="utf-8"))
             for p in sorted(cards_dir.glob("*.yaml"))]
    html = render_deck(cards)
    assert "<!doctype html>" in html
    assert "oulipo memory deck" in html
    for card in cards:
        assert card["base_line"] in html
        assert card["s_plus_7_line"] in html
        # vignette appears in normalized form
        vignette_first_word = card["vignette"].split()[0]
        assert vignette_first_word in html


def test_render_writes_print_html(tmp_path: Path, repo_root):
    out = tmp_path / "print.html"
    code = render_all(repo_root, out)
    assert code == 0
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    # eight cards rendered, each in its own section
    sections = re.findall(r'<section class="card"', text)
    assert len(sections) == 8


def test_render_html_has_no_external_assets(tmp_path: Path, repo_root):
    out = tmp_path / "print.html"
    render_all(repo_root, out)
    text = out.read_text(encoding="utf-8")
    # no <script>, <link rel="stylesheet">, <img src="http">
    assert "<script" not in text.lower()
    assert "stylesheet" not in text.lower()
    assert "http://" not in text
    assert "https://" not in text
