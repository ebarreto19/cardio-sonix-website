"""
This module contains class for preprocessing tabular data:
    - Encoding categorical features.
    - Standardization, normalization numerical features.
"""

__all__ = ["TabularPreprocessor"]

import os
from pathlib import Path
from typing import (
    Optional,
    Union,
    Literal,
    Any
)

import streamlit as st
import joblib
import pandas as pd
import numpy as np


class TabularPreprocessor:
    """
    This class contains methods for:
        - Splitting features by type (categorical or numerical)
        - Encoding categorical features.
        - Standardization, normalization numerical features.
        - And unite encoded categorical features with normalized numerical features.
    """
    def __init__(self,
                 dirname: Optional[str] = "preprocessors",
                 dtype: Optional[np.dtype] = np.float32
                 ):
        self._dtype = dtype
        self.__dirname = dirname
        self.__normalizer = self.__make_preprocessor("Normalizer.joblib")
        self.__encoder = self.__make_preprocessor("OneHotEncoder.joblib")

    def _get_path(self, filename: str) -> str:
        return os.path.join(os.getcwd(), self.__dirname, filename)

    @staticmethod
    def _as_sklearn_input(x: dict[str, int | float]) -> pd.DataFrame:
        return pd.DataFrame(x, columns=list(x.keys()), index=[0])

    @st.cache_resource
    def __make_preprocessor(_self, filename: str) -> Any:
        path = _self._get_path(filename)
        if os.path.exists(path):
            return joblib.load(path)
        raise FileExistsError

    def normalize(self, data: dict[str, float] | pd.DataFrame) -> np.ndarray:
        if not isinstance(data, pd.DataFrame):
            data = self._as_sklearn_input(data)
        return self.__normalizer.transform(data)

    def encode(self, data: dict[str, int] | pd.DataFrame) -> np.ndarray:
        if not isinstance(data, pd.DataFrame):
            data = self._as_sklearn_input(data)
        return self.__encoder.transform(data).toarray()

    def __call__(self, categorical: dict[str, int] | pd.DataFrame, quantity: dict[str, float] | pd.DataFrame) -> np.ndarray:
        quantity = self.normalize(quantity)
        categorical = self.encode(categorical)
        return np.concatenate([quantity, categorical], axis=1, dtype=self._dtype)
