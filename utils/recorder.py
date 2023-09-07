"""Docstring"""

__all__ = ["AudioRecorder"]

from typing import Union, AnyStr, Optional
import io
from pathlib import Path
import librosa
import streamlit as st
from audiorecorder import audiorecorder
from .converter import AudioConverter


class AudioRecorder:
    def __init__(self,
                 duration: Optional[float] = 10.0,
                 valid_extensions: Optional[list[str]] = None,
                 convert_to: Optional[str] = "wav"
                 ):
        self.duration = duration

        if not valid_extensions:
            valid_extensions = [
                "wav", "mp3", "ogg",
                "flac", "m4a"
            ]

        self.converter = AudioConverter(
            valid_extensions=valid_extensions,
            convert_to=convert_to
        )

    def __check_duration(self, data: AnyStr | bytes) -> io.BytesIO | None:
        audio, sr = librosa.load(io.BytesIO(data), sr=None)
        duration = librosa.get_duration(y=audio, sr=sr)

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

    def _record_audio(self) -> AnyStr | None:
        data = audiorecorder()
        if data:
            return self.__check_duration(data.export().read())

    def _load_audio(self) -> Union[bytes, None]:
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
            data = self.converter(data)
            return self.__check_duration(data)

    def get_audio(self) -> None | io.BytesIO:
        choice = st.sidebar.selectbox(
            label="Do you want to upload or record an audio file?",
            options=["Upload 📁", "Record 🎤"]
        )
        return self._load_audio() if choice == "Upload 📁" else self._record_audio()
