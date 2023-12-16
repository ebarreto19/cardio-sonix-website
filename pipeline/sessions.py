__all__ = ["PredictionSession"]

import streamlit as st
import numpy as np
from huggingface_hub import hf_hub_download
from onnxruntime import InferenceSession


class PredictionSession:
    def __init__(self, filename: str, classes: list[str, ...] | tuple[str, ...]):
        self.__session = self._make_session(filename)
        self.__input_names = self.__get_input_names()
        self.__classes = classes

    @property
    def session(self) -> InferenceSession:
        return self.__session

    def classes(self) -> list:
        return self.__classes

    @staticmethod
    @st.cache_resource(show_spinner="Please wait for the models to be loaded...")
    def _make_session(filename: str) -> InferenceSession:
        model = hf_hub_download("Cardionix/cardionet-v2", filename)
        return InferenceSession(model)

    def __get_input_names(self) -> list[str, ...]:
        return [
            data.name
            for data in self.__session.get_inputs()
        ]

    @staticmethod
    def _softmax(logites: np.ndarray) -> np.ndarray[np.float32]:
        exp = np.exp(logites)
        return exp / np.sum(exp)

    def forward(self, inputs: dict[str, np.ndarray]) -> np.ndarray:
        logites = self.__session.run(None, inputs)[0]
        logites = logites.squeeze()
        return self._softmax(logites)

    def _get_input(self, *args: np.ndarray) -> dict[str, np.ndarray]:
        return dict(zip(self.__input_names, args))

    def _get_output(self, probs: np.ndarray) -> dict[str, float]:
        return dict(zip(self.__classes, probs))

    def _get_predict(self, probs: np.ndarray) -> str:
        return self.__classes[probs.argmax()]

    def __call__(self, *inputs: np.ndarray) -> tuple[str, dict[str, float]]:
        inputs = self._get_input(*inputs)
        probs = self.forward(inputs)
        outputs = self._get_output(probs)
        predict = self._get_predict(probs)
        return predict, outputs
