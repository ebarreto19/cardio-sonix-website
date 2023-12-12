"""
This module contains class for preprocessing tabular data:
- Encoding categorical features.
- Standardization, normalization numerical features.
"""

__all__ = ["TabularPreprocessor"]

import os
from pathlib import Path
from typing import Union, Literal, Any
import joblib
import pandas as pd
import numpy as np
import os


class TabularPreprocessor:
    """
    This class contains methods for:
    - Splitting features by type (categorical or numerical)
    - Encoding categorical features.
    - Standardization, normalization numerical features.
    - And unite encoded categorical features with normalized numerical features.
    """

    def __init__(self):
        self.__dirname = "preprocessors"
        self.__normalizer = self.__make_preprocessor("Normalizer.joblib")
        self.__encoder = self.__make_preprocessor("OneHotEncoder.joblib")

    def _get_path(self, filename: str) -> str:
        return os.path.join(os.getcwd(), self.__dirname, filename)

    @staticmethod
    def _as_sklearn_input(x: dict[str, int | float]) -> pd.DataFrame:
        return pd.DataFrame(x, columns=list(x.keys()), index=[0])

    def __make_preprocessor(self, filename: str) -> Any:
        path = self._get_path(filename)
        if os.path.exists(path):
            return joblib.load(path)
        raise FileExistsError

    def normalize(self, data: pd.DataFrame) -> np.ndarray:
        data = self._as_sklearn_input(data)
        return self.__normalizer.transform(data)

    def encode(self, data: pd.DataFrame) -> np.ndarray:
        data = self._as_sklearn_input(data)
        return self.__encoder.transform(data).toarray()

    def __call__(self, categorical: dict[str, int], quantity: dict[str, float]) -> np.ndarray:
        quantity = self.normalize(quantity)
        categorical = self.encode(categorical)
        return np.concatenate([quantity, categorical], axis=1)
