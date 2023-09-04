"""Page about health"""

import streamlit as st
from pathlib import Path


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Research"
PAGE_ICON: str = "🔬"


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)
