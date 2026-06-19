# Oulipo Memory Deck

A narrative deckbuilder where everyday objects (kettle, hinge, key) become
memory cards. Each card's description is run through Oulipo S+7 word-swaps
to expose buried history.

## What this is

Eight starter cards, each named for an everyday object. Each card has:

- A base line — a literal description of the object.
- An S+7 line — the same line with every noun replaced by the seventh
  noun after it in a chosen dictionary.
- A 40-80 word vignette written by the user that uses the S+7 line as a
  prompt and treats the uncanny substitution as the seed of a memory.

The output is a single static HTML page the user opens locally. The whole
deck fits in one browser tab.

## Status

v0 scaffold. No cards, no S+7 script, no renderer. Spec 0001 defines
the card YAML schema, the S+7 algorithm contract, the dictionary
format, and the gates that land in spec 0002.

## How to run

Placeholder. Spec 0002 will ship:

```bash
python scripts/s_plus_7.py cards/kettle.yaml
python scripts/render_html.py --out index.html
```

Then open `index.html` in a browser.

## Layout

```
.
├── AGENTS.md
├── LICENSE
├── README.md
├── docs/
│   └── first-pr.md
└── specs/
    └── 0001-foundation/
        ├── acceptance.md
        ├── design.md
        ├── requirements.md
        └── tasks.md
```

Planned directories:

- `cards/`
  - `objects/*.yaml` — one file per object card.
- `dictionaries/`
  - `common-nouns.txt` — the dictionary the S+7 swap walks.
- `scripts/`
  - `s_plus_7.py` — performs the substitution.
  - `render_html.py` — assembles the single static page.
- `templates/index.html` — page layout.
- `generated/` — gitignored.

## Why this exists

LLM-era writing tools converge on chat. An Oulipo-constrained card
deck makes the opposite point: a small fixed rule plus a curated
dictionary produces prose that is stranger and more useful than free
generation. The deck is a tiny shippable artifact that demonstrates
prompt-engineering taste through a literary constraint rather than a
chat transcript.

## License

MIT. See `LICENSE`.
