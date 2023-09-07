"""AudioConverter it's classs for converting audio files to only supported formats"""

__all__ = ["AudioConverter"]

from typing import Union, AnyStr, Optional
import os
import io
from pathlib import Path
from subprocess import Popen, PIPE
import streamlit as st
from streamlit.runtime.uploaded_file_manager import UploadedFile
import ffmpeg
from .variables import ROOT_DIR


class AudioConverter:
    def __init__(self,
                 valid_extensions: list[str],
                 convert_to: Optional[str] = "wav",
                 ac: Optional[int] = 1
                 ):
        self.valid_extensions = valid_extensions
        self.convert_to = convert_to
        self.ac = ac
        self.root_dir = ROOT_DIR

    def convert(self, path: str | Path) -> AnyStr:
        return Popen(
            ["ffmpeg", "-hide_banner", "-i", f"{path}", "-f", f"{self.convert_to}", "-"],
            stdout=PIPE
        ).stdout.read()

    def check_extension(self, filename: str | Path) -> Union[None, str]:
        if filename.split(".")[-1] not in self.valid_extensions:
            return filename

    def define_location(self, file_id: str, extension: str) -> str:
        return os.path.join(self.root_dir, f"{file_id}.{extension}")

    @staticmethod
    def write(path: Union[str, Path], data: io.BytesIO | bytes) -> None:
        with open(path, "wb") as f:
            f.write(data)

    def __call__(self, source: UploadedFile) -> bytes | AnyStr:
        data = source.getvalue()

        if self.check_extension(source.name):
            in_path = self.define_location(
                source.file_id, source.name.split(".")[-1]
            )

            try:
                self.write(in_path, source.getbuffer())
                data = self.convert(in_path)
            except Exception as e:
                st.error("We're sorry, something happened to the server ⚡️")
            else:
                return data
            finally:
                if os.path.exists(in_path):
                    os.remove(in_path)

        return data
