from __future__ import annotations

import json
from pathlib import Path

from oulipo_memory_deck.spec_check import check_specs
from oulipo_memory_deck.swap import load_dictionary


def test_common_nouns_sha_pin_matches_live_file(repo_root: Path):
    _words, _version, sha = load_dictionary("common-nouns-v1", repo_root)
    index = json.loads(
        (repo_root / "dictionaries" / "INDEX.json").read_text(encoding="utf-8")
    )
    assert sha == index["common-nouns-v1"]["sha256"]


def test_real_specs_have_no_dangling_references(repo_root: Path):
    assert check_specs(repo_root) == []


def test_dangling_reference_is_reported(tmp_path: Path):
    spec_dir = tmp_path / "specs" / "0003-probe"
    spec_dir.mkdir(parents=True)
    (spec_dir / "requirements.md").write_text(
        "# Spec 0003\n\n## R-OMD-997 - defined\n",
        encoding="utf-8",
    )
    (spec_dir / "tasks.md").write_text(
        "# Tasks\n\n- [ ] Build the missing thing (R-OMD-998).\n",
        encoding="utf-8",
    )

    errors = check_specs(tmp_path)

    assert any("R-OMD-998" in error for error in errors)
