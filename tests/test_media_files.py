import os
from pathlib import Path

from mediatest.path_utils import get_file_ext

from tests.test_config import *

# TODO: Write test to disallow periods in filenames except as file extension separator
# TODO: Validate filenames, prohibited chars in filenames

# '’' is prohibited because it's problematic with ID3 tags (converts to '?' if ripped from CD),
# so I need to check the tags on these files and change '?' to ''' if needed.
# also disallow both regular question mark and weird unicode question mark
# >>> ord('?')
# 63
# >>> ord('？')
# 65311

FILENAME_PROHIBITED_CHARS = "’？?"


def get_media_file_paths(media_lib_path: Path) -> List[Path]:
    ret : set[Path] = set()
    for root, _, files in os.walk(media_lib_path, topdown=False):
        for name in files:
            fullpath = Path(root) / name
            ret.add(fullpath)
    return list(ret)


def pytest_generate_tests(metafunc): # type: ignore
    media_file_paths : List[Path] = []
    for lib_idx in range(LIB_COUNT):
        media_lib_path = Path(LIBS_MEDIA_PATH[lib_idx])
        media_file_paths.extend(get_media_file_paths(media_lib_path))
    metafunc.parametrize("media_file_path", media_file_paths) # type: ignore


def test_media_file_filename(media_file_path: Path):
    """Verifies that media file filename doesn't break any naming rules"""
    for c in FILENAME_PROHIBITED_CHARS:
        assert c not in media_file_path.name


def test_media_file_file_ext(media_file_path: Path):
    """Verifies that media file file extension is in allowed_exts list"""
    ext = get_file_ext(media_file_path)
    assert ext in ALLOWED_EXTS, f"'{ext}' not in allowed extensions"
