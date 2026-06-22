# Spec 0002 — Design iteration

This spec covers the next pass after foundation: pinning the
dictionary, expanding it, and wiring the portfolio-wide voice gates
against card prose. Foundation (spec 0001) shipped 8 cards, the
schema, the swap, the renderer, and a small curated dictionary.
0002 is about discipline around those artifacts.

## R-OMD-101 — pinned dictionary sha256
`dictionaries/INDEX.json` MUST carry a `sha256` field for every
dictionary entry. The loader MUST refuse to load a dictionary whose
on-disk LF-normalized utf-8 sha256 does not match the pinned value.
Mismatch is a hard error, not a warning.

## R-OMD-102 — voice lint on prose surfaces
`scripts/voice_lint.py` (or an in-package equivalent) MUST flag
marketing language, sentence-case headings turning into title-case,
and capitalized acronyms in `base_line` / `vignette` fields. The
gate runs as part of `python -m oulipo_memory_deck validate`.

## R-OMD-103 — spec_check
`scripts/spec_check.py` (or an in-package equivalent) MUST verify
that every `R-OMD-NNN` referenced in `design.md` or `tasks.md` is
defined in the `requirements.md` of the same spec slug.

## R-OMD-104 — dictionary v2
`dictionaries/common-nouns.txt` MAY be retired in favor of a v2 file
with broader coverage (~1200 nouns) at a new tag
`common-nouns-v2`. Existing cards remain pinned at `v1`. New cards
declare `dictionary_version: v2` and are validated against the new
file. The swap algorithm itself does not change.

## R-OMD-105 — print-and-play layout
A second render target (e.g. `python -m oulipo_memory_deck render
--layout print-and-play`) emits a two-up landscape page with
card-back placeholders so the deck can be cut and folded. No
JavaScript, no external assets, prints cleanly from a browser.

## R-OMD-106 — single-card validation
`python -m oulipo_memory_deck validate --card <id>` validates a
single card by id. Useful while authoring new vignettes; the no-args
default still validates every card.
