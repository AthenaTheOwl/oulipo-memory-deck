"""render the card deck to a single static print.html page."""

from __future__ import annotations

import html
from pathlib import Path

import yaml


_PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>oulipo memory deck</title>
<style>
  body {{
    font-family: Georgia, "Times New Roman", serif;
    max-width: 42rem;
    margin: 2rem auto;
    padding: 0 1rem;
    color: #1d1d1d;
    line-height: 1.55;
  }}
  h1 {{
    font-size: 1.4rem;
    font-weight: normal;
    font-variant: small-caps;
    letter-spacing: 0.12em;
    margin: 0 0 2.5rem 0;
  }}
  .card {{
    margin-bottom: 2.5rem;
    border-top: 1px solid #c9c9c9;
    padding-top: 1.2rem;
    page-break-inside: avoid;
  }}
  .object {{
    font-variant: small-caps;
    letter-spacing: 0.18em;
    color: #6a6a6a;
    font-size: 0.85rem;
  }}
  .base-line {{
    color: #7a7a7a;
    font-style: italic;
    margin-top: 0.4rem;
  }}
  .swap-line {{
    font-weight: bold;
    margin-top: 0.5rem;
    font-size: 1.1rem;
  }}
  .vignette {{
    margin-top: 1rem;
  }}
  @media print {{
    .card {{ page-break-after: always; }}
    h1 {{ page-break-after: avoid; }}
  }}
</style>
</head>
<body>
<h1>oulipo memory deck</h1>
{cards}
</body>
</html>
"""

_CARD = """<section class="card" id="card-{slug}">
  <div class="object">{object}</div>
  <div class="base-line">{base_line}</div>
  <div class="swap-line">{s_plus_7_line}</div>
  <p class="vignette">{vignette}</p>
</section>"""


def _render_one(card: dict) -> str:
    return _CARD.format(
        slug=html.escape(card["id"]),
        object=html.escape(card["object"]),
        base_line=html.escape(card["base_line"]),
        s_plus_7_line=html.escape(card["s_plus_7_line"]),
        vignette=html.escape(card["vignette"]),
    )


def render_deck(cards: list[dict]) -> str:
    body = "\n".join(_render_one(c) for c in cards)
    return _PAGE.format(cards=body)


def render_all(root: Path, out_path: Path) -> int:
    cards_dir = root / "cards" / "objects"
    files = sorted(cards_dir.glob("*.yaml"))
    if not files:
        print("no cards to render", file=__import__("sys").stderr)
        return 1
    cards = [yaml.safe_load(p.read_text(encoding="utf-8")) for p in files]
    page = render_deck(cards)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(page, encoding="utf-8")
    print(f"wrote {out_path} ({len(cards)} cards)")
    return 0
