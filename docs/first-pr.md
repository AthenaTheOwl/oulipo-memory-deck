# First PR after the scaffold

Title: `feat: card schema, dictionary v1, s_plus_7 swap script`

## Scope

This PR lands the typed substrate and the deterministic swap
function. No cards yet, no renderer yet. The point is that the swap
script is locked, the dictionary is versioned, and the determinism
gate runs green against a fixture.

## Files added

- `schemas/card.schema.json` — R-OMD-002. Required: `id`, `object`,
  `base_line`, `s_plus_7_line`, `vignette`, `dictionary_id`,
  `dictionary_version`. `vignette` is a string; the word-count
  range is enforced by `validate_cards.py` rather than the schema
  itself.
- `dictionaries/common-nouns.txt` — v1. ~1200 newline-delimited
  English nouns. Ordering is the canonical S+7 walk order; the
  file's `sha256` is recorded in `dictionaries/INDEX.json` as
  `dictionary_version = "v1"` along with a short provenance note.
- `dictionaries/INDEX.json` — maps `dictionary_id` to
  `{file, sha256, version, provenance}`.
- `scripts/s_plus_7.py` — R-OMD-005. Pure function plus CLI:
  - `s_plus_7.py <yaml-file>` prints the swap result.
  - `s_plus_7.py --check-determinism` walks all cards in
    `cards/objects/` and exits non-zero on any mismatch.
- `tests/test_swap_determinism.py` — two-pass invariance test
  against fixture inputs.
- `tests/test_swap_wraparound.py` — verifies the modulo-wrap at the
  dictionary end.
- `tests/test_no_network.py` — uses a `socket.socket` monkeypatch to
  assert `s_plus_7.py` opens zero sockets.
- `tests/fixtures/` — small fixture dictionary + 2 fixture lines.
- `pyproject.toml` — `pyyaml`, `jsonschema`, `pytest`, `ruff`.

## Files changed

None. First PR after the scaffold.

## Verification

```bash
uv sync
uv run pytest -v
uv run python scripts/s_plus_7.py --check-determinism
```

`pytest -v` shows at least 5 passing tests. The determinism check
exits zero because no cards exist yet (the walk is empty).

## What this PR does not do

- No card YAMLs (PR 2).
- No renderer (PR 2).
- No HTML template (PR 2).
- No validate_cards.py beyond the schema-driven check (full word-
  count gate in PR 2).
- No voice_lint or spec_check (PR 3).

## Review checklist

- [ ] `common-nouns.txt` v1 has its sha256 recorded in
      `INDEX.json`; the test suite re-computes it and confirms
      match.
- [ ] `s_plus_7.py` is a pure function; the CLI is a thin wrapper.
- [ ] Determinism check is genuinely deterministic — the same input
      twice in the same Python process produces the same output.
- [ ] No network code anywhere in the swap script.
- [ ] Tokenization rule is documented inline at the top of
      `s_plus_7.py`.
