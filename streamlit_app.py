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
from oulipo_memory_deck.swap import load_dictionary, swap

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

st.divider()
st.subheader("run the S+7 transform on your own line")
st.caption(
    "type any line. it is run through the same deterministic "
    "oulipo_memory_deck.swap.swap() function the deck was built with — "
    "each dictionary noun is replaced by the one seven entries later. "
    "words not in the dictionary pass through unchanged."
)

# load the real dictionary off disk (id + version + sha verified inside).
dict_id = "common-nouns-v1"
try:
    dictionary, dict_ver, dict_sha = load_dictionary(dict_id, ROOT)
except (KeyError, ValueError, FileNotFoundError) as exc:
    st.error(f"could not load dictionary '{dict_id}': {exc}")
    st.stop()

st.caption(
    f"dictionary: {dict_id} ({dict_ver}, {len(dictionary)} nouns, "
    f"sha256 {dict_sha[:12]}…)"
)

user_line = st.text_input(
    "your line",
    value="the lamp hums beside the window.",
    help="anything. nouns present in the dictionary get swapped +7.",
)

if user_line.strip():
    # CALL THE REAL ENGINE — same swap() the committed deck uses.
    result = swap(user_line, dictionary)

    before = user_line.split()
    after = result.split()
    swaps = sum(1 for a, b in zip(before, after) if a != b)

    st.markdown(f"**base line**  \n_{user_line}_")
    st.markdown(f"**S+7 line**  \n**{result}**")

    if swaps:
        st.success(f"{swaps} word(s) swapped.")
        # show the per-word mapping, only for tokens that actually changed.
        changed = [
            {"position": i + 1, "before": a, "after": b}
            for i, (a, b) in enumerate(zip(before, after))
            if a != b
        ]
        st.dataframe(changed, use_container_width=True, hide_index=True)
    else:
        st.info(
            "no swaps — none of these words are in the dictionary. "
            "try one of the dictionary nouns below."
        )

    with st.expander("dictionary nouns (the S+7 walk)"):
        st.write(
            "the +7 swap walks this exact ordered list, wrapping at the end:"
        )
        st.code("  ".join(dictionary), language=None)
else:
    st.info("enter a line above to run the transform.")
