"""Small voice lint rules for prose surfaces."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping


MARKETING_WORDS = frozenset(
    {
        "delight",
        "disrupt",
        "ecosystem",
        "empower",
        "frictionless",
        "holistic",
        "journey",
        "leverage",
        "pivot",
        "robust",
        "scalable",
        "seamless",
        "synergy",
        "transformative",
    }
)

# Project-specific employer, manager, or project names can be pinned here.
INTERNAL_REFERENCES: tuple[str, ...] = ()

CARD_TEXT_FIELDS = ("base_line", "vignette")

_ACRONYM_RE = re.compile(r"\b[A-Z]{2,}\b")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


def lint_card(
    card: Mapping[str, object],
    *,
    internal_references: Iterable[str] | None = None,
) -> list[str]:
    """Return voice lint failures for card prose fields."""
    failures: list[str] = []
    refs = INTERNAL_REFERENCES if internal_references is None else internal_references
    for field in CARD_TEXT_FIELDS:
        text = str(card.get(field, ""))
        failures.extend(_lint_text(text, source=field, internal_references=refs))
        for acronym in sorted(set(_ACRONYM_RE.findall(text))):
            failures.append(f"{field}: capitalized acronym {acronym!r}")
    return failures


def lint_markdown(
    text: str,
    *,
    source: str = "markdown",
    internal_references: Iterable[str] | None = None,
) -> list[str]:
    """Return voice lint failures for markdown prose."""
    refs = INTERNAL_REFERENCES if internal_references is None else internal_references
    failures = _lint_text(text, source=source, internal_references=refs)
    in_fence = False
    fence_marker = ""
    for line_no, line in enumerate(text.splitlines(), start=1):
        fence_match = _FENCE_RE.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = ""
            continue
        if in_fence:
            continue
        heading_match = _HEADING_RE.match(line)
        if heading_match and _has_title_case_word(heading_match.group(2)):
            failures.append(
                f"{source}:{line_no}: markdown heading should stay lowercase"
            )
    return failures


def _lint_text(
    text: str,
    *,
    source: str,
    internal_references: Iterable[str],
) -> list[str]:
    failures: list[str] = []
    for word in sorted(MARKETING_WORDS):
        if _contains_term(text, word):
            failures.append(f"{source}: marketing word {word!r}")
    for ref in sorted({ref for ref in internal_references if ref}):
        if _contains_term(text, ref):
            failures.append(f"{source}: internal reference {ref!r}")
    return failures


def _contains_term(text: str, term: str) -> bool:
    pattern = rf"(?<![A-Za-z0-9_-]){re.escape(term)}(?![A-Za-z0-9_-])"
    return re.search(pattern, text, flags=re.IGNORECASE) is not None


def _has_title_case_word(heading: str) -> bool:
    for word in re.findall(r"[A-Za-z][A-Za-z0-9+-]*", heading):
        if word.isupper() or re.fullmatch(r"R-OMD-\d+", word):
            continue
        if word[:1].isupper():
            return True
    return False
