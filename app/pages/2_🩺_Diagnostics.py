"""Page to make predictions and diagnostics"""

from typing import Union
from pathlib import Path
import streamlit as st
import requests
import plotly.express as px


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Diagnostics"
PAGE_ICON: str = "🩺"

# --- Cardio Sonix API ---
API_HOST: str = "http://127.0.0.1:8000"
END_POINT_PREDICT: str = API_HOST + "/predict"


# Set page config
st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)

# Set page session_state
if not st.session_state.get("card", None):
    st.session_state["card"] = {
        "name": None,
        "age": None,
        "gender": None,
        "complaint": None
    }


def load_audio() -> Union[bytes, None]:
    data = st.file_uploader(
        label="Upload an audio file of your heartbeat "
              "that is at least 10 seconds long.")
    if data:
        data = data.getvalue()
        st.audio(data)
    return data


def get_predictions(data: bytes) -> dict:
    with st.spinner("Please wait... We examine your heart 🫀"):
        try:
            return requests.post(
                url=END_POINT_PREDICT,
                files={f"audio_file": data}
            ).json()
        except requests.exceptions.ConnectionError as e:
            st.error("ConnectionError")


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
            <b>Survey card ⚕️</b>
            <br>Name: {st.session_state["card"].get("name", "...")}<br>
            Age: {st.session_state["card"].get("age", "...")}
            <br>Gender: {st.session_state["card"].get("gender", "...")}<br>
            Сomplaints: {st.session_state["card"].get("complaints", "...")}
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


def check_data(data: bytes) -> None:
    predictions = get_predictions(data)
    if not predictions:
        pass
    elif predictions["preds"] == "artifact":
        artifact_report()
    else:
        classification_report(predictions)
        plot_predictions(predictions)


def create_medical_card() -> None:
    st.session_state["card"]["name"] = st.text_input("Enter your full name")
    st.session_state["card"]["age"] = st.number_input("How old are you?", step=1)
    st.session_state["card"]["gender"] = st.selectbox("What is your gender?", ["unknown", "man", "woman"])
    st.session_state["card"]["complaint"] = st.text_input("Please describe what is bothering you?")


st.image(f"{GIF_DIR}/circle.gif")
data = load_audio()
if data:
    create_card = st.radio("Do you want to fill out a medical card?", ["Default", "Yes", "No"])
    if create_card == "Yes":
        create_medical_card()
    if (create_card == "Yes" and st.session_state["card"]["complaint"]) or create_card == "No":
        check_data(data)
