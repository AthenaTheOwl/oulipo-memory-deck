"""Check that spec requirement references resolve within each spec slug."""

from __future__ import annotations

import re
from pathlib import Path


REF_RE = re.compile(r"\bR-OMD-\d{3}\b")
REQ_HEADING_RE = re.compile(r"^##\s+(R-OMD-\d{3})\b", re.MULTILINE)
_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def check_specs(root: Path) -> list[str]:
    """Return dangling R-OMD reference errors under root/specs."""
    specs_dir = root / "specs"
    if not specs_dir.exists():
        return []

    failures: list[str] = []
    for spec_dir in sorted(path for path in specs_dir.iterdir() if path.is_dir()):
        requirements_path = spec_dir / "requirements.md"
        defined = _defined_requirements(requirements_path)
        for path in (spec_dir / "design.md", spec_dir / "tasks.md"):
            if not path.exists():
                continue
            text = _strip_fenced_code(path.read_text(encoding="utf-8"))
            for ref in sorted(set(REF_RE.findall(text))):
                if ref not in defined:
                    failures.append(
                        f"{_display_path(path, root)}: dangling reference {ref} "
                        f"(not defined in {_display_path(requirements_path, root)})"
                    )
    return failures


def _defined_requirements(requirements_path: Path) -> set[str]:
    if not requirements_path.exists():
        return set()
    text = requirements_path.read_text(encoding="utf-8")
    return set(REQ_HEADING_RE.findall(text))


def _strip_fenced_code(text: str) -> str:
    out: list[str] = []
    in_fence = False
    fence_marker = ""
    for line in text.splitlines():
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
        if not in_fence:
            out.append(line)
    return "\n".join(out)


def _display_path(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)
