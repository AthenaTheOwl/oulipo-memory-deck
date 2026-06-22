"""command-line entry point.

usage:
  python -m oulipo_memory_deck validate          # default: validate all cards
  python -m oulipo_memory_deck render --out PATH # render deck to print.html
"""

from __future__ import annotations

import argparse
from pathlib import Path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="oulipo_memory_deck",
        description="deterministic S+7 card deck",
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser(
        "validate",
        help="validate all cards against schema + S+7 determinism",
    )

    render = sub.add_parser("render", help="render the deck to a static page")
    render.add_argument(
        "--out",
        default="generated/print.html",
        help="output path (default: generated/print.html)",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    root = Path.cwd()

    cmd = args.cmd or "validate"

    if cmd == "validate":
        from .validate import validate_all
        return validate_all(root)
    if cmd == "render":
        from .render import render_all
        return render_all(root, Path(args.out))

    parser.print_help()
    return 1
