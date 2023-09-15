"""Docstring"""

__all__ = ["DataMart", "DataWidgets"]

from typing import Optional, Iterable
from pathlib import Path
from typing import Literal
import os
import time
from dataclasses import dataclass

import plotly.express as px
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from sklearn.preprocessing import LabelEncoder
from .variables import DATA_DIR


@dataclass
class DataMart:
    filepath: str | Path
    color: Optional[str] = "#353cbd"
    background_color: Optional[str] = "#0b0e22"
    title: Optional[str] = "Some data mart"
    link: Optional[str] = None
    dataframe: pd.DataFrame = None
    description: Optional[str] = None
    unsafe_allow_html: Optional[bool] = True
    column_config: Optional[dict] = None
    hide_index: Optional[bool] = True

    def insert_link(self) -> None:
        self.description = f"""{self.description}<a href="{self.link}">Link to data source.</a>"""

    def insert_html(self) -> None:
        self.description = f"""
        <div class="alert alert-block alert-info" style="font-size:20px; 
        background-color: {self.background_color}; 
        font-family:verdana; 
        color: {self.color}; 
        border-radius: 10px; 
        border: 0px #533078 solid">{self.description}</div>
        """

    #@st.cache_data(show_spinner=False)
    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.filepath)
        return df.drop(df.columns[df.columns.str.contains("unnamed", case=False)], axis=1, inplace=False)

    @staticmethod
    def to_list(dataframe: pd.DataFrame) -> list[str, ...]:
        return dataframe.dropna().index.tolist()

    def select(self, dtypes: list[Literal["str", "object", "int64", "float64"], ...]) -> pd.DataFrame:
        return self.dataframe[
            [col
             for col, dtype in self.dataframe.dtypes.items()
             if dtype in dtypes]
        ]

    def get_corr(self) -> pd.DataFrame:
        dataframe = self.dataframe.copy()
        for column in self.select(dtypes=["object"]).columns.tolist():
            dataframe[column] = LabelEncoder().fit(
                dataframe[column]
            ).transform(dataframe[column])
        return dataframe.corr().round(2)

    def __post_init__(self) -> None:
        if not self.dataframe:
            self.dataframe = self.load_data()
        if self.unsafe_allow_html:
            if self.link:
                self.insert_link()
            if self.description:
                self.insert_html()


class DataWidgets:
    def __init__(self):
        self.graphs = {
            "histogram": px.histogram,
            "bar": px.bar,
            "box": px.box,
            "violin": px.violin,
            "scatter": px.scatter,
        }
        self._init_dashboard()
        self.__graph_type = st.session_state.get("graph_type", None)
        self.__display_mode = st.session_state.get("display_mode", None)
        self.chart_params = None

    def _init_dashboard(self) -> None:
        st.sidebar.subheader(":gray[Dashboard]", divider="gray")
        st.sidebar.radio(
            "Select display mode:",
            ["Data", "Stats", "Heatmap",
             "Categorical features", "Quantitative features"],
            key="display_mode"
        )
        st.sidebar.selectbox(
            label="Select graph type:",
            options=self.graphs.keys(),
            key="graph_type"
        )

    def table_widget(self, datamart: DataMart) -> None:
        content = {
            "Data": datamart.dataframe,
            "Stats": datamart.dataframe.describe(),
            "Heatmap": datamart.get_corr().style.background_gradient(cmap="plasma"),
            "Categorical features": datamart.select(dtypes=["object"]),
            "Quantitative features": datamart.select(dtypes=["int64", "float64"])
        }

        st.header(f":blue[{datamart.title}]", divider="blue")
        st.write(datamart.description, unsafe_allow_html=datamart.unsafe_allow_html)
        st.write("<br><br>", unsafe_allow_html=True)

        if self.__display_mode:
            st.subheader(f":blue[{self.__display_mode}]", divider="blue")
            st.dataframe(
                content[self.__display_mode],
                column_config=datamart.column_config,
                use_container_width=True,
                hide_index=True
                if self.__display_mode not in ["Stats", "Heatmap"]
                else False
            )

    def charts_widget(self, datamart: DataMart) -> None:
        graph = self.graphs[self.__graph_type]
        fig = graph(data_frame=datamart.dataframe, **self.chart_params)
        st.subheader(f":blue[{self.__graph_type.capitalize()} chart]", divider="blue")
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    def __form_axis(self,
                    form: DeltaGenerator,
                    quantitative_cols: list[str, ...],
                    categorical_cols: list[str, ...]
                    ) -> None:

        self.chart_params.update({
            "x": form.selectbox(
                label="Select a column for the X axis:",
                options=quantitative_cols
                if self.__graph_type in ["histogram", "scatter"]
                else categorical_cols
            )
        })

        if self.__graph_type != "histogram":
            self.chart_params.update({
                "y": form.selectbox(
                    label="Select a column for the Y axis:",
                    options=quantitative_cols
                )
            })

    def __form_cols(self,
                    form: DeltaGenerator,
                    categorical_cols: list[str, ...]
                    ) -> None:

        color = form.selectbox(
            label="Select a category to highlight:",
            options=["Without highlight", *categorical_cols]
        )
        facet_col = form.selectbox(
            label="Select a category to separate:",
            options=["Without separate", *categorical_cols]
        )

        if color != "Without highlight":
            self.chart_params.update({"color": color})
        if facet_col != "Without separate":
            self.chart_params.update({"facet_col": facet_col})

    def submit_form(self, form: DeltaGenerator, datamart: DataMart) -> None:
        self.chart_params = {}
        categorical_cols = datamart.select(dtypes=["object"]).columns
        quantitative_cols = datamart.select(dtypes=["int64", "float64"]).columns
        self.__form_axis(form, quantitative_cols, categorical_cols)
        self.__form_cols(form, categorical_cols)
        form.form_submit_button("Plot chart 📊")

