# Spec 0002 — Acceptance

Spec 0002 is done when the following hold.

## Pinned dictionary

- `dictionaries/INDEX.json` has a `sha256` field for every registered
  dictionary.
- `oulipo_memory_deck.transform.load_dictionary` raises on sha
  mismatch.
- A test in `tests/` recomputes the sha of every dictionary file and
  asserts equality against `INDEX.json`.

## Voice + spec gates

- `python -m oulipo_memory_deck validate` runs the voice rules over
  every card's `base_line` and `vignette` and exits non-zero on a
  violation.
- `spec_check` exits zero against `specs/0001-foundation/` and
  `specs/0002-design/`.

## Dictionary v2 (when shipped)

- `dictionaries/common-nouns-v2.txt` is committed with its sha
  pinned in `INDEX.json`.
- At least one card declares `dictionary_version: v2` and validates.
- All existing v1 cards continue to validate against v1.

## Print-and-play (when shipped)

- `python -m oulipo_memory_deck render --layout print-and-play
  --out generated/print-and-play.html` produces a static page.
- The page opens locally in a browser, makes no network requests,
  and prints two cards per landscape sheet.

## Out of scope for spec 0002

- Multi-language dictionaries.
- A web UI for editing cards.
- Any model API.
