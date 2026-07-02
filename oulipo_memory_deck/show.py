"""show the committed deck as a readable, ranked table.

read-only, offline. reads cards/objects/*.yaml and the committed
dictionary, recomputes how many nouns each card's base line swaps,
and prints a table ranked by swap count (most-transformed first)
plus a one-line headline finding.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from .swap import load_dictionary, swap


def _swap_count(base_line: str, dictionary: list[str]) -> int:
    """how many whitespace tokens change when S+7 is applied."""
    if not dictionary:
        return 0
    before = base_line.split()
    after = swap(base_line, dictionary).split()
    return sum(1 for a, b in zip(before, after) if a != b)


def load_rows(root: Path) -> list[dict]:
    """return one row per card, ranked by swap count (desc), then id."""
    cards_dir = root / "cards" / "objects"
    files = sorted(cards_dir.glob("*.yaml"))
    dict_cache: dict[str, list[str]] = {}
    rows: list[dict] = []
    for path in files:
        card = yaml.safe_load(path.read_text(encoding="utf-8"))
        # a hand-edited card can drop a required key; name the file so the
        # reader edits the right one instead of chasing a raw KeyError.
        try:
            did = card["dictionary_id"]
            if did not in dict_cache:
                dict_cache[did], _ver, _sha = load_dictionary(did, root)
            dictionary = dict_cache[did]
            rows.append(
                {
                    "object": card["object"],
                    "base_line": card["base_line"],
                    "s_plus_7_line": card["s_plus_7_line"],
                    "vignette": card["vignette"],
                    "swaps": _swap_count(card["base_line"], dictionary),
                    "vignette_words": len(card["vignette"].split()),
                }
            )
        except (KeyError, TypeError) as exc:
            raise ValueError(f"{path.name}: missing key {exc}") from exc
    rows.sort(key=lambda r: (-r["swaps"], r["object"]))
    return rows


def show(root: Path) -> int:
    try:
        rows = load_rows(root)
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1
    if not rows:
        print("no cards found in cards/objects/")
        return 1

    total_swaps = sum(r["swaps"] for r in rows)
    most = rows[0]

    print("oulipo memory deck -- 8 cards, ranked by S+7 transform")
    print()
    header = f"{'rank':>4}  {'object':<8}  {'swaps':>5}  {'words':>5}  s+7 line"
    print(header)
    print("-" * len(header))
    for i, r in enumerate(rows, 1):
        line = r["s_plus_7_line"]
        if len(line) > 42:
            line = line[:39] + "..."
        print(
            f"{i:>4}  {r['object']:<8}  {r['swaps']:>5}  "
            f"{r['vignette_words']:>5}  {line}"
        )

    print()
    print(
        f"finding: '{most['object']}' is the most-transformed card "
        f"({most['swaps']} nouns swapped); the deck swaps {total_swaps} "
        f"nouns across {len(rows)} cards."
    )
    print()
    print("most-transformed card:")
    print(f"  base: {most['base_line']}")
    print(f"  s+7:  {most['s_plus_7_line']}")
    return 0
