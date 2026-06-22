# Spec 0002 — Tasks

Ordered for the first two PRs after foundation.

## PR 1 — pin sha256 + voice + spec_check

- [ ] Compute the sha256 of `dictionaries/common-nouns.txt` and pin
      it in `INDEX.json` (R-OMD-101).
- [ ] Make the loader refuse a mismatching sha (already implemented,
      add a test that the pinned value is the live value).
- [ ] Add `oulipo_memory_deck/voice_lint.py` with the rule list
      defined in `design.md` (R-OMD-102).
- [ ] Wire voice_lint into `python -m oulipo_memory_deck validate`.
- [ ] Add `oulipo_memory_deck/spec_check.py` and run it from CI / a
      dedicated subcommand (R-OMD-103).

## PR 2 — dictionary v2 + print-and-play

- [ ] Curate `dictionaries/common-nouns-v2.txt` (~1200 nouns).
- [ ] Register it in `INDEX.json` with its sha (R-OMD-104).
- [ ] Add one v2-pinned card to demonstrate the version discipline.
- [ ] Add `--layout print-and-play` to `render` (R-OMD-105).
- [ ] Add `--card <id>` to `validate` (R-OMD-106).
