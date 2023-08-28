"""Entry point for the streamlit application"""

import streamlit as st
from pathlib import Path


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent if "__file__" in locals() else Path.cwd()
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Home"
PAGE_ICON: str = "⭐️"


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
)


st.title(":red[_Dr. Cardio Sonix_] :heart:")
st.write(
    """
    **Dr. Cardio Sonix is your cardiologist 
    available to everyone at any time! 
    Just record the sounds of your heartbeat 
    as indicated in the instructions and send us 🫶🏻** 
    """
)
st.image(f"{GIF_DIR}/pulse-home-bar.gif")


col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    st.header(":blue[Cardiovascular diseases]")
    st.image(f"{IMAGES_DIR}/heart-attack.png")
    st.write(
        """
        According to the World Health Organisation, 
        cardiovascular diseases (CVDs) are the number one cause of death globally: 
        more people die annually from CVDs than from any other cause. 
        An estimated 17.1 million people died from CVDs in 2004, 
        representing 29% of all global deaths. 
        Of these deaths, an estimated 7.2 million were due to coronary heart disease.
        """
    )


with col2:
    st.header(":blue[Motivation]")
    st.image(f"{GIF_DIR}/slime.gif")
    st.write(
        """
        Any method which can help to detect signs of heart disease 
        could therefore have a significant impact on world health. 
        This challenge is to produce methods to do exactly that. 
        Specifically, we are interested in creating the first level of screening 
        of cardiac pathologies both in a Hospital environment by a doctor 
        (using a digital stethoscope) and at home by the patient (using a mobile device).
        """
    )


st.header(":blue[Medicine and AI]")
st.image(f"{IMAGES_DIR}/medicine-ai.jpeg")
st.write(
    """
    The problem is of particular interest to machine learning researchers 
    as it involves classification of audio sample data, 
    where distinguishing between classes of interest is non-trivial. 
    Data is gathered in real-world situations 
    and frequently contains background noise of every conceivable type. 
    The differences between heart sounds corresponding 
    to different heart symptoms can also be extremely subtle 
    and challenging to separate. Success in classifying this 
    form of data requires extremely robust classifiers. 
    Despite its medical significance, 
    to date this is a relatively unexplored application for machine learning.
    """
)
