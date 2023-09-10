"""
Page from interactive charts and
data marts on research topics.
"""

from typing import Sequence
import os
import streamlit as st
from pathlib import Path
import pandas as pd
from utils import DataMart


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"
DATA_DIR: Path = ASSETS_DIR / "data"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Research"
PAGE_ICON: str = "🔬"


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)


# Page head
st.title(":green[_Statistics and heart disease_] 📊")
st.write(
    """
    <div class="alert alert-block alert-info" style="font-size:20px; background-color: #044447; font-family:verdana; color: #52d9c7; border-radius: 10px; border: 0px #533078 solid">
        Sometimes statistics can say much more than the text in an article. 
        On this page you will see interactive graphs 
        with which you can interact to clearly see 
        the influence of various factors on the heart.
    </div>
    """,
    unsafe_allow_html=True
)
st.image(f"{GIF_DIR}/research.gif")


survey = DataMart(
    title="Survey Data",
    link="https://www.cdc.gov/brfss/annual_data/annual_2020.html",
    filepath=os.path.join(DATA_DIR, "survey.csv"),
    description="""
    Originally, the data come from the CDC and is a major part 
    of the Behavioral Risk Factor Surveillance System (BRFSS), 
    which conducts annual telephone surveys to gather data on the health status of U.S. residents. 
    As the CDC describes: 
    "Established in 1984 with 15 states, 
    BRFSS now collects data in all 50 states 
    as well as the District of Columbia and three U.S. territories. 
    BRFSS completes more than 400,000 adult interviews each year, 
    making it the largest continuously conducted health survey system in the world.". 
    The most recent dataset (as of February 15, 2022) includes data from 2020. 
    It consists of 401,958 rows and 279 columns. 
    The vast majority of columns are questions asked to respondents about their health status, 
    such as "Do you have serious difficulty walking or climbing stairs?" 
    or "Have you smoked at least 100 cigarettes in your entire life? [Note: 5 packs = 100 cigarettes]". 
    In this dataset, I noticed many different factors (questions) that directly or indirectly influence heart disease, 
    so I decided to select the most relevant variables from it and 
    do some cleaning so that it would be usable for machine learning projects.
    """,
    column_config="",
    unsafe_allow_html=True
)


clinical_records = DataMart(
    title="Heart failure clinical records",
    link="https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records",
    filepath=os.path.join(DATA_DIR, "clinical-records.csv"),
    description="""
    This data contains the medical records of 299 patients who had heart failure, 
    collected during their follow-up period, where each patient profile has 13 clinical features.
    """,
    column_config="",
    unsafe_allow_html=True
)


heartbeat = DataMart(
    title="Heartbeat records",
    link="https://www.kaggle.com/datasets/mersico/dangerous-heartbeat-dataset-dhd",
    filepath=os.path.join(DATA_DIR, "heartbeat.csv"),
    description="""
    The data contains audio recordings of the heart and class labels. 
    There are several types of heart sounds that can be dangerous symptoms. 
    The dataset contains these types of sounds and labels of their class. 
    The dataset is clean and has no gaps. 
    The audio files are of varying lengths, between 1 second and 30 seconds. 
    Total 585 audio files with class label. 
    It can be applied in multi-class classification of various human heart rate abnormalities.
    """,
    column_config="",
    unsafe_allow_html=True
)


# Data tabs
tab1, tab2, tab3 = st.tabs([
    survey.title,
    clinical_records.title,
    heartbeat.title
])


def tabs(datamart: DataMart) -> None:
    st.header(f":blue[{datamart.title}]", divider="blue")
    st.write(
        datamart.description,
        unsafe_allow_html=datamart.unsafe_allow_html,
    )
    st.write("<br><br>", unsafe_allow_html=True)
    st.dataframe(datamart.dataframe, use_container_width=True)
    st.subheader(":blue[Describe]", divider="blue")
    st.dataframe(datamart.dataframe.describe(), use_container_width=True)


with tab1:
    tabs(survey)


with tab2:
    tabs(clinical_records)


with tab3:
    heartbeat.dataframe.set_index("class", inplace=True)
    st.header(f":blue[{heartbeat.title}]", divider="blue")
    st.write(
        heartbeat.description,
        unsafe_allow_html=heartbeat.unsafe_allow_html,
    )

    st.write("<br><br>", unsafe_allow_html=True)
    heartbeat_type = st.selectbox(
        options=heartbeat.dataframe.index.tolist(),
        label="Please select heartbeat type 🫀"
    )

    table = heartbeat.dataframe.loc["{}".format(heartbeat_type)]
    st.audio(os.path.join(DATA_DIR, f"audio/{heartbeat_type}.wav"))
    st.write(
        f"""
        <div class="alert alert-block alert-info" style="font-size:20px; 
        background-color: #0b0e22; font-family:verdana; 
        color: #353cbd; 
        border-radius: 10px; 
        border: 0px #533078 solid">{table["description"]}
        </div>
        """,
        unsafe_allow_html=True
    )
