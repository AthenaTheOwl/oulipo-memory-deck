"""schema validation: every shipped card matches card.schema.json."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator


def _load_schema(root: Path) -> Draft202012Validator:
    schema = json.loads(
        (root / "schemas" / "card.schema.json").read_text(encoding="utf-8")
    )
    return Draft202012Validator(schema)


def _card_paths(root: Path) -> list[Path]:
    return sorted((root / "cards" / "objects").glob("*.yaml"))


def test_eight_starter_cards_exist(repo_root):
    paths = _card_paths(repo_root)
    names = {p.stem for p in paths}
    expected = {
        "kettle", "hinge", "key", "lamp",
        "mirror", "radio", "spoon", "window",
    }
    assert names == expected, f"expected {expected}, got {names}"


@pytest.mark.parametrize(
    "card_name",
    ["kettle", "hinge", "key", "lamp", "mirror", "radio", "spoon", "window"],
)
def test_card_matches_schema(repo_root, card_name):
    validator = _load_schema(repo_root)
    path = repo_root / "cards" / "objects" / f"{card_name}.yaml"
    card = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = list(validator.iter_errors(card))
    assert errors == [], "\n".join(e.message for e in errors)


def test_card_ids_match_filename(repo_root):
    for path in _card_paths(repo_root):
        card = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert card["id"] == path.stem
        assert card["object"] == path.stem
