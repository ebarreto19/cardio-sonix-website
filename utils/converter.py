"""AudioConvertor it's classs for converting audio files to only supported formats"""

__all__ = ["AudioConvertor"]

from typing import Union
import os
import io
import time
from pathlib import Path
import soundfile as sf
from streamlit.runtime.uploaded_file_manager import UploadedFile
import ffmpeg


class AudioConvertor:
    def __init__(self,
                 root_dir: Union[str, Path],
                 valid_extensions: list[str],
                 convert_to: str,
                 ac: int = 1
                 ):
        self.check_sanity(root_dir)
        self.root_dir = root_dir
        self.valid_extensions = valid_extensions
        self.convert_to = convert_to
        self.ac = ac

    @staticmethod
    def check_sanity(root_dir: Union[str, Path]) -> None:
        if not os.path.isdir(root_dir):
            raise ValueError(
                f"Expected argument root_dir should be dirpath, but got {root_dir}"
            )

    def define_location(self, filename: str) -> str:
        return os.path.join(self.root_dir, f"{time.time()}-{filename}")

    @staticmethod
    def load(path: Union[str, Path]) -> sf.SoundFile:
        return sf.SoundFile(path, "r")

    @staticmethod
    def write(path: Union[str, Path], data: io.BytesIO) -> None:
        with open(path, "wb") as f:
            f.write(data)

    def convert(self, in_path: Union[str, Path], out_path: Union[str, Path]) -> None:
        (
            ffmpeg
            .input(in_path)
            .output(
                out_path,
                format=self.convert_to,
                ac=self.ac
            )
            .run()
        )

    def check_format(self, filename: str) -> Union[None, str]:
        if filename.split(".")[-1] not in self.valid_extensions:
            return filename

    @staticmethod
    def clear(paths: list[str, ...]) -> None:
        for path in paths:
            if not os.path.isfile(path):
                raise ValueError(
                    f"Expected argument paths should contain file paths, but got {paths}"
                )
            else:
                os.remove(path)

    def __call__(self, source: UploadedFile) -> io.BytesIO:
        data = io.BytesIO(source.getbuffer())
        if self.check_format(source.name):
            in_path = self.define_location(source.name)
            self.write(in_path, source.getbuffer())
            out_path = self.define_location(source.name)
            self.convert(in_path, out_path)
            data = self.load(out_path)
            self.clear([in_path, out_path])
        return data
