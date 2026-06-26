# oulipo-memory-deck

Take a sentence about a kettle. Replace every noun with the one seven entries
later in the dictionary. Now it's a sentence about a drawer that sits on a spoon,
and somehow it has a whole kitchen behind it. That's the deck.

## What it is

Eight everyday objects — kettle, hinge, key, lamp, mirror, radio, spoon, window —
each printed on a card. Every card carries one plain line about its object. Run
that line through the Oulipo S+7 swap and it comes out the other side strange but
not random, the way a half-remembered room is strange. Then you write a 40-to-80
word vignette using the strange line as the seed.

The whole thing is one static HTML page. No JavaScript, no assets, no model in the
loop. You can print it and play it at a table.

## The S+7 swap

Old Oulipo trick: take a dictionary, and replace every noun with the noun seven
entries down the list (wrap around at the end). Verbs, articles, anything not a
noun, pass through untouched. Casing and trailing punctuation survive.

```
base:  the kettle sits on the stove.
s+7:   the drawer sits on the spoon.
```

The swap is kept deliberately dumb. Plurals and compounds aren't solved with parser
cleverness; they're solved by curating the dictionary, which is the honest way to
solve them. The constraint does the work, not a heuristic.

## Try it

```bash
python -m oulipo_memory_deck show
```

Prints the eight cards ranked by how violently the swap mangled them — most-changed
first — and spells out the worst offender. Then validate the deck:

```bash
python -m oulipo_memory_deck validate
```

`validate` (no args) checks all eight cards against the schema, re-runs every swap
against the committed dictionary, and confirms each vignette landed in the 40-to-80
word window. Exits zero on a clean deck.

## Live demo

A Streamlit card browser: pick an object, see its plain line, its swapped line, and
the vignette someone wrote from it.

```bash
python -m uv run --with streamlit streamlit run streamlit_app.py
```

Deploy on Streamlit Cloud: repo `AthenaTheOwl/oulipo-memory-deck`, branch `main`,
main file `streamlit_app.py`.

<!-- live-url: (add the streamlit cloud url here once deployed) -->

## Render the printable deck

```bash
python -m oulipo_memory_deck render --out generated/print.html
```

Open `generated/print.html` and print it. Paper deck, propped-open silverware
drawer included.

## Why there's no model writing the vignettes

If a model writes the vignette, the swap is just decoration — you could delete it
and nothing would change. The point is the other way around: the constraint hands
you a strange seed, and you do the remembering. The kettle becoming a drawer is the
prompt. The kitchen is yours.

## Layout

```
oulipo_memory_deck/       package: cli, swap, validate, render
schemas/card.schema.json  the card shape
dictionaries/             the committed dictionary (v1) + provenance index
cards/objects/*.yaml      the eight starter cards
tests/  specs/  docs/
generated/                gitignored render output
```

## How it connects

Part of the narrative cluster with the [starforge demos](https://github.com/AthenaTheOwl?tab=repositories&q=starforge)
— small experiments in constraint-driven storytelling that share one prose source
and ship as different playable shapes.

## License

MIT. See `LICENSE`.
