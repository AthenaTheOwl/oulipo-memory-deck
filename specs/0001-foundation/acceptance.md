# Spec 0001 — Acceptance

v0 is done when the following hold.

## Repo shape

- README, LICENSE, AGENTS.md, .gitignore at the root.
- `specs/0001-foundation/` complete.
- `docs/first-pr.md` concrete and file-level.

## Commands

After PR 1-3 land:

```bash
python scripts/validate_cards.py
python scripts/s_plus_7.py --check-determinism
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/render_html.py --out generated/index.html
```

All five exit zero.

## Functional gates

- Exactly 8 card YAMLs in `cards/objects/` (R-OMD-003).
- Each card's `s_plus_7_line` matches the live output of the swap
  script against `dictionaries/common-nouns.txt` v1 (R-OMD-006).
- Each card's `vignette` is between 40 and 80 words inclusive
  (R-OMD-008).
- The rendered `index.html` opens locally in a browser without
  external network requests.
- `tests/test_no_network.py` confirms `s_plus_7.py` and
  `render_html.py` make no socket calls (R-OMD-010).
- `spec_check.py` confirms every `R-OMD-NNN` reference is defined.

## Out of scope for v0 acceptance

- Card layout for printing.
- Additional dictionary versions.
- Card decks beyond the initial eight.
- Any model API.

Those are not planned.
