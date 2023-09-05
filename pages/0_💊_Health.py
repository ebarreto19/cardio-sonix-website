"""
Page with information about a healthy lifestyle
to maintain the tone of the heart muscle.
"""

import streamlit as st
from pathlib import Path


# --- PATH SETTINGS ---
APP_DIR: Path = Path(__file__).parent.parent if "__file__" in locals() else Path.cwd().parent
ASSETS_DIR: Path = APP_DIR / "assets"
GIF_DIR: Path = ASSETS_DIR / "gif"
IMAGES_DIR: Path = ASSETS_DIR / "images"

# --- GENERAL SETTINGS ---
PAGE_TITLE: str = "Health"
PAGE_ICON: str = "💊"


st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON
)


# Page head
st.image(f"{IMAGES_DIR}/pulse-black.jpg")
col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    st.subheader("Lifespan")
    st.image(f"{IMAGES_DIR}/life-cycle.jpg")
    st.write(
        """
        Human life is fragile and not so long. 
        Every action you take can affect your health in the future. 
        One way or another, almost all of us hit the threshold of average life expectancy, which is about 74.5 years. 
        Just as important is not only the numbers that you live, but also the quality of this life. 
        Summarizing all of the above, I want to convey to you the value of your time and health, 
        because they have their limits.
        """
    )


with col2:
    st.subheader("Heart and life path")
    st.image(f"{IMAGES_DIR}/dark-heart.png")
    st.write(
        """
        Half of patients with heart failure live no more than five years, 
        a significant proportion of them die within just one year. 
        The heart plays a big role in the quality and duration of human life, 
        so it is important to learn how to detect problems of the cardiovascular system in advance.
        """
    )


# Page body
st.header("How to keep a life streak?")
st.write(
    """
    Now that you understand the importance of the contribution of the cardiovascular system to your life expectancy, 
    I would like to give a couple of useful tips without further ado. 
    This is a brief summary of the most important factors that affect the heart which I know.
    """
)
st.image(f"{GIF_DIR}/life-streak.gif")


# First raw
col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    st.subheader("Alcohol 🥃")
    st.image(f"{IMAGES_DIR}/alcohol.jpg")
    st.write(
        """
        ##### Strongest cellular poison 🧪
        Being the strongest cellular poison, alcohol damages the cells of the heart muscle 
        and increases blood pressure (even with a single dose - for several days), 
        poisoning the nervous and cardiovascular systems. 
        A sharp increase in blood pressure can lead to a hypertensive crisis, 
        myocardial infarction and stroke. 
        
        ##### The most harmful alcohol 🍺
        The most harmful alcohol can be called beer, 
        the cobalt contained in the foam increases the load on the heart muscle.
        
        ##### Bovine heart 🫀
        With frequent use of alcohol, 
        an excess amount of fat accumulates in the heart muscle, 
        it is reborn, becomes flabby. 
        The heart becomes weak, enlarged and can hardly cope with its work, 
        the so-called "alcoholic" or "bovine" heart develops. 
        The result of such disorders is hypertension and premature atherosclerosis.
        """
    )


with col2:
    st.subheader("Smoking 🚬")
    st.image(f"{GIF_DIR}/cigarette-smoke.gif")
    st.write(
        """
        ##### Nicotine
        Nicotine causes an increase in blood pressure and heart rate, 
        and carbon monoxide causes heart failure.
        
        ##### Tobacco smoke
        Tobacco smoke contains carbon monoxide (carbon monoxide), 
        which prevents the blood from carrying oxygen. 
        Therefore, to supply the body with oxygen, the heart has to work harder. 
        Smoking also contributes to the deposition of fats in the blood vessels, 
        constricts them and increases blood pressure.
        
        ##### Cardiac spasm
        Cardiac spasm is the most common complication of smoking. 
        The result of such a spasm can be a myocardial infarction - the necrosis of a section of the 
        heart muscle due to a violation of its nutrition.
        """
    )

# Second raw
col1, col2 = st.columns([0.5, 0.5], gap="large")

with col1:
    st.subheader("Food 🥗")
    st.image(f"{IMAGES_DIR}/food.jpg")
    st.write(
        """
        ##### Healthy fruits 🥝
        Almost all fresh fruits are good for the heart. 
        Therefore, in the summer you need to eat as much as possible: 
        * apples 🍏
        * pears 🍐
        * plums 
        * all kinds of berries 🍒
        
        ##### Dark-colored berries 🫐
        By the way, all dark-colored berries (blueberries, blackberries, currants) not only replenish 
        the body's vitamin supply and nourish the heart muscle, 
        but also increase the level of hemoglobin in the blood.
        
        ##### Calcium
        The heart system needs not only plant foods, but also calcium. 
        It can be obtained from: 
        * milk 🥛
        * cheese 🧀
        * yogurt
        
        ##### Dairy-free with calcium
        But if you can’t eat dairy products, 
        the lack of calcium is compensated by the consumption:
        * fish (salmon and sardines) 🍣
        * seeds (sesame and chia)
        * nuts 🥜
        * figs
        
        ##### Harmful to the heart: 
        * smoked and raw smoked sausages 🫘
        * caviar
        * all products containing margarine
        """
    )


with col2:
    st.subheader("Sleep 💤")
    st.image(f"{GIF_DIR}/sleep.gif")
    st.write(
        """
        ##### The heart needs sleep too 
        Sleep is a time of rest for the whole body. 
        Even the heart, which works day and night, naturally slows down during sleep. 
        Therefore, poor heart function caused by heart disease can deprive the body of normal rest during sleep. 
        Moreover, the relationship between heart function and the sleep process operates in two directions. 
        For example, sleep-related respiratory disorders have been shown to play an important role 
        in the development of certain types of heart and vascular disease.
        
        ##### How much sleep? 
        On average, the duration of sleep should be about seven hours. 
        Adults are recommended to sleep for seven to nine hours, 
        but for people over 65, six to eight hours is enough.
        """
    )
