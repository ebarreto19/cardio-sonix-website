"""Page with tutorial for audio recording and prediction"""

import streamlit as st
from pathlib import Path


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Tutorial"
PAGE_ICON: str = "🧪"


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)


st.title("User guide for heartbeat recording")
st.write(
    """
    <div class="alert alert-block alert-info" style="font-size:20px; background-color: #1b1b25; font-family:verdana; color: #a09fa7; border-radius: 10px; border: 0px #533078 solid">
        If you already have an audio recording, then simply download it, 
        but we recommend that you familiarize yourself with it 
        to know how to correctly record your heartbeat.
    </div>
    """,
    unsafe_allow_html=True
)
st.write("<br><br>", unsafe_allow_html=True)


# Step 1
st.header("Prepare your phone - :blue[Step 1]", divider="blue")
st.write("Open any audio recording software like a voice recorder on your phone.")
st.image(f"{GIF_DIR}/audio-recording.gif")
st.write("<br><br>", unsafe_allow_html=True)


# Step 2
st.header("Stand up - :blue[Step 2]", divider="blue")
st.markdown(
    """
    - find a quiet place 
    - remove outer clothing (phone must be in direct contact with the skin)
    - stand upright on a hard surface
    """
)
st.write("<br><br>", unsafe_allow_html=True)


# Step 3
st.header("Record your heartbeat - :blue[Step 3]", divider="blue")
st.write(
    "Now take the phone in one hand and firmly attach it "
    "to the area indicated in the picture by the yellow rectangle 👇"
)
st.image(f"{IMAGES_DIR}/phone-body-location.png")
st.markdown(
    """  
    ### Notes:
    - recording must have duration not less than 20 seconds
    - you can record both at rest and after physical activity 
    - phone should be in a vertical position
    - distance between your body and the phone should not remain
    - try not to move or make unnecessary sounds
    - make sure you put the phone on the side with the microphone
    """
)
st.write("<br><br>", unsafe_allow_html=True)


# Step 4
st.header("Upload audio - :blue[Step 4]", divider="blue")
st.write(
    """
    If you used the built-in recorder on this site, the audio is already downloaded. 
    If you recorded audio using other software, simply upload the file to the site. 
    We support all audio formats.
    """
)
st.image(f"{GIF_DIR}/file-loading.gif")


def rate_change():
    if st.session_state["rate"] in ["Helped a lot! 😃", "It was helpful 🙂"]:
        st.balloons()


rate = st.sidebar.selectbox(
    "Was it helpful?",
    ["It's important to us", "Helped a lot! 😃", "It was helpful 🙂", "Didn't really help 🤨", "Nothing is clear! 😡"],
    key="rate",
    on_change=rate_change
)
