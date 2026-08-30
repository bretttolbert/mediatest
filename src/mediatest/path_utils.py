import os
from pathlib import Path


def get_file_ext(path: str | Path) -> str:
    _, ext = os.path.splitext(path)
    return ext.strip(".")


def get_path_depth(path: str | Path):
    return len(str(path).strip(os.path.sep).split(os.path.sep))
