"""Docstring"""

__all__ = ["DataMart"]

from typing import Optional, Iterable
from pathlib import Path
import os
from dataclasses import dataclass
import pandas as pd
import streamlit as st


@dataclass
class DataMart:
    filepath: str | Path
    color: Optional[str] = "#353cbd"
    background_color: Optional[str] = "#0b0e22"
    title: Optional[str] = "Some data mart"
    link: Optional[str] = "https://link-to-source.com"
    dataframe: pd.DataFrame = None
    description: Optional[str] = "Description of the data"
    unsafe_allow_html: Optional[bool] = True
    column_config: Optional[dict] = None

    def insert_link(self, text: str) -> str:
        return f"""{text}<a href="{self.link}">Link to data source.</a>"""

    def insert_html(self, text: str) -> str:
        return f"""
        <div class="alert alert-block alert-info" style="font-size:20px; 
        background-color: {self.background_color}; 
        font-family:verdana; 
        color: {self.color}; 
        border-radius: 10px; 
        border: 0px #533078 solid">{text}</div>
        """

    @st.cache_data(show_spinner=False)
    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(self.filepath)

    def __post_init__(self) -> None:
        if not self.dataframe:
            self.dataframe = self.load_data()
        if self.unsafe_allow_html:
            description = self.insert_link(self.description)
            self.description = self.insert_html(description)
