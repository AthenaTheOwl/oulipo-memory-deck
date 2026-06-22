# oulipo memory deck

a tiny narrative deck. eight everyday objects -- kettle, hinge, key,
lamp, mirror, radio, spoon, window -- become memory cards. each
card's base line is run through an oulipo s+7 word swap to expose
buried history, and the user writes a 40-80 word vignette using the
uncanny output as a seed.

the artifact is a single static html page. no javascript, no external
assets, no model in the loop.

## the s+7 swap

given a base line and a dictionary, replace every noun with the noun
seven entries later in the dictionary, wrapping at the end. non-noun
tokens (and tokens not in the dictionary) pass through unchanged.
casing and trailing punctuation are preserved. the algorithm is
intentionally small; edge cases (plurals, compounds) are handled by
curating the dictionary, not by parser heuristics.

example, against `dictionaries/common-nouns.txt` v1:

```
base:  the kettle sits on the stove.
s+7:   the drawer sits on the spoon.
```

the user then writes a 40-80 word vignette using the s+7 line as a
prompt -- a kitchen remembered around a propped-open silverware drawer.

## first run

```bash
uv sync
python -m oulipo_memory_deck validate
```

`validate` (no args) checks all 8 cards against `schemas/card.schema.json`,
re-runs the s+7 swap against the committed dictionary, and confirms
each vignette is between 40 and 80 words. exits zero on a clean deck.

to render the deck to a single static page:

```bash
python -m oulipo_memory_deck render --out generated/print.html
```

then open `generated/print.html` in a browser.

## layout

```
oulipo_memory_deck/       # package: cli, swap, validate, render
schemas/card.schema.json  # card shape (json schema draft 2020-12)
dictionaries/
  common-nouns.txt        # the committed dictionary (v1)
  INDEX.json              # dictionary_id -> { file, version, provenance }
cards/objects/*.yaml      # the eight starter cards
tests/                    # pytest: schema, swap, render, no-network
docs/                     # historical first-pr notes
specs/                    # requirements / design / acceptance
generated/                # gitignored render output
```

## why no model in the loop

the literary constraint is the point. if a model writes the vignettes,
the s+7 swap becomes ornamental rather than load-bearing. the swap
provides the seed; the user provides the memory.

## license

MIT. see `LICENSE`.
