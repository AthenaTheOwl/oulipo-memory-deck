# status

## Current state

v0.1 ships a complete, locally-runnable deck.

- 8 starter cards in `cards/objects/`: kettle, hinge, key, lamp,
  mirror, radio, spoon, window. each card has `id`, `object`,
  `base_line`, `s_plus_7_line`, `vignette` (40-80 words),
  `dictionary_id`, `dictionary_version`.
- `schemas/card.schema.json` (draft 2020-12) is the source of truth
  for card shape; `additionalProperties: false`.
- `dictionaries/common-nouns.txt` is a 40-noun curated list pinned at
  `common-nouns-v1`. `dictionaries/INDEX.json` records the version and
  provenance.
- `oulipo_memory_deck.swap.swap()` is a pure function. the tokenizer
  is documented inline.
- `python -m oulipo_memory_deck validate` (no args) validates all 8
  cards against the schema, re-runs the S+7 swap, and checks the
  vignette word-count gate. exits zero on a clean deck.
- `python -m oulipo_memory_deck render --out generated/print.html`
  produces one static html page with all eight cards.
- tests cover schema validity, swap determinism + wraparound +
  casing, render output shape, and a no-network invariant
  (source-level grep + socket monkeypatch).

## Known limits

- the dictionary is 40 nouns -- big enough for the eight base lines,
  small enough for a human to read in one screen. it is not the
  ~1200-noun list anticipated in `docs/first-pr.md`; expanding it
  later requires a `v2` tag because committed card `s_plus_7_line`
  values are reproducible only against the dictionary they were
  computed under.
- tokenization is exact-membership only. plurals, compounds, and
  proper nouns are out-of-scope for the parser; they are handled by
  curating the dictionary, per the design spec.
- no print-friendly card layout beyond the single-page html. the
  `@media print` rule emits one card per page but does not lay out
  fronts/backs.
- `dictionaries/INDEX.json` does not pin a sha256 for the v1 file in
  v0.1. the loader computes the sha at read time and surfaces it; a
  future change can pin it without touching the swap algorithm.
- the validator does not yet enforce the portfolio-wide voice spec on
  card prose (spec 0001 R-OMD-009 -- planned for a later spec).

## Next feature queue

- pin the `common-nouns-v1` sha256 in `INDEX.json` and assert it in
  the test suite.
- add `scripts/voice_lint.py` and `scripts/spec_check.py` per
  R-OMD-009 so the portfolio voice gates run against the cards.
- expand the dictionary to ~1200 nouns and tag it `common-nouns-v2`;
  add a second deck pinned at v2 to demonstrate the version
  discipline.
- add a `--card <id>` flag to `validate` for fast single-card checks.
- ship a print-and-play layout (two-up landscape) as a second render
  target alongside `print.html`.

- Resolve factory defect: expected file 'specs/0002-design/requirements.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/design.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/tasks.md' is missing
- Resolve factory defect: expected file 'specs/0002-design/acceptance.md' is missing
- Resolve factory defect: module 'transform' declares source 'oulipo_memory_deck/transform.py', but it is missing
- Resolve factory defect: claude_code review requested patch; inspect defect log
