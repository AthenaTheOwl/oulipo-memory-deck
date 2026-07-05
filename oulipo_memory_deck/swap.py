"""S+7 substitution.

tokenization rule (kept tiny on purpose, documented inline):

1. split the line into runs on whitespace, preserving the whitespace runs
   so they can be reassembled verbatim.
2. for each non-whitespace run, separate leading punctuation, a "core"
   word, and trailing punctuation. punctuation is `string.punctuation`.
3. if the core's lowercase form appears in the dictionary, replace the
   core with the noun seven entries later (modulo dictionary length).
   apply the original casing pattern (all-lower / Title / ALL-CAPS) and
   reattach the original leading + trailing punctuation runs.
4. tokens whose core is not in the dictionary pass through unchanged.

edge cases (plurals, compounds, proper nouns) are handled by curating
the dictionary, not by parser heuristics. this module imports only
stdlib + (optionally) the dictionary file -- no network code lives
here, by design (see R-OMD-010 and tests/test_no_network.py).
"""

from __future__ import annotations

import hashlib
import json
import re
import string
from pathlib import Path


_WS_SPLIT = re.compile(r"(\s+)")


def _normalize(raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    return text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")


def load_dictionary(dictionary_id: str, root: Path) -> tuple[list[str], str, str]:
    """return (words, version, sha256_hex) for the named dictionary.

    sha256 is computed over the LF-normalized utf-8 bytes so the value
    is stable regardless of how the file was checked out on disk.
    """
    index_path = root / "dictionaries" / "INDEX.json"
    index = json.loads(index_path.read_text(encoding="utf-8"))
    if dictionary_id not in index:
        raise KeyError(f"unknown dictionary_id: {dictionary_id}")
    entry = index[dictionary_id]
    dict_path = root / "dictionaries" / entry["file"]
    normalized = _normalize(dict_path.read_bytes())
    sha = hashlib.sha256(normalized).hexdigest()
    expected = entry.get("sha256")
    if not expected:
        raise ValueError(f"missing sha256 for {dictionary_id} in INDEX.json")
    if expected != sha:
        raise ValueError(
            f"sha256 mismatch for {dictionary_id}: "
            f"expected {expected}, got {sha}"
        )
    words = [w for w in normalized.decode("utf-8").split("\n") if w]
    return words, entry["version"], sha


def _split_token(token: str) -> tuple[str, str, str]:
    i = 0
    while i < len(token) and token[i] in string.punctuation:
        i += 1
    j = len(token)
    while j > i and token[j - 1] in string.punctuation:
        j -= 1
    return token[:i], token[i:j], token[j:]


def _apply_case(template: str, replacement: str) -> str:
    if not template:
        return replacement
    if len(template) > 1 and template.isupper():
        return replacement.upper()
    if template[0].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def swap(line: str, dictionary: list[str]) -> str:
    """pure function: apply the S+7 substitution to `line`."""
    if not dictionary:
        return line
    index = {w: i for i, w in enumerate(dictionary)}
    n = len(dictionary)
    out: list[str] = []
    for part in _WS_SPLIT.split(line):
        if not part or part.isspace():
            out.append(part)
            continue
        lead, core, trail = _split_token(part)
        key = core.lower()
        if core and key in index:
            replacement = dictionary[(index[key] + 7) % n]
            replacement = _apply_case(core, replacement)
            out.append(lead + replacement + trail)
        else:
            out.append(part)
    return "".join(out)
