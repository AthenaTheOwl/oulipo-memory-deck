# AGENTS.md — oulipo-memory-deck

Operating contract for AI agents working on this deck.

## What this repo is

A tiny static-page card deck. Eight object cards, one S+7 substitution
script, one HTML renderer, one dictionary file. The artifact is a
single locally-opened `index.html` page.

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
| `swap-engineer` | Maintains `scripts/s_plus_7.py` |
| `renderer` | Maintains `scripts/render_html.py` and templates |

## Gates (will land in spec 0002)

```bash
python scripts/validate_cards.py
python scripts/voice_lint.py
python scripts/spec_check.py
python scripts/s_plus_7.py --check-determinism
```

## Out of scope

- LLM-generated vignettes. The constraint is literary, not
  technological; if a model wrote the vignettes, the deck would just
  be another generator.
- Multi-language dictionaries. v0 uses one English noun list.
- A web app. v0 is a static page.
- Selling. The deck is MIT.
