import os
from typing import Tuple, Union
from pathlib import Path
import pandas as pd

import torchaudio
from torch import Tensor
from torch.utils.data import Dataset


def load_item(file_id: str, path: str, ext_audio: str, df: pd.DataFrame) -> Tuple[Tensor, int, str]:
    txt = df.loc[df['id'] == file_id, ["text"]]
    transcript = txt.values[0][0]
    file_audio = file_id + ext_audio
    file_audio = os.path.join(path, "data", file_id[:2], file_audio)

    # Load audio
    waveform, sample_rate = torchaudio.load(file_audio)

    return waveform, sample_rate, transcript


# ----------------------------
# Sound Dataset
# ----------------------------
class SoundDS(Dataset):
    _ext_audio = ".flac"

    def __init__(self, df: pd.DataFrame, root: Union[str, Path], ):
        # Get string representation of 'root' in case Path object is passed
        root = os.fspath(root)
        self._df = df
        self._path = root
        self._walker = sorted(str(p.stem) for p in Path(root).glob('*/*/*' + self._ext_audio))

    # ----------------------------
    # Number of items in dataset
    # ----------------------------
    def __len__(self) -> int:
        return len(self._walker)

    # ----------------------------
    # Get i'th item in dataset
    # ----------------------------
    def __getitem__(self, n: int) -> Tuple[Tensor, int, str]:
        file_id = self._walker[n]
        return load_item(file_id, self._path, self._ext_audio, self._df)
