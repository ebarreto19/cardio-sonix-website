"""
Docstring
"""

__version__ = "1.0.0"
__all__ = ["get_base_cardionet"]

import torch
import streamlit as st
from .wrapper import BaseWrapper
from ..architect import BaselineRNNModel
from ..transforms import ETLPipeline


@st.cache_resource
def get_base_cardionet() -> BaseWrapper:
    model = BaselineRNNModel(
        input_shape=(1, 52),
        encoder_depth=[2048, 1024, 512],
        rnn_depth=[256, 128],
        decoder_depth=[64, 32, 3],
        activation="relu"
    )

    pipeline = ETLPipeline(
        sample_rate=22050,
        duration=10,
        mono=True,
        extractor="MFCC",
        extractor_kwargs={
            "n_fft": 2048,
            "win_length": 2048,
            "hop_length": 1024,
            "n_mels": 52,
            "n_mfcc": 52,
            "average_by": "time"
        }
    )

    return BaseWrapper(
        classes=["artifact", "healthy", "abnormal"],
        model=model,
        pipeline=pipeline,
        device="auto",
        weights_path="sonixhub/weights/cardionet-v1.0.0.pth"
    )
