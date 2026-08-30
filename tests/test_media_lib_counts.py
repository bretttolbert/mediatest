import os
from dataclasses import dataclass
from pathlib import Path

from tests.test_config import *

from mediatest.path_utils import get_file_ext, get_dir_path_filesize_gb

@dataclass
class MediaFileCounts:
    media: int = 0
    mp3: int = 0
    m4a: int = 0
    lrc: int = 0 # synced lyrics
    txt: int = 0 # unsynced lyrics


def get_media_file_counts(media_lib_path: Path | str) -> MediaFileCounts:
    counts = MediaFileCounts()
    for _, _, files in os.walk(media_lib_path, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            if ext in EXTS_MEDIA:
                counts.media += 1
            if ext == "mp3":
                counts.mp3 += 1
            elif ext == "m4a":
                counts.m4a += 1
            elif ext == "lrc":
                counts.lrc += 1
            elif ext == "txt":
                counts.txt += 1
    print(f"counts.mp3={counts.mp3}")
    print(f"counts.m4a={counts.m4a}")
    print(f"counts.media={counts.media}")
    print(f"counts.lrc={counts.lrc}")
    print(f"counts.txt={counts.txt}")
    print(f"counts.lrc.missing={counts.media - counts.lrc}")
    return counts


def pytest_generate_tests(metafunc): # type: ignore
    media_counts_expected : List[int] = []
    media_counts_actual : List[int] = []
    lrc_counts_expected : List[int] = []
    lrc_counts_actual : List[int] = []
    file_size_limit : List[int] = []
    file_size_expected : List[int] = []
    file_size_actual : List[float] = []
    for lib_idx in range(LIB_COUNT):
        media_lib_path = Path(LIBS_MEDIA_PATH[lib_idx])
        counts = get_media_file_counts(media_lib_path)

        media_counts_expected.append(LIBS_EXPECTED_MEDIA_COUNT[lib_idx])
        media_counts_actual.append(counts.media)

        lrc_counts_expected.append(LIBS_EXPECTED_LRC_COUNT[lib_idx])
        lrc_counts_actual.append(counts.lrc)

        file_size_expected.append(LIBS_EXPECTED_FILESIZE_GB[lib_idx])
        file_size_limit.append(LIBS_TOTAL_FILESIZE_LIMIT_GB[lib_idx])
        lib_file_size_actual = get_dir_path_filesize_gb(media_lib_path)
        print(f"filesize={lib_file_size_actual}")
        file_size_actual.append(lib_file_size_actual)

    if "media_count_expected" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("media_count_expected", media_counts_expected) # type: ignore
    if "media_count_actual" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("media_count_actual", media_counts_actual) # type: ignore

    if "lrc_count_expected" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("lrc_count_expected", lrc_counts_expected) # type: ignore
    if "lrc_count_actual" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("lrc_count_actual", lrc_counts_actual) # type: ignore

    if "file_size_expected" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("file_size_expected", file_size_expected) # type: ignore
    if "file_size_limit" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("file_size_limit", file_size_limit) # type: ignore
    if "file_size_actual" in metafunc.fixturenames: # type: ignore
        metafunc.parametrize("file_size_actual", file_size_actual) # type: ignore


def test_media_count(media_count_expected: int, media_count_actual: int):
    assert media_count_expected == media_count_actual


def test_lrc_count(lrc_count_expected: int, lrc_count_actual: int):
    assert lrc_count_expected == lrc_count_actual


def test_file_size_eq_expected(file_size_actual: float, file_size_expected: int):
    assert file_size_expected == round(file_size_actual)


def test_file_size_lt_limit(file_size_actual: float, file_size_limit: int):
    assert file_size_actual < file_size_limit
