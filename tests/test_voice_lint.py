from __future__ import annotations

from oulipo_memory_deck.voice_lint import lint_card, lint_markdown


def _clean_card() -> dict[str, str]:
    return {
        "base_line": "the kettle sits on the stove.",
        "vignette": "the drawer sits on the spoon. the cup rests by the sink.",
    }


def test_clean_card_has_no_voice_lint_hits():
    assert lint_card(_clean_card()) == []


def test_marketing_word_is_flagged():
    card = _clean_card()
    card["vignette"] = "the drawer can leverage the spoon."
    assert any("leverage" in error for error in lint_card(card))


def test_capitalized_acronym_is_flagged_in_card_fields():
    card = _clean_card()
    card["base_line"] = "the DNA card sits on the stove."
    assert any("DNA" in error for error in lint_card(card))


def test_internal_reference_list_is_flagged():
    card = _clean_card()
    card["vignette"] = "the drawer sits near Acme Launch."
    errors = lint_card(card, internal_references=("Acme Launch",))
    assert any("Acme Launch" in error for error in errors)


def test_markdown_title_case_heading_is_flagged():
    errors = lint_markdown("# Design Notes\n\nplain text")
    assert any("heading" in error for error in errors)
