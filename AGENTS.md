# AGENTS.md — oulipo-memory-deck

Operating contract for AI agents working on this deck.

## What this repo is

A tiny static-page card deck. Eight object cards, one S+7 substitution
module, one HTML renderer, one dictionary file. The artifact is a
single locally-opened page (`generated/print.html` by default).

This is not a writing app, a chatbot, or a generator. The user writes
every vignette by hand; the S+7 swap is the only mechanical
intervention.

## Voice constraints

- The base line is plain physical description. No metaphor, no mood.
  The whole point is that the S+7 swap will do the work.
- The S+7 swap is deterministic: same input + same dictionary
  produces the same output. Random walks are out.
- Vignettes are 40-80 words. Outside that range is a gate failure.
- No marketing words in any prose surface (cards, README, rules).
- No antithetical reversals as a structural device.

## Roles in tasks

| Role | What they do |
|---|---|
| `card-author` | Names an object, writes a base line, writes the vignette |
| `dictionary-keeper` | Owns `dictionaries/common-nouns.txt`; pins ordering |
| `swap-engineer` | Maintains `oulipo_memory_deck/swap.py` |
| `renderer` | Maintains `oulipo_memory_deck/render.py` |

## Gates

CI runs these; run them before merging.

```bash
uv run pytest
python -m oulipo_memory_deck validate
python scripts/validate_data_conformance.py
```

`validate` is the one command that covers what the separate scripts
in spec 0001 were planned to do: it runs `spec_check`
(`oulipo_memory_deck/spec_check.py`), then for every card the schema,
the voice lint on `base_line` and `vignette`
(`oulipo_memory_deck/voice_lint.py`), the pinned-dictionary check, S+7
determinism against the stored `s_plus_7_line`, and the 40-80 word
vignette count. There is no `scripts/validate_cards.py`,
`scripts/voice_lint.py`, `scripts/spec_check.py` or
`scripts/s_plus_7.py`.

## Out of scope

- LLM-generated vignettes. The constraint is literary, not
  technological; if a model wrote the vignettes, the deck would just
  be another generator.
- Multi-language dictionaries. v0 uses one English noun list.
- A web app. v0 is a static page.
- Selling. The deck is MIT.
