# Spec 0001 — Foundation

## R-OMD-001 — repo scaffold
Repo at `e:/claude_code/random-apps/oulipo-memory-deck`. MIT license.
README, AGENTS.md, LICENSE, .gitignore at the root.

## R-OMD-002 — card schema
`schemas/card.schema.json` defines one card: `id`, `object` (single
noun), `base_line` (1-2 sentences, plain physical description),
`s_plus_7_line` (deterministic output of the swap),
`vignette` (40-80 words), `dictionary_id`, `dictionary_version`.

## R-OMD-003 — eight starter cards
`cards/objects/` ships 8 YAML files: `kettle.yaml`, `hinge.yaml`,
`key.yaml`, `lamp.yaml`, `mirror.yaml`, `radio.yaml`, `spoon.yaml`,
`window.yaml`. Each file is one card per R-OMD-002.

## R-OMD-004 — dictionary
`dictionaries/common-nouns.txt` is a UTF-8 newline-delimited noun
list. Order is the canonical S+7 walk order. The file is committed
exactly once at a tagged `dictionary_version`; later changes require
a new version tag so old card swaps remain reproducible.

## R-OMD-005 — S+7 algorithm contract
`scripts/s_plus_7.py` takes a `base_line` plus a `dictionary_id` and
returns the `s_plus_7_line` by replacing every noun token with the
noun seven entries later in the dictionary, wrapping at end-of-file.
Non-noun tokens are passed through. Tokenization uses a small noun-
detection rule documented inline.

## R-OMD-006 — determinism check
`s_plus_7.py --check-determinism` re-runs the swap on every card and
fails if the produced `s_plus_7_line` differs from the stored value.

## R-OMD-007 — render pipeline
`scripts/render_html.py` reads the 8 card YAMLs plus
`templates/index.html` and emits a single `index.html` at the repo
root (or at `--out` path). The page lists each card with base line,
S+7 line, and vignette in a fixed layout.

## R-OMD-008 — vignette length gate
`scripts/validate_cards.py` fails any card whose `vignette` word count
is outside the 40-80 inclusive range.

## R-OMD-009 — voice lint + spec check
Portfolio voice spec gates apply to YAML prose surfaces and the
README. `spec_check.py` confirms every `R-OMD-NNN` referenced in
`design.md` and `tasks.md` is defined here.

## R-OMD-010 — no model in the loop
The repo refuses to invoke any external model API. The CLI has no
network code; tests assert this.
