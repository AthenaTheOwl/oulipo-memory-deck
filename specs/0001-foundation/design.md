# Spec 0001 — Design

## Shape

A schema, a dictionary, a swap script, a renderer, a static HTML
page. The whole repo is small enough to read in one sitting.

```
schemas/card.schema.json    # R-OMD-002
dictionaries/
  common-nouns.txt          # R-OMD-004
cards/objects/
  kettle.yaml               # R-OMD-003
  hinge.yaml
  key.yaml
  lamp.yaml
  mirror.yaml
  radio.yaml
  spoon.yaml
  window.yaml
scripts/
  s_plus_7.py               # R-OMD-005, R-OMD-006
  render_html.py            # R-OMD-007
  validate_cards.py         # R-OMD-008
  voice_lint.py             # R-OMD-009
  spec_check.py             # R-OMD-009
templates/
  index.html                # card list layout
tests/
  test_swap_determinism.py
  test_swap_wraparound.py
  test_validate_cards.py
  test_no_network.py
```

## S+7 algorithm

Given a base line and a dictionary:

1. Tokenize the line (whitespace + punctuation aware).
2. For each token, decide if it is a noun via a small rule set:
   the token (case-normalized, stripped of trailing punctuation)
   appears in the dictionary.
3. For each noun token, compute its dictionary index, add 7,
   wrap modulo dictionary length, look up the replacement.
4. Preserve original capitalization and trailing punctuation on the
   replacement token.
5. Reassemble.

The algorithm is intentionally simple. Edge cases (plurals,
compound nouns, proper nouns) are handled by curating the dictionary
rather than by parser heuristics.

## Dictionary discipline

The dictionary file is a versioned artifact. Card files carry
`dictionary_id` and `dictionary_version`. A change to the dictionary
that would alter an existing card's `s_plus_7_line` requires a new
version tag and a re-render. The determinism gate (R-OMD-006) is the
contract that catches drift.

## Rendering

`render_html.py` produces one `index.html` with all eight cards in
sequence. The layout shows base line in muted type, S+7 line in
bold, vignette below. No JavaScript. No external assets. The page
works offline and prints cleanly.

## Why no model in the loop

The literary constraint is the point. If a model writes the
vignettes, the constraint becomes ornamental rather than load-
bearing. The user hand-writes every vignette using the S+7 line as a
seed; the repo provides the seed and the page, nothing more.

## What is not in spec 0001

- Print-and-play card layout (the HTML page is the artifact).
- Multi-language dictionaries.
- Card decks beyond the initial eight.
- Any model integration.

Spec 0002 lands the dictionary + the first 4 cards end-to-end.
