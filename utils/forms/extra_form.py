"""Docstring"""

__all__ = ["ExtraForm"]

from typing import Optional, Any
import streamlit as st


class MultiLabelEncoder:
    _no_yes: dict[str, int] = {"no": 0, "yes": 1}
    _sex: dict[str, int] = {"female": 0, "male": 1}

    _gen_health: dict[str, int] = {
        "excellent": 0, "very good": 1,
        "good": 2, "fair": 3, "poor": 4,
    }

    _age_category: dict = {
        "18-24": 0, "25-29": 1,
        "30-34": 2, "35-39": 3,
        "40-44": 4, "45-49": 5,
        "50-54": 6, "55-59": 7,
        "60-64": 8, "65-69": 9,
        "70-74": 10, "75-79": 11,
        "80 or older": 12
    }

    _race: dict[str, int] = {
        "white": 0, "black": 1, "asian": 2,
        "american indian / alaskan native": 3,
        "other": 4, "hispanic": 5
    }

    _diabetic: dict[str, int] = {
        "no": 0, "yes": 1,
        "yes (during pregnancy)": 2,
        "no, borderline diabetes": 3
    }

    def __init__(self):
        self.__fields = [
            self._no_yes,
            self._sex,
            self._race,
            self._age_category,
            self._diabetic,
            self._gen_health
        ]

    def __len__(self) -> int:
        return len(self.__fields)

    @staticmethod
    def options(field: dict[str, int]) -> list[str, ...]:
        return [
            label.lower()
            for label in list(field.keys())
        ]

    def encode(self, category: str) -> int:
        category = category.lower()
        for field in self.__fields:
            if (label := field.get(category, None)) is not None:
                return label


class ExtraForm(MultiLabelEncoder):
    def __init__(self,
                 name: Optional[str] = "extra_form",
                 sidebar: Optional[bool] = False,
                 output_format: Optional[Any] = None
                 ):
        super().__init__()
        self.output_format = output_format
        self.__form = st.form(name) if not sidebar else st.sidebar.form(name)

    def is_smoking(self) -> int:
        is_smoking = self.__form.selectbox(
            "Have you smoked at least 100 cigarettes in your entire life?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_smoking)

    def is_drinking(self) -> int:
        is_drinking = self.__form.selectbox(
            "Do you have more than 14 drinks of alcohol (male) or more than 7 (female) in a week?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_drinking)

    def is_stroke(self) -> int:
        is_stroke = self.__form.selectbox(
            "Did you have a stroke?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_stroke)

    def is_asthma(self) -> int:
        is_asthma = self.__form.selectbox(
            "Do you have asthma?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_asthma)

    def is_skin_cancer(self) -> int:
        is_skin_cancer = self.__form.selectbox(
            "Do you have skin cancer?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_skin_cancer)

    def is_kidney_disease(self) -> int:
        is_kidney_disease = self.__form.selectbox(
            "Do you have kidney disease?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_kidney_disease)

    def is_diffwalking(self) -> int:
        is_diffwalking = self.__form.selectbox(
            "Do you have serious difficulty walking or climbing stairs?",
            options=self.options(self._no_yes)
        )
        return self.encode(is_diffwalking)

    def get_sex(self) -> int:
        sex = self.__form.selectbox(
            "Are you a male or a female?",
            options=self.options(self._sex)
        )
        return self.encode(sex)

    def get_age_category(self) -> int:
        age_category = self.__form.selectbox(
            "What is your age category? (years)",
            options=self.options(self._age_category)
        )
        return self.encode(age_category)

    def get_race(self) -> int:
        race = self.__form.selectbox(
            "What race are you?",
            options=self.options(self._race)
        )
        return self.encode(race)

    def get_diabetic(self) -> int:
        diabetic = self.__form.selectbox(
            "Have you ever had diabetes?",
            options=self.options(self._diabetic)
        )
        return self.encode(diabetic)

    def get_physical_activity(self) -> int:
        physical_activity = self.__form.selectbox(
            "Have you played any sports (running, biking, etc.) in the past month?",
            options=self.options(self._no_yes)
        )
        return self.encode(physical_activity)

    def get_gen_health(self) -> int:
        gen_health = self.__form.selectbox(
            "How can you define your general health?",
            options=self.options(self._gen_health)
        )
        return self.encode(gen_health)

    def get_physical_health(self) -> int:
        physical_health = self.__form.number_input(
            "For how many days during the past 30 days was your physical health not good?",
            min_value=0, max_value=30, step=1, value=0
        )
        if self.output_format:
            return self.output_format(physical_health)
        return physical_health

    def get_mental_health(self) -> int:
        mental_health = self.__form.number_input(
            "For how many days during the past 30 days was your mental health not good?",
            min_value=0, max_value=30, step=1, value=0
        )
        if self.output_format:
            return self.output_format(mental_health)
        return mental_health

    def get_sleep_time(self) -> float:
        sleep_time = self.__form.number_input(
            "How many hours on average do you sleep?",
            min_value=0.0, max_value=18.0, step=1.0, value=7.0
        )
        if self.output_format:
            return self.output_format(sleep_time)
        return sleep_time

    def get_bmi(self) -> float:
        bmi = self.__form.number_input(
            "Enter your BMI (Body mass index)",
            min_value=5.0, max_value=251.1, step=1.0, value=25.0,
            help="Body mass index is a value that allows you to assess the degree of correspondence "
                 "between a person’s weight and his height and "
                 "thereby indirectly judge whether the weight is insufficient, normal or excessive. "
                 "Important when determining indications for the need for treatment. "
                 "Body mass index is calculated using the formula: weight (kg) / height (m)2.",
        )
        if self.output_format:
            return self.output_format(bmi)
        return bmi

    def quantity(self) -> dict[str, int | float]:
        return {
            "BMI": self.get_bmi(),
            "PhysicalHealth": self.get_physical_health(),
            "MentalHealth": self.get_mental_health(),
            "SleepTime": self.get_sleep_time()
        }

    def categorical(self) -> dict[str, int]:
        return {
            "Smoking": self.is_smoking(),
            "AlcoholDrinking": self.is_drinking(),
            "Stroke": self.is_stroke(),
            "DiffWalking": self.is_diffwalking(),
            "Sex": self.get_sex(),
            "AgeCategory": self.get_age_category(),
            "Race": self.get_race(),
            "Diabetic": self.get_diabetic(),
            "PhysicalActivity": self.get_physical_activity(),
            "GenHealth": self.get_gen_health(),
            "Asthma": self.is_asthma(),
            "KidneyDisease": self.is_kidney_disease(),
            "SkinCancer": self.is_skin_cancer()
        }

    @property
    def submit_button(self) -> bool:
        return self.__form.form_submit_button(":blue[Scan] 🩺")

    def get_all_form(self):
        categorical = self.categorical()
        quantity = self.quantity()
        if self.submit_button:
            return {
                "categorical": categorical,
                "quantity": quantity
            }
