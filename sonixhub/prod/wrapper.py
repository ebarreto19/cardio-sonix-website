"""
Docstring
"""

__all__ = ["BaseWrapper"]


from typing import Union, Literal
from os import PathLike
import torch
import torch.nn.functional as F
from torch.nn import Module
import numpy as np


class BaseWrapper(Module):
    def __init__(self,
                 classes: Union[tuple[str, ...], list[str, ...]],
                 model: Module,
                 pipeline: Module,
                 device: Literal["cpu", "cuda", "auto"],
                 weights_path: Union[str, PathLike]
                 ):
        super().__init__()
        self.classes = classes
        self.model = model
        self.pipeline = pipeline
        self.device = self.define_device() if device == "auto" else torch.device(device)
        self.weights_path = weights_path
        self.define_model()

    @staticmethod
    def define_device() -> torch.device:
        return torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    def define_model(self):
        state_dict = torch.load(self.weights_path)
        self.model.load_state_dict(state_dict)
        self.model.to(self.device)
        self.model.eval()
        self.freeze()

    def freeze(self):
        for param in self.model.parameters():
            param.requires_grad = False

    @staticmethod
    def to_list(x: torch.Tensor) -> np.ndarray:
        return list(map(float, x.detach().cpu().numpy()))

    def label_decoding(self, preds: torch.Tensor):
        return self.classes[preds] if len(preds.shape) == 0 else list(map(lambda x: self.classes[x], preds))

    def forward(self, source: Union[str, bytes, PathLike]) -> torch.Tensor:
        output = self.pipeline(source)
        logites = self.model(output.to(self.device))
        probs = F.softmax(logites, dim=0)
        preds = torch.argmax(probs, dim=0)
        return {
            "preds": self.label_decoding(preds),
            "probs": self.to_list(probs),
            "classes": self.classes
        }
