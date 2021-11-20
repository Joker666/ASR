import os
import zipfile
from pathlib import Path
from typing import List, Tuple, Union

import pandas as pd
import torchaudio
from torch import Tensor
from torch.utils.data import Dataset
from torchaudio.datasets.utils import (download_url)

# character we will filter from text sequence, this can be change according
# to your needs
FILTER_CHARS = [
    '"', '%', "'", ',', '-', '.', '/', '\x93', '\x94', '\u200c', '\u200d', '‘',
    '’', '“', '”', '…', '!', ':'
]

# english character set to discard
ENGLISH = {'0', '1', '2', '3', '4', '5', 'B', 'L', 'T', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'l', 'm', 'n', 'o',
           'p', 'r', 's', 't', 'u', 'v', 'w', 'x', 'z'}


def clean(text):
    """Clean text"""
    for c in FILTER_CHARS:
        if c in text:
            text = text.replace(c, '')
    return text


def contains_english_chars(text):
    if ENGLISH.intersection(set(text)):
        return True
    return False


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

    def __init__(self, root: Union[str, Path],
                 d_keys: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f'],
                 download: bool = False,
                 df: pd.DataFrame = None):
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

            for key in d_keys:
                url = base_url + key + ext_archive
                archive = os.path.join(root, FOLDER_IN_ARCHIVE + '_' + key + ext_archive)
                if not os.path.isfile(archive):
                    download_url(url, root)

            self._path = os.path.join(root, FOLDER_IN_ARCHIVE)
            utt_path = self._path + '/utt_spk_text.tsv'
            flac_list = sorted(str(p.stem) for p in Path(self._path).glob('*/*/*' + self._ext_audio))
            flac_set = set(flac_list)

            if not os.path.isdir(self._path):
                unpack_all_in_dir(root, ext_archive)

            data = []
            unique_chars = set()
            max_text_len = 0
            max_text = ''
            en_bn_mixed = 0

            with open(utt_path, 'r') as fp:
                lines = fp.readlines()
                for line in lines:
                    line = line.strip(' \n')
                    line = line.split('\t')
                    file_name, text = line[0], line[2]

                    if file_name in flac_set:
                        text = clean(text)

                        # skip english text
                        if contains_english_chars(text):
                            en_bn_mixed += 1
                            continue

                        data.append({'id': file_name, 'text': text})

                        # create unique chars set
                        for c in text:
                            unique_chars.add(c)

                        # find max text sequence length, text
                        text_len = len(text)
                        if max_text_len < text_len:
                            max_text_len = text_len
                            max_text = text

            unique_chars = sorted(unique_chars)

            df = pd.DataFrame.from_dict(data)
            df.sort_values(by=['id'], inplace=True)
            self._df = df

            print(f'utt entry       : {len(lines)}')
            print(f'unique chars    : {len(unique_chars)}')
            print(f'data            : {len(data)}')
            print(f"max text length : {max_text_len}")
            print(f'max text        : {max_text}')
            print(f'en bn mixed     : {en_bn_mixed}')
            print(f'flac audio files: {len(flac_list)}')
            print(f'flac_dic        : {len(flac_set)}')

    # ----------------------------
    # Number of items in dataset
    # ----------------------------
    def __len__(self) -> int:
        return len(self._df.index)

    # ----------------------------
    # Get i'th item in dataset
    # ----------------------------
    def __getitem__(self, n: int) -> Tuple[Tensor, int, str]:
        file_id = self._df.iloc[n]['id']
        return load_item(file_id, self._path, self._ext_audio, self._df)
