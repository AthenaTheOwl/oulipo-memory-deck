"""validate cards: schema + S+7 determinism + vignette word count."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from .swap import load_dictionary, swap


VIGNETTE_MIN = 40
VIGNETTE_MAX = 80


def _word_count(text: str) -> int:
    return len(text.split())


def validate_all(root: Path) -> int:
    schema_path = root / "schemas" / "card.schema.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)

    cards_dir = root / "cards" / "objects"
    yaml_files = sorted(cards_dir.glob("*.yaml"))

    if not yaml_files:
        print("no card files found in cards/objects/", file=sys.stderr)
        return 1

    failures = 0
    for path in yaml_files:
        card = yaml.safe_load(path.read_text(encoding="utf-8"))

        errors = list(validator.iter_errors(card))
        if errors:
            for err in errors:
                print(f"{path.name}: schema error: {err.message}")
            failures += 1
            continue

        try:
            dictionary, version, _sha = load_dictionary(
                card["dictionary_id"], root
            )
        except (KeyError, ValueError) as exc:
            print(f"{path.name}: dictionary error: {exc}")
            failures += 1
            continue

        if version != card["dictionary_version"]:
            print(
                f"{path.name}: dictionary_version mismatch: "
                f"card says {card['dictionary_version']}, "
                f"INDEX.json has {version}"
            )
            failures += 1
            continue

        produced = swap(card["base_line"], dictionary)
        if produced != card["s_plus_7_line"]:
            print(f"{path.name}: s_plus_7_line is not deterministic:")
            print(f"  stored:   {card['s_plus_7_line']!r}")
            print(f"  produced: {produced!r}")
            failures += 1
            continue

        wc = _word_count(card["vignette"])
        if wc < VIGNETTE_MIN or wc > VIGNETTE_MAX:
            print(
                f"{path.name}: vignette word count {wc} "
                f"outside [{VIGNETTE_MIN}, {VIGNETTE_MAX}]"
            )
            failures += 1
            continue

        print(f"{path.name}: ok (vignette {wc} words)")

    if failures:
        print(f"\n{failures} card(s) failed validation", file=sys.stderr)
        return 1
    print(f"\nall {len(yaml_files)} cards validate.")
    return 0
