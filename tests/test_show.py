"""show: ranked, readable, read-only table of the committed deck."""

from __future__ import annotations

from oulipo_memory_deck.show import load_rows, show


def test_load_rows_one_per_card_ranked(repo_root):
    rows = load_rows(repo_root)
    assert len(rows) == 8
    # ranked by swap count descending
    swaps = [r["swaps"] for r in rows]
    assert swaps == sorted(swaps, reverse=True)
    for r in rows:
        assert r["swaps"] >= 1
        assert 40 <= r["vignette_words"] <= 80
        assert r["base_line"] != r["s_plus_7_line"]


def test_show_exits_zero_and_prints_table(repo_root, capsys):
    code = show(repo_root)
    assert code == 0
    out = capsys.readouterr().out
    assert "oulipo memory deck" in out
    assert "rank" in out and "object" in out and "swaps" in out
    assert "finding:" in out
    # every object appears in the table
    for obj in ("kettle", "hinge", "key", "lamp",
                "mirror", "radio", "spoon", "window"):
        assert obj in out
