"""oulipo memory deck -- card browser.

reads the committed cards (cards/objects/*.yaml) and the committed
dictionary directly off disk, relative to this file. no network, no
secrets. pick a card; see its base line, its S+7 line, and the
vignette seeded by the swap.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from oulipo_memory_deck.show import load_rows

ROOT = Path(__file__).resolve().parent

st.set_page_config(page_title="oulipo memory deck", page_icon=":spades:")

st.title("oulipo memory deck")
st.caption(
    "eight everyday objects, each base line run through a deterministic "
    "oulipo S+7 noun swap to seed a 40-80 word vignette."
)

cards_dir = ROOT / "cards" / "objects"
if not cards_dir.exists() or not any(cards_dir.glob("*.yaml")):
    st.warning(
        "no cards found at cards/objects/. run this app from a checkout "
        "of the oulipo-memory-deck repo."
    )
    st.stop()

rows = load_rows(ROOT)

total_swaps = sum(r["swaps"] for r in rows)
most = rows[0]
avg_words = round(sum(r["vignette_words"] for r in rows) / len(rows))

col1, col2, col3 = st.columns(3)
col1.metric("cards", len(rows))
col2.metric("nouns swapped", total_swaps)
col3.metric("avg vignette words", avg_words)

st.info(
    f"most-transformed card: '{most['object']}' "
    f"({most['swaps']} nouns swapped)."
)

st.subheader("the deck, ranked by S+7 transform")
table = [
    {
        "object": r["object"],
        "swaps": r["swaps"],
        "vignette words": r["vignette_words"],
        "s+7 line": r["s_plus_7_line"],
    }
    for r in rows
]
st.dataframe(table, use_container_width=True, hide_index=True)

st.subheader("browse a card")
objects = [r["object"] for r in rows]
choice = st.selectbox("pick an object", objects)
card = next(r for r in rows if r["object"] == choice)

st.markdown(f"**base line**  \n_{card['base_line']}_")
st.markdown(f"**S+7 line**  \n**{card['s_plus_7_line']}**")
st.markdown("**vignette**")
st.write(card["vignette"])
st.caption(
    f"{card['swaps']} nouns swapped  |  {card['vignette_words']} words"
)
