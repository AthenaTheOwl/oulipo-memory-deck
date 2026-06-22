# system map

```
.
├── pyproject.toml              # uv/hatchling package config
├── README.md                   # what the project is, how to run
├── PRODUCT_BRIEF.md            # scope + non-goals
├── SYSTEM_MAP.md               # this file
├── STATUS.md                   # current state, known limits, next queue
├── AGENTS.md                   # operating contract for agents
├── LICENSE
├── .gitignore
│
├── oulipo_memory_deck/         # the package
│   ├── __init__.py
│   ├── __main__.py             # `python -m oulipo_memory_deck ...`
│   ├── cli.py                  # argparse front end
│   ├── swap.py                 # pure S+7 function + dictionary loader
│   ├── validate.py             # schema + determinism + word-count gate
│   └── render.py               # cards -> single static print.html
│
├── schemas/
│   └── card.schema.json        # JSON Schema (draft 2020-12) for a card
│
├── dictionaries/
│   ├── common-nouns.txt        # 40 curated nouns, canonical S+7 order
│   └── INDEX.json              # dictionary_id -> { file, version, provenance }
│
├── cards/objects/              # one yaml per starter card
│   ├── kettle.yaml
│   ├── hinge.yaml
│   ├── key.yaml
│   ├── lamp.yaml
│   ├── mirror.yaml
│   ├── radio.yaml
│   ├── spoon.yaml
│   └── window.yaml
│
├── tests/                      # pytest
│   ├── conftest.py             # repo_root fixture
│   ├── test_schema.py          # all 8 cards match schema
│   ├── test_swap.py            # determinism + wraparound + casing
│   ├── test_render.py          # render produces a static page
│   └── test_no_network.py      # source grep + socket monkeypatch
│
├── docs/
│   └── first-pr.md             # the original first-pr plan (kept as history)
│
└── specs/0001-foundation/
    ├── requirements.md         # R-OMD-001..010
    ├── design.md
    ├── acceptance.md
    └── tasks.md
```

## data flow

```
   dictionaries/common-nouns.txt  -- ordered noun list
                |
                v
   swap.load_dictionary()  --  sha-stable read, returns words+version
                |
                v
   swap.swap(line, words)  --  pure function, deterministic
                ^
                |
   cards/objects/*.yaml  --  base_line, s_plus_7_line, vignette, ...
                |
   +------------+-------------+
   |                          |
   v                          v
   validate.validate_all      render.render_all
   (schema + s+7 + words)     (cards -> print.html)
                              |
                              v
                         generated/print.html
```

## boundaries

- `swap.py` is the only module that touches the dictionary file.
- `validate.py` is the only path that enforces the vignette word-count
  range (40-80).
- nothing in `oulipo_memory_deck/` imports `socket`, `urllib`,
  `requests`, or `http.client`. tests assert this at both source-grep
  and runtime levels.
