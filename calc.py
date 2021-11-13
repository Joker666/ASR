import os
from pathlib import Path

_ext_txt = ".trans.txt"
_ext_audio = ".flac"


def add(x, y):
    return x + y


def subtract(x, y):
    return x - y


# Get string representation of 'root' in case Path object is passed
root = os.fspath("./asr_bengali")

walker = sorted(str(p.stem) for p in Path(root).glob('*/*/*' + _ext_audio))
print(len(walker))
print(walker[0])
