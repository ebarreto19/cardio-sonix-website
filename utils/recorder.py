"""Docstring"""

__all__ = ["AudioRecorder"]

from typing import Union, AnyStr, Optional
import io
from pathlib import Path
import librosa
import streamlit as st
from audiorecorder import audiorecorder
from .converter import AudioConvertor
from .variables import ROOT_DIR


class AudioRecorder:
    def __init__(self,
                 duration: Optional[float] = 10.0,
                 valid_extensions: Optional[list[str]] = None,
                 convert_to: Optional[str] = "wav"
                 ):
        self.duration = duration
        self.convert_to = convert_to
        if not valid_extensions:
            valid_extensions = [
                "wav", "mp3", "ogg",
                "flac", "m4a"
            ]
        self.valid_extensions = valid_extensions

    @staticmethod
    def __get_length(audio: AnyStr) -> float:
        audio, sr = librosa.load(io.BytesIO(audio), sr=None)
        return librosa.get_duration(y=audio, sr=sr)

    def _record_audio(self) -> io.BytesIO | None:
        data = audiorecorder()

        if data:
            data = data.export().read()
            duration = self.__get_length(data)

            if duration >= self.duration:
                st.audio(data)
                return io.BytesIO(data)
            else:
                st.error(
                    f"Oops! Length of the heartbeat audio recording "
                    f"must be at least 10 seconds, but the length is {duration} seconds. "
                    f"Please try again.",
                    icon="😮"
                )

    def _load_audio(self) -> Union[io.BytesIO, None]:
        data = st.file_uploader(
            label="Upload an audio file of your heartbeat "
                  "that is at least 10 seconds long.",
            type=[
                ".wav", ".aac", ".ogg",
                ".mp3", ".aiff", ".flac",
                ".ape", ".dsd", ".mqa", ".wma"
            ]
        )

        if data:
            st.audio(data.getvalue())
            return AudioConvertor(
                root_dir=ROOT_DIR,
                valid_extensions=self.valid_extensions,
                convert_to=self.convert_to
            )(data)

    def get_audio(self) -> None | io.BytesIO:
        choice = st.sidebar.selectbox(
            label="Do you want to upload or record an audio file?",
            options=["Upload 📁", "Record 🎤"]
        )
        return self._load_audio() if choice == "Upload 📁" else self._record_audio()
