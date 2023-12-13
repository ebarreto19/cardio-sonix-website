"""Docstring"""

__all__ = ["AudioRecorder"]

from typing import Union, AnyStr, Optional
import io
from pathlib import Path
import librosa
import streamlit as st
from st_audiorec import st_audiorec
from .converter import AudioConverter
from utils.variables import ROOT_DIR


class AudioRecorder(AudioConverter):
    __default_extensions = [
        ".wav", ".aac",
        ".ogg", ".mp3",
        ".aiff", ".flac",
        ".ape", ".dsd",
        ".mqa", ".wma",
        ".m4a"
    ]

    def __init__(self,
                 duration: Optional[int] = 10,
                 valid_extensions: Optional[list[str]] = None,
                 convert_to: Optional[str] = "wav",
                 sample_rate: Optional[int] = 22050,
                 mono: Optional[bool] = True
                 ):
        super().__init__(valid_extensions, convert_to, (1 if mono else 2), ROOT_DIR)
        self.duration = duration
        self.sample_rate = sample_rate
        self.mono = mono

    def chunks(self):
        pass

    def __check_duration(self, data: AnyStr | bytes) -> io.BytesIO:
        audio, sr = librosa.load(io.BytesIO(data), sr=self.sample_rate, mono=self.mono)
        duration = librosa.get_duration(y=audio, sr=self.sample_rate)
        if duration >= self.duration:
            return io.BytesIO(data)
        else:
            st.error(
                f"Oops! Length of the heartbeat audio recording "
                f"must be at least {self.duration} seconds, "
                f"but the length is {round(duration, 2)} seconds. "
                f"Please try again.",
                icon="😮"
            )

    def _record_audio(self) -> AnyStr:
        data = st_audiorec()
        if data is not None:
            return self.__check_duration(data)

    def _load_audio(self) -> Union[bytes, None]:
        data = st.file_uploader(
            label=f"Upload an audio file of your heartbeat "
                  f"that is at least {self.duration} seconds long.",
            type=self.__default_extensions
        )
        if data:
            st.audio(data)
            data = self.__call__(data)
            return self.__check_duration(data)

    def get_audio(self) -> io.BytesIO:
        choice = st.sidebar.selectbox(
            label="Do you want to upload or record an audio file?",
            options=["Upload 📁", "Record 🎤"]
        )
        if choice == "Upload 📁":
            return self._load_audio()
        return self._record_audio()
