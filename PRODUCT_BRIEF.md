# product brief

## what this is

a narrative card deck. eight everyday objects (kettle, hinge, key,
lamp, mirror, radio, spoon, window) become memory cards. each card
carries:

- a **base line** -- a plain physical description of the object
- an **s+7 line** -- the base line with every noun replaced by the
  noun seven entries later in a committed dictionary
- a **vignette** -- 40-80 words of hand-written prose that uses the
  uncanny s+7 line as the seed of a memory

the artifact is a single static html page, printable, no javascript,
no external assets.

## who it is for

a writer, a workshop facilitator, or anyone curious about the oulipo
s+7 constraint as a memory-prompt device. v0.1 is a finished tiny
thing rather than a starter kit.

## what shipped in v0.1

- 8 starter cards in `cards/objects/`
- a 40-noun curated dictionary in `dictionaries/common-nouns.txt`,
  tagged as `common-nouns-v1`
- `python -m oulipo_memory_deck validate` -- schema + s+7 determinism
  + vignette word count, no args, exits zero when the deck is well
  formed
- `python -m oulipo_memory_deck render --out generated/print.html` --
  one static page with all eight cards in sequence
- `pytest` test suite covering schema, swap, render, and a no-network
  invariant

## what this is not

- a writing assistant. the s+7 swap is the only mechanical step; every
  vignette is hand-written.
- a chatbot. no model is in the loop at any point, by design.
- a generator. one curated dictionary, one deterministic walk; same
  input yields the same output.
- a web app. v0.1 is a static page opened locally.

## non-goals for v0.2 and beyond

- print-and-play card layout
- multi-language dictionaries
- card decks beyond the initial eight

## voice

lowercase, plain physical description in the base lines, no marketing
words anywhere in the prose surfaces.
