"""S+7 swap: determinism, wraparound, and case/punctuation preservation."""

from __future__ import annotations

import yaml

from oulipo_memory_deck.swap import load_dictionary, swap


def test_swap_is_pure_and_deterministic(repo_root):
    words, _version, _sha = load_dictionary("common-nouns-v1", repo_root)
    line = "the kettle sits on the stove."
    a = swap(line, words)
    b = swap(line, words)
    assert a == b
    assert a == "the drawer sits on the spoon."


def test_swap_wraps_modulo_dictionary_length():
    # ten-noun fixture: index N maps to (N+7) % 10
    tiny = ["cup", "plate", "bowl", "fork", "knife",
            "candle", "book", "pen", "chair", "table"]
    # cup is at index 0 -> dictionary[7] = pen
    assert swap("cup", tiny) == "pen"
    # table at index 9 -> dictionary[(9+7) % 10] = dictionary[6] = book
    assert swap("table", tiny) == "book"


def test_swap_preserves_trailing_punctuation():
    tiny = ["cup", "plate", "bowl", "fork", "knife",
            "candle", "book", "pen", "chair", "table"]
    assert swap("cup,", tiny) == "pen,"
    assert swap("cup.", tiny) == "pen."
    assert swap("(cup)", tiny) == "(pen)"


def test_swap_preserves_casing():
    tiny = ["cup", "plate", "bowl", "fork", "knife",
            "candle", "book", "pen", "chair", "table"]
    assert swap("Cup", tiny) == "Pen"
    assert swap("CUP", tiny) == "PEN"
    assert swap("cup", tiny) == "pen"


def test_swap_passes_through_unknown_tokens():
    tiny = ["cup", "plate", "bowl"]
    # 'the' and 'sits' are not in dict and pass through
    # cup at idx 0 -> (0+7)%3 = 1 -> plate
    assert swap("the cup sits", tiny) == "the plate sits"


def test_swap_walks_full_deck_for_every_card(repo_root):
    """determinism check: every committed card's s_plus_7_line matches
    the live output of swap() against the committed dictionary."""
    words, _version, _sha = load_dictionary("common-nouns-v1", repo_root)
    cards_dir = repo_root / "cards" / "objects"
    files = sorted(cards_dir.glob("*.yaml"))
    assert len(files) == 8
    for path in files:
        card = yaml.safe_load(path.read_text(encoding="utf-8"))
        produced = swap(card["base_line"], words)
        assert produced == card["s_plus_7_line"], (
            f"{path.name}: stored={card['s_plus_7_line']!r} "
            f"produced={produced!r}"
        )


def test_dictionary_sha256_is_stable(repo_root):
    """two reads of the dictionary produce the same sha."""
    _w1, _v1, sha1 = load_dictionary("common-nouns-v1", repo_root)
    _w2, _v2, sha2 = load_dictionary("common-nouns-v1", repo_root)
    assert sha1 == sha2
    assert len(sha1) == 64
