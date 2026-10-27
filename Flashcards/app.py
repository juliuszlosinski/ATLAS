"""ATLAS Flashcards: entry point with navigation between pages.

Run:
    python -m streamlit run app.py
"""

from pathlib import Path

import streamlit as st

import theme

ASSETS = Path(__file__).parent / "assets"

st.set_page_config(page_title="ATLAS Flashcards", page_icon=str(ASSETS / "flashcards_logo.svg"), layout="wide")
theme.apply()

# Navigation in the top bar, so the logo can sit at the very top of the sidebar
navigation = st.navigation([
    st.Page("generator.py", title="Generator fiszek", default=True),
    st.Page("docs.py", title="Dokumentacja", url_path="dokumentacja"),
], position="top")

# Middle column of three keeps the logo centered and about 3/4 of the sidebar wide
_, logo_col, _ = st.sidebar.columns([1, 6, 1])
logo_col.image(str(ASSETS / "flashcards_logo.svg"), width="stretch")

navigation.run()
