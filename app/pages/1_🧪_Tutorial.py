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


# Step 1
st.header("Prepare your phone - :blue[Step 1]")
st.write("Open any audio recording software like a voice recorder on your phone.")
st.image(f"{GIF_DIR}/audio-recording.gif")


# Step 2
st.header("Lie down - :blue[Step 2]")

st.markdown(
    """
    - calm down  
    - find a quiet place 
    - remove outer clothing (phone must be in direct contact with the skin)
    - lie down as in the picture 👇
    """
)

st.image(f"{IMAGES_DIR}/lie-down.png")


# Step 3
st.header("Record your heartbeat - :blue[Step 3]")

st.write(
    "Now take the phone in one hand and firmly attach it "
    "to the area indicated in the picture by the yellow rectangle 👇"
)

st.image(f"{IMAGES_DIR}/phone-body-location.png")

st.markdown(
    """  
    ### Should I just lie down?
    Almost, but it would be nice to know a couple of details about how to breathe.
    While recording, you should inhale slowly and then hold your breath for 5 seconds.
    After holding your breath, exhale slowly through your mouth
    so that your breath does not get on the record. 
    The length of the recording with which you can work is 10 seconds. 
    Keep in mind that if there are 30 seconds in the recording, 
    then it will be divided into three parts and you will get three results, 
    but if there are less than 10 seconds, you will get an error.   
    
    ### Notes:
    - phone should be in a vertical position
    - distance between your body and the phone should not remain
    - try not to move or make unnecessary sounds
    - make sure you put the phone on the side with the microphone
    """
)


# Step 4
st.header("Upload audio - :blue[Step 4]")
st.write(
    "Upload the audio recording of the heartbeat obtained in the previous step. "
    "An audio recording of the heartbeat can be obtained in any way, including special devices. "
    "The method in step 3 does not pretend to be the best, "
    "but it makes it possible to get the necessary data when only the phone is at hand."
)


def rate_change():
    if st.session_state["rate"] in ["Helped a lot! 😃", "It was helpful 🙂"]:
        st.balloons()


st.image(f"{GIF_DIR}/file-loading.gif")
rate = st.sidebar.selectbox(
    "Was it helpful?",
    ["It's important to us", "Helped a lot! 😃", "It was helpful 🙂", "Didn't really help 🤨", "Nothing is clear! 😡"],
    key="rate",
    on_change=rate_change
)
