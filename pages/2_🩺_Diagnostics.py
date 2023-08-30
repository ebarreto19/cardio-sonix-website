"""Page to make predictions and diagnostics"""

from typing import Union
from pathlib import Path
import io
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import plotly.express as px
from sonixhub import base_cardionet
from utils import GIF_DIR, IMAGES_DIR, ROOT_DIR
from utils import AudioConvertor


# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Diagnostics"
PAGE_ICON: str = "🩺"

# Set page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)


# Set page session_state
if not st.session_state.get("card", None):
    st.session_state["card"] = {
        "name": "...",
        "age": "...",
        "gender": "...",
        "complaints": "..."
    }


def record_audio() -> io.BytesIO | None:
    data = audio_recorder(
        neutral_color="#0b0e35",
        recording_color="#5b2da1",
        energy_threshold=0.01,
        pause_threshold=0.8
    )
    if data:
        st.audio(data)
        return io.BytesIO(data)


def load_audio() -> Union[io.BytesIO, None]:
    data = st.file_uploader(
        label="Upload an audio file of your heartbeat "
              "that is at least 10 seconds long.",
        type=[
            ".wav", ".aac", ".ogg",
            ".mp3", ".aiff", ".flac",
            ".ape", ".dsd", ".mqa", "wma"
        ]
    )

    if data:
        st.audio(data.getvalue())
        return AudioConvertor(
            root_dir=ROOT_DIR,
            valid_extensions=["wav"],
            convert_to="wav"
        )(data)


def get_predictions(data: Union[io.BytesIO, bytes]) -> dict:
    with st.spinner("Please wait... We examine your heart 🫀"):
        try:
            return base_cardionet(data)
        except Exception as e:
            st.error("We're sorry, something happened to the server ⚡️")


def plot_predictions(predictions: dict) -> None:
    fig = px.bar(x=predictions["classes"], y=predictions["probs"])
    fig.update_layout(
        xaxis_title="Classes",
        yaxis_title="Probabilities"
    )
    st.plotly_chart(
        fig, theme="streamlit", use_container_width=True,
        labels=dict(x="Classes", y="Probabilities")
    )


def classification_report(predictions: dict) -> None:
    col1, col2 = st.columns([0.5, 0.5], gap="large")

    col1.write(
        f"""
        <div class="alert alert-block alert-info" style="font-size:20px; background-color: #0b0e22; font-family:verdana; color: #ffffff; border-radius: 10px; border: 0px #533078 solid">
            <b><font color=#5954b0>Survey card ⚕️</font></b>
            <br>Name: {st.session_state["card"].get("name")}<br>
            Age: {st.session_state["card"].get("age")}
            <br>Gender: {st.session_state["card"].get("gender")}<br>
            Сomplaints: {st.session_state["card"].get("complaints")}
            <br>Diagnosis: {predictions["preds"]}<br>
        </div>
        """,
        unsafe_allow_html=True
    )

    col2.image(f"{GIF_DIR}/status-{predictions['preds']}.gif")


def artifact_report() -> None:
    st.error(
        "Error! Heartbeat sounds were not found in the file you uploaded. "
        "Try recording again.", icon="🚨"
    )
    st.markdown(
        """
        There may have been a lot of extraneous noise during the recording. 
        ### Try:
        - Find a quiet place
        - Make sure there is no extraneous noise
        - Attach the phone closer to the body as shown in the picture
        - If all else fails, try recording audio from another device
        """
    )
    st.image(f"{IMAGES_DIR}/phone-body-location.png")


def scan_audio(data: bytes) -> None:
    predictions = get_predictions(data)
    if not predictions:
        return None
    elif predictions["preds"] == "artifact":
        artifact_report()
    else:
        classification_report(predictions)
        plot_predictions(predictions)


def create_medical_card() -> None:
    # Field name
    name = st.text_input("Enter your full name")
    st.session_state["card"]["name"] = name if name else "unknown"

    # Field age
    age = st.number_input("How old are you?", step=1, min_value=0, max_value=120)
    st.session_state["card"]["age"] = "unknown" if age == 0 else age

    # Field gender
    gender = st.selectbox("What is your gender?", ["unknown", "man", "woman"])
    st.session_state["card"]["gender"] = gender

    # Field complaints
    complaints = st.text_input("Please describe what is bothering you?")
    st.session_state["card"]["complaints"] = complaints if complaints else "no complaints"


def get_data() -> None | io.BytesIO | bytes:
    choice = st.sidebar.selectbox(
        label="Do you want to upload or record an audio file?",
        options=["Upload 📁", "Record 🎤"]
    )
    return load_audio() if choice == "Upload 📁" else record_audio()


st.image(f"{GIF_DIR}/circle.gif")
data = get_data()

if data:
    create_card = st.radio("Do you want to fill out a medical card?", ["Default", "Yes", "No"])
    if create_card == "Yes":
        create_medical_card()
        st.button(":blue[Scan] 🩺", key="scan")
    if (create_card == "Yes" and st.session_state.get("scan", None)) or create_card == "No":
        scan_audio(data)

