"""
Contains a classes for audio preprocessing and feature extraction:
    - audio loading
    - clipping or padding
    - extraction MFCCs
    - converting to numpy dtypes
"""

__all__ = ["AudioPreprocessor"]

from typing import Literal, Optional, Union
from os import PathLike
import numpy as np
import librosa
import torch
import torchaudio.transforms as T
from torch.nn import Module, Sequential


class SafeLoader(Module):
    def __init__(self,
                 sample_rate: Optional[int] = 22050,
                 duration: Optional[int] = 10,
                 mono: Optional[bool] = True,
                 ):
        super().__init__()
        self.sample_rate = sample_rate
        self.duration = duration
        self.mono = mono
        self.length = self.duration * self.sample_rate

    def forward(self, source: Union[str, bytes, PathLike]) -> torch.Tensor:
        """
        Performs loading of an audio sample, data preprocessing, augmentation and feature extraction step by step.
        Finally returns a set of features cast to a tensor type.

        Args:
            source: (str) path to the audio sample file
        """
        waveform, _ = librosa.load(source, sr=self.sample_rate, mono=self.mono)
        waveform = librosa.util.fix_length(waveform, size=self.length)
        return torch.tensor(np.expand_dims(waveform, axis=0), dtype=torch.float32)


class MFCCExtractor(Module):
    r"""Create the Mel-frequency cepstrum coefficients from an audio signal.

    .. devices:: CPU CUDA

    .. properties:: Autograd TorchScript

    By default, this calculates the MFCC on the DB-scaled Mel spectrogram.
    This is not the textbook implementation, but is implemented here to
    give consistency with librosa.

    This output depends on the maximum value in the input spectrogram, and so
    may return different values for an audio clip split into snippets vs. a
    a full clip.

    Args:
        sample_rate (int, optional): Sample rate of audio signal. (Default: ``22050``)
        n_mfcc (int, optional): Number of mfc coefficients to retain. (Default: ``52``)
        n_mels (int, optional): Number of mell filterbanks. (Default: ``52``)
        n_fft (bool, optional): Size of FFT, creates n_fft // 2 + 1 bins. (Default: 400)
        win_length (int, optional): Window size. (Default: n_fft)
        hop_length (int, optional): Length of hop between STFT windows. (Default: win_length // 2)
        average_by (string, optional): Average mffcs by frequency or time axis. (Default: None)
    Example
        >>> extractor = MFCCExtractor()
        >>> waveform, sample_rate = torcwhaudio.load("test.wav", normalize=True)
        >>> mfcc = extractor(waveform)

    See also:
        :py:func:`torchaudio.functional.melscale_fbanks` - The function used to
        generate the filter banks.
    """
    def __init__(self,
                 sample_rate: Optional[int] = 22050,
                 n_fft: Optional[int] = 2048,
                 win_length: Optional[int] = 2048,
                 hop_length: Optional[int] = 1024,
                 n_mels: Optional[int] = 52,
                 n_mfcc: Optional[int] = 52,
                 average_by: Optional[Literal["time", "mfcc"]] = None
                 ):

        super().__init__()
        self.average_by = average_by
        self.average_dict = {
            "mfcc": 0,
            "time": 1,
        }

        self.mfcc_extractor = T.MFCC(
            sample_rate=sample_rate,
            n_mfcc=n_mfcc,
            melkwargs={
                "n_fft": n_fft,
                "n_mels": n_mels,
                "win_length": win_length,
                "hop_length": hop_length,
                "mel_scale": "htk"
            }
        )

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        """
        Extract MFCC coefficients and average them.

        :param waveform: audio sample represented as an ``Tensor`` with a set of amplitudes.
        """
        mfcc = self.mfcc_extractor(waveform).squeeze().T
        if self.average_by:
            mfcc = mfcc.mean(self.average_dict[self.average_by])
        return mfcc.unsqueeze(0)


class AudioPreprocessor(Module):
    def __init__(self,
                 sample_rate: Optional[int] = 22050,
                 duration: Optional[int] = 10,
                 mono: Optional[bool] = True,
                 n_fft: Optional[int] = 2048,
                 win_length: Optional[int] = 2048,
                 hop_length: Optional[int] = 1024,
                 n_mels: Optional[int] = 52,
                 n_mfcc: Optional[int] = 52,
                 average_by: Optional[Literal["time", "mfcc"]] = None,
                 dtype: Optional[np.dtype] = np.float32
                 ):
        super().__init__()
        self._dtype = dtype
        self.__preprocessor = Sequential(
            SafeLoader(
                sample_rate=sample_rate,
                duration=duration, mono=mono
            ),
            MFCCExtractor(
                sample_rate, n_fft,
                win_length, hop_length,
                n_mels, n_mfcc, average_by
            )
        )

    def forward(self, source: Union[str, bytes, PathLike]) -> np.ndarray:
        return self.__preprocessor(source).numpy().astype(self._dtype)
