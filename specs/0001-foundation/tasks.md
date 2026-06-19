# Spec 0001 — Tasks

Ordered for the first 2-3 PRs.

## PR 1 — schema, dictionary, swap script

- [ ] Write `schemas/card.schema.json` (R-OMD-002).
- [ ] Commit `dictionaries/common-nouns.txt` v1 (R-OMD-004).
- [ ] Write `scripts/s_plus_7.py` (R-OMD-005) — pure function plus
      `--check-determinism` mode (R-OMD-006).
- [ ] Write `tests/test_swap_determinism.py` and
      `tests/test_swap_wraparound.py`.
- [ ] Write `tests/test_no_network.py` (R-OMD-010).

## PR 2 — first 4 cards + renderer

- [ ] Write `cards/objects/kettle.yaml`, `hinge.yaml`, `key.yaml`,
      `lamp.yaml`.
- [ ] Each card's `s_plus_7_line` produced by running
      `s_plus_7.py` and committed.
- [ ] Each vignette hand-written, 40-80 words.
- [ ] Write `templates/index.html`.
- [ ] Write `scripts/render_html.py` (R-OMD-007).
- [ ] Write `scripts/validate_cards.py` (R-OMD-008).
- [ ] Render the page and confirm it opens cleanly in a browser.

## PR 3 — remaining 4 cards + voice gates

- [ ] Add `mirror.yaml`, `radio.yaml`, `spoon.yaml`, `window.yaml`.
- [ ] Copy `scripts/voice_lint.py` from portfolio (R-OMD-009).
- [ ] Write `scripts/spec_check.py` (R-OMD-009).
- [ ] All gates exit zero against all 8 cards.
- [ ] Final `index.html` committed (or build instructions confirmed
      to produce it locally).
