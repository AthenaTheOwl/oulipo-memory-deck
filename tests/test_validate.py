"""validate: the vignette word-count bounds branch is actually enforced."""

from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from oulipo_memory_deck.swap import load_dictionary, swap
from oulipo_memory_deck.validate import validate_all


def _tmp_root(repo_root: Path, dest: Path) -> Path:
    """copy the schema + dictionary into dest so validate_all can run there."""
    shutil.copytree(repo_root / "schemas", dest / "schemas")
    shutil.copytree(repo_root / "dictionaries", dest / "dictionaries")
    (dest / "cards" / "objects").mkdir(parents=True)
    return dest


def _card_with_vignette(repo_root: Path, vignette: str) -> dict:
    """a schema-valid card whose s_plus_7_line is the real S+7 of base_line."""
    words, version, _sha = load_dictionary("common-nouns-v1", repo_root)
    base_line = "the kettle sits on the stove."
    return {
        "id": "probe",
        "object": "probe",
        "base_line": base_line,
        "s_plus_7_line": swap(base_line, words),
        "vignette": vignette,
        "dictionary_id": "common-nouns-v1",
        "dictionary_version": version,
    }


def test_short_vignette_fails_bounds_check(tmp_path: Path, repo_root):
    # drop the bounds check at validate.py:73 and this card would pass;
    # a 5-word vignette is well under the [40, 80] window.
    root = _tmp_root(repo_root, tmp_path)
    card = _card_with_vignette(repo_root, "a b c d e")
    (root / "cards" / "objects" / "probe.yaml").write_text(
        yaml.safe_dump(card), encoding="utf-8"
    )
    assert validate_all(root) == 1


def test_long_vignette_fails_bounds_check(tmp_path: Path, repo_root, capsys):
    root = _tmp_root(repo_root, tmp_path)
    card = _card_with_vignette(repo_root, " ".join(["word"] * 81))
    (root / "cards" / "objects" / "probe.yaml").write_text(
        yaml.safe_dump(card), encoding="utf-8"
    )
    assert validate_all(root) == 1
    assert "outside [40, 80]" in capsys.readouterr().out
