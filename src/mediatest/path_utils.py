import os
from pathlib import Path
from typing import List


KILOBYTE = 10**3
MEGABYTE = 10**6
GIGABYTE = 10**9



def get_file_ext(path: str | Path) -> str:
    """Gets the file extension of the given file path, exluding the '.' character."""
    _, ext = os.path.splitext(path)
    return ext.strip(".")


def get_path_depth(path: str | Path) -> int:
    """Gets the depth of the given path relative to the root directory,
    which has a depth of 1"""
    return len(str(path).strip(os.path.sep).split(os.path.sep))


def is_dir_with_subdirs(path: str | Path, strict: bool=False) -> bool:
    """
    With strict=False:
    Returns True if path points to a directory containing at least one subdirectory
    and zero or more files
    With strict=True:
    Returns True if path points to a directory containing at least one subdirectory 
    and only containing subdirectories (i.e. zero files)
    """
    if not os.path.isdir(path):
        return False
    subdir_count = 0
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            subdir_count += 1
        else:
            if strict:
                return False
    return subdir_count > 0


def is_dir_with_files(path: Path, file_exts: List[str]) -> bool:
    """Returns True if directory contains at least one file with
    a file extension matching any of the extensions in file_exts
    and the directory does not contain subdirectories
    file_exts : a list of file extensions without the '.' character
    e.g. ['mp3', 'm4a']
    """
    ret = False
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            return False
        elif os.path.isfile(os.path.join(path, f)) and get_file_ext(f) in file_exts:
            ret = True
    return ret


def get_dir_path_filesize_gb(path: Path | str) -> float:
    """Recursively calculates total filesize of the given directory path"""
    size = 0
    for path, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    size_gb = size / GIGABYTE
    return size_gb
