"""Entry point for the streamlit application"""

import streamlit as st
from pathlib import Path
from utils import GIF_DIR, IMAGES_DIR


# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Home"
PAGE_ICON: str = "⭐️"

# Set page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
)


st.title(":red[_Dr. Cardionix_] :heart:")
st.write(
    """
    <div class="alert alert-block alert-info" style="font-size:20px; background-color: #661321; font-family:verdana; color: #e63c3c; border-radius: 10px; border: 0px #533078 solid">
        Dr. Cardio Sonix is your cardiologist 
        available to everyone at any time! 
        Just record the sounds of your heartbeat 
        as indicated in the instructions and send us 🫶🏻
    </div>
    """,
    unsafe_allow_html=True
)
st.write("<br><br>", unsafe_allow_html=True)
st.image(f"{GIF_DIR}/pulse-home-bar.gif")


col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    st.header(":blue[Cardiovascular diseases]", divider=True)
    st.image(f"{IMAGES_DIR}/heart-attack.png")
    st.write(
        """
        <div class="alert alert-block alert-info" style="font-size:20px; background-color: #0b0e22; font-family:verdana; color: #353cbd; border-radius: 10px; border: 0px #533078 solid">
            Heart disease has remained the leading cause of death worldwide for 20 years. 
            However, they have never claimed as many lives as they do today. 
            Deaths from cardiovascular disease have increased by more than 2 million since 2000, reaching nearly 9 million in 2019. 
            Heart disease today accounts for 16% of all deaths worldwide.
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:
    st.header(":blue[Motivation]", divider="blue")
    st.image(f"{GIF_DIR}/slime.gif")
    st.write(
        """
        <div class="alert alert-block alert-info" style="font-size:20px; background-color: #0b0e22; font-family:verdana; color: #353cbd; border-radius: 10px; border: 0px #533078 solid">
            Any method that can help detect signs of cardiovascular disease early can save many lives. 
            Our goal is to make a reliable classifier accessible to every person. 
            We see a future world in which deaths from diseases that can be cured in their early stages will disappear forever.
            Together we can go beyond human capabilities 🌎
        </div>
        """,
        unsafe_allow_html=True
    )


st.header(":blue[Medicine and AI]", divider="blue")
st.image(f"{IMAGES_DIR}/medicine-ai.jpeg")
st.write(
    """
    <div class="alert alert-block alert-info" style="font-size:20px; background-color: #0b0e22; font-family:verdana; color: #353cbd; border-radius: 10px; border: 0px #533078 solid">
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
    </div>
    """,
    unsafe_allow_html=True
)
