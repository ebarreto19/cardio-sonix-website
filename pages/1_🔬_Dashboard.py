"""
Page from interactive charts and
data marts on research topics.
"""

from typing import Sequence, Literal, Optional
import os
from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit.column_config import NumberColumn, Column
from utils import DataMart, DataWidgets


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


# Survey | data mart
survey_data = DataMart(
    title="Survey data 📝",
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
    unsafe_allow_html=True,
    column_config={
        "HeartDisease": Column(
            "HeartDisease",
            help="""
            Respondents that have ever reported having coronary heart disease (CHD) 
            or myocardial infarction (MI)"""
        ),

        "BMI": Column(
            "BMI",
            help="""
            Body Mass Index (BMI) is a value that allows you to assess the degree of correspondence between a person's mass and his height, 
            and thereby indirectly judge whether the mass is insufficient, normal or excessive. 
            It is important in determining the indications for the need for treatment.
            """
        ),

        "Smoking": Column(
            "Smoking",
            help="""
            Have you smoked at least 100 cigarettes in your entire life? 
            [Note: 5 packs = 100 cigarettes]
            """
        ),

        "AlcoholDrinking": Column(
            "AlcoholDrinking",
            help="""
            Heavy drinkers (adult men having more than 14 drinks per week 
            and adult women having more than 7 drinks per week
            """
        ),

        "Stroke": Column("Stroke", help="(Ever told) (you had) a stroke?"),

        "PhysicalHealth": Column(
            "PhysicalHealth",
            help="""
            Now thinking about your physical health, 
            which includes physical illness and injury, 
            for how many days during the past 30
            """
        ),

        "MentalHealth": Column(
            "MentalHealth",
            help="""
            Thinking about your mental health, 
            for how many days during the past 30 days was your mental health not good?
            """
        ),

        "DiffWalking": Column("DiffWalking", help="Do you have serious difficulty walking or climbing stairs?"),
        "Sex": Column("Sex", help="Are you male or female?"),
        "AgeCategory": Column("AgeCategory", help="Fourteen-level age category"),

        "GenHealth": Column("GenHealth", help="well-being"),
        "PhysicalActivity": Column("PhysicalActivity", help="adults who reported doing physical activity or exercise during the past 30 days other than their regular job"),

        "Race": Column("Race", help="obviously"),
        "Diabetic": Column("Diabetic", help="obviously"),
        "SleepTime": Column("SleepTime", help="Number of hours of sleep"),
        "Asthma": Column("Asthma", help="obviously"),
        "KidneyDisease": Column("KidneyDisease", help="obviously"),
        "SkinCancer": Column("SkinCancer", help="obviously")
    }
)


# Heart failure clinical records | data mart
clinical_records = DataMart(
    title="Heart failure clinical records 💉",
    link="https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records",
    filepath=os.path.join(DATA_DIR, "clinical-records.csv"),
    description="""
    This data contains the medical records of 299 patients who had heart failure, 
    collected during their follow-up period, where each patient profile has 13 clinical features.
    """,
    unsafe_allow_html=True,
    column_config={
        "age": Column("age", help="age of the patient [years]"),
        "sex": Column("sex", help="Are you male or female?"),
        "DEATH_EVENT": Column("DEATH_EVENT", help="Patcinet died?"),
        "anaemia": Column("anaemia", help="Decrease of red blood cells or hemoglobin (boolean)"),
        "creatinine_phosphokinase": Column("creatinine_phosphokinase", help="Level of the CPK enzyme in the blood (mcg/L)"),
        "diabetes": Column("diabetes", help="If the patient has diabetes (boolean)"),
        "ejection_fraction": Column("ejection_fraction", help="Percentage of blood leaving the heart at each contraction (percentage)"),
        "high_blood_pressure": Column("high_blood_pressure", help="If the patient has hypertension (boolean)"),
        "platelets": Column("platelets", help="Platelets in the blood (kiloplatelets/mL)"),
        "serum_creatinine": Column("serum_creatinine", help="Level of serum creatinine in the blood (mg/dL)"),
        "serum_sodium": Column("serum_sodium", help="Level of serum sodium in the blood (mEq/L)")
    }
)


# Heartbeat records | data mart
heartbeat_sound = DataMart(
    title="Heartbeat sound 💓",
    link="https://www.kaggle.com/datasets/mersico/dangerous-heartbeat-dataset-dhd",
    filepath=os.path.join(DATA_DIR, "heartbeat-sound.csv"),
    description="""
    The data contains audio recordings of the heart and class labels. 
    There are several types of heart sounds that can be dangerous symptoms. 
    The dataset contains these types of sounds and labels of their class. 
    The dataset is clean and has no gaps. 
    The audio files are of varying lengths, between 1 second and 30 seconds. 
    Total 585 audio files with class label. 
    It can be applied in multi-class classification of various human heart rate abnormalities.
    """,
    unsafe_allow_html=True
)


survey_tab, clinical_tab, heartbeat_tab = st.tabs([
    survey_data.title, clinical_records.title, heartbeat_sound.title
])
widgets = DataWidgets()


with survey_tab:
    widgets.table_widget(survey_data)
    form = st.form("survey_form")
    widgets.submit_form(form, survey_data)
    widgets.charts_widget(survey_data)


with clinical_tab:
    widgets.table_widget(clinical_records)
    form = st.form("clinical_form")
    widgets.submit_form(form, clinical_records)
    widgets.charts_widget(clinical_records)


with heartbeat_tab:
    heartbeat_sound.dataframe.set_index("class", inplace=True)
    st.header(f":blue[{heartbeat_sound.title}]", divider="blue")
    st.write(
        heartbeat_sound.description,
        unsafe_allow_html=heartbeat_sound.unsafe_allow_html,
    )

    st.write("<br><br>", unsafe_allow_html=True)
    heartbeat_type = st.selectbox(
        options=heartbeat_sound.dataframe.index.tolist(),
        label="Please select heartbeat type 🫀"
    )

    table = heartbeat_sound.dataframe.loc[f"{heartbeat_type}"]
    st.audio(os.path.join(DATA_DIR, f"audio/{heartbeat_type}.wav"))
    st.subheader(f":blue[About {heartbeat_type} category 🩺]", divider="blue")
    st.write(table["description"], unsafe_allow_html=True)
