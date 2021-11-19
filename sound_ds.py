import os, zipfile
from typing import Tuple, Union
from pathlib import Path
import pandas as pd

import torchaudio
from torch import Tensor
from torch.utils.data import Dataset
from torchaudio.datasets.utils import (download_url, extract_archive)


def load_item(file_id: str, path: str, ext_audio: str, df: pd.DataFrame) -> Tuple[Tensor, int, str]:
    txt = df.loc[df['id'] == file_id, ["text"]]
    transcript = txt.values[0][0]
    file_audio = file_id + ext_audio
    file_audio = os.path.join(path, "data", file_id[:2], file_audio)

    # Load audio
    waveform, sample_rate = torchaudio.load(file_audio)

    return waveform, sample_rate, transcript

def unpack_all_in_dir(_dir, extension):
    for item in os.listdir(_dir):  # loop through items in dir
        abs_path = os.path.join(_dir, item)  # absolute path of dir or file
        if item.endswith(extension):  # check for ".zip" extension
            file_name = os.path.abspath(abs_path)  # get full path of file
            zip_ref = zipfile.ZipFile(file_name)  # create zipfile object
            zip_ref.extractall(_dir)  # extract file to dir
            zip_ref.close()  # close file
        elif os.path.isdir(abs_path):
            unpack_all_in_dir(abs_path)  # recurse this function with inner folder


# ----------------------------
# Sound Dataset
# ----------------------------
class SoundDS(Dataset):
    _ext_audio = ".flac"

    def __init__(self, df: pd.DataFrame, root: Union[str, Path], download: bool = False):
        # Get string representation of 'root' in case Path object is passed
        root = os.fspath(root)
        if not os.path.isdir(root):
            os.mkdir(path=root)

        if download is False:
            self._df = df
            self._path = root
        else:
            FOLDER_IN_ARCHIVE = "asr_bengali"

            ext_archive = ".zip"
            base_url = "http://www.openslr.org/resources/53/asr_bengali_"
            # d_keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
            d_keys = ['1', '2']

            for key in d_keys:
                url = os.path.join(base_url + key, url + ext_archive)
                archive = os.path.join(root, FOLDER_IN_ARCHIVE + '_' + key)
                if not os.path.isfile(archive):
                    download_url(url, root)
            
            unpack_all_in_dir(root)

            df = pd.read_csv(root, FOLDER_IN_ARCHIVE + '/utt_spk_text.tsv', sep='\t', header=None)
            df.columns = ["id", "hash", "text"]
            df.sort_values(by=['id'], inplace=True)
            self._df = df
            self._path = os.path.join(root, FOLDER_IN_ARCHIVE)
        
        self._walker = sorted(str(p.stem) for p in Path(self._path).glob('*/*/*' + self._ext_audio))


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
