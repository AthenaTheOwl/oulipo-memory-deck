# Spec 0002 — Design

Foundation shipped the swap, the schema, the renderer, and a small
curated dictionary. This iteration tightens the discipline around
those artifacts: pin the dictionary, lint the prose, and open the
door to a v2 dictionary without breaking existing cards.

## Shape

```
oulipo_memory_deck/
  transform.py            # canonical swap import (R-OMD-005)
  swap.py                 # implementation (kept for back-compat)
  validate.py             # gains voice + sha gates (R-OMD-101, R-OMD-102)
  voice_lint.py           # NEW — voice gate (R-OMD-102)
  spec_check.py           # NEW — R-OMD-NNN ref check (R-OMD-103)
  render.py               # gains --layout flag (R-OMD-105)
dictionaries/
  common-nouns.txt        # v1, pinned sha256 (R-OMD-101)
  common-nouns-v2.txt     # NEW — ~1200 nouns (R-OMD-104)
  INDEX.json              # both entries with sha256
```

## Pinned sha256

The loader already computes the sha at read time. R-OMD-101 makes
the `sha256` field in `INDEX.json` non-optional. A new dictionary
file is committed together with its sha; rotation requires both
changes in the same commit.

## Voice lint

A small rule set, not a full natural-language gate:

- no marketing words (`leverage`, `delight`, `journey`, etc.).
- lowercase headings in markdown; sentence-case prose in YAML.
- no internal references (employer/manager/project names).

The rule list lives next to the implementation so it can be reviewed
without reading code.

## Dictionary versioning

`dictionary_id` is an opaque slug; `dictionary_version` is a string
of the form `vN`. Cards always carry both. The loader fails closed
if the file's sha or version drifts. To retire a dictionary, a new
slug is registered alongside; old cards stay pinned.

## Print-and-play

A second render path: two cards per landscape page, with a fold
guide and a small back panel. Implementation reuses the same card
data and a separate template; no algorithm change.

## What is not in spec 0002

- Multi-language dictionaries.
- A web UI for editing cards.
- Any model API or generation step.
