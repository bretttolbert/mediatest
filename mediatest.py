# !/usr/bin/python3
from __future__ import annotations
import yaml
import pytest
import os
import re
import sys
from typing import List

from dataclasses import dataclass
from datetime import time

from dataclass_wizard import YAMLWizard  # type: ignore

"""
I run this script with pytest to keep my music folders organized.
"""

# For running tests on the yaml file output by mediascan
# E.g. for ID3-tag tests
# E.g. testing if year is a valid year or something weird like 0
MEDIASCAN_FILES_PATH = "../mediascan/files.yaml"

# LIB1 is my primary music library
LIB1_MEDIA_PATH = "/data/Music/"
LIB1_EXPECTED_MEDIA_COUNT = 13512
LIB1_EXPECTED_LRC_COUNT = 5969
LIB1_TOTAL_FILESIZE_LIMIT_GB = (
    96  # Goal: Keep LIB1 small enough to fit on 128 GB tablets
)

# LIB2 is for everything that doesn't fit in LIB1
LIB2_MEDIA_PATH = "/data/MusicOther/"
LIB2_EXPECTED_MEDIA_COUNT = 1845
LIB2_EXPECTED_LRC_COUNT = 516

# intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = ["jpg", "webp", "png"]
EXTS_LYRICS = ["lrc", "txt"]
EXTS_EXTRA = ["pdf"]
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_EXTRA


@dataclass
class Mediafile:
    """
    Mediafile dataclass

    """

    path: str
    size: int
    format: str
    title: str | int | float | bool
    artist: str | bool | int
    album: str | int | float | bool | time
    genre: str
    year: int
    duration: int


@dataclass
class Data(YAMLWizard):
    """
    Data dataclass

    """

    mediafiles: list[Mediafile]


@pytest.fixture(scope="session")
def files_yaml_file() -> Data:
    yaml_fname: str = MEDIASCAN_FILES_PATH
    data = None
    with open(yaml_fname, "r") as stream:
        try:
            data = Data.from_yaml(stream)  # type: ignore
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return data  # type: ignore


def test_yaml_no_zero_years(files_yaml_file: Data):
    for f in files_yaml_file.mediafiles:
        assert f.year > 0


def test_yaml_no_years_gt_present(files_yaml_file: Data):
    for f in files_yaml_file.mediafiles:
        assert f.year <= 2024


def get_file_ext(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.strip(".")


def get_path_depth(path: str):
    return len(path.strip(os.path.sep).split(os.path.sep))


def assert_directory_contains_media(path: str):
    """Asserts that directory contains at least one media file
    and that directory does not contain subdirectories"""
    ret = False
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            assert False
        elif os.path.isfile(os.path.join(path, f)) and get_file_ext(f) in EXTS_MEDIA:
            ret = True
    assert ret


def assert_directory_contains_subdirectories(path: str):
    """Asserts that directory contains at least one subdirectory
    and that directory does not contain any files"""
    ret = False
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            assert False
        elif os.path.isdir(os.path.join(path, f)):
            ret = True
    assert ret


def directory_contains_cover_jpg(path: str) -> bool:
    """Returns whether directory contains cover.jpg or not"""
    return "cover.jpg" in os.listdir(path)


def string_contains_trailing_space(s: str) -> bool:
    """Trailing space can causes problems e.g. when burning to a BluRay on Windows,
    I was getting 'file not found' errors for some albums that had trailing space"""
    return bool(s != s.strip())


def do_test_allowed_exts(media_path: str):
    count = 0
    for _, _, files in os.walk(media_path, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            assert ext in ALLOWED_EXTS, "{} not in allowed extensions".format(name)
    print(count)


def do_test_media_file_count(
    media_path: str, expected_media_count: int, expected_lrc_count: int
):
    count_media = 0
    count_mp3 = 0
    count_m4a = 1
    count_lrc = 0  # synced lyrics
    count_txt = 0  # unsynced lyrics
    for _, _, files in os.walk(media_path, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            if ext in EXTS_MEDIA:
                count_media += 1
            if ext == "mp3":
                count_mp3 += 1
            elif ext == "m4a":
                count_m4a += 1
            elif ext == "lrc":
                count_lrc += 1
            elif ext == "txt":
                count_txt += 1
    print("count_mp3={}".format(count_mp3))
    print("count_m4a={}".format(count_m4a))
    print("count_media={}".format(count_media))
    print("count_lrc={}".format(count_lrc))
    print("count_txt={}".format(count_txt))
    print("missing lrc count={}".format(count_media - count_lrc))
    assert count_media == expected_media_count
    assert count_lrc == expected_lrc_count


def do_test_no_empty_dirs(media_path: str):
    base_depth = get_path_depth(media_path)
    for root, dirs, _ in os.walk(media_path, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            current_depth = get_path_depth(fullpath)
            relative_depth = current_depth - base_depth
            # 1 = artist dir
            if relative_depth == 1:
                assert_directory_contains_subdirectories(fullpath)
            # 2 = album [year] dir
            elif relative_depth == 2:
                assert_directory_contains_media(fullpath)
            else:
                assert False, "folder nested too deep: {}".format(fullpath)


# @pytest.mark.skip(reason="wip")
def do_test_album_dir_name(media_path: str):
    # prohibit chars not allowed in windows filenames
    # and other problematic characters
    album_pattern = re.compile(r'[^:\?&#%{}\\\.`$!<>\*"+|=]*\[\d+(-\d+)?\]')
    base_depth = get_path_depth(media_path)
    count = 0
    match_count = 0
    for root, dirs, _ in os.walk(media_path, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            current_depth = get_path_depth(fullpath)
            # 1 = artist dir
            # 2 = album [year] dir
            if current_depth - base_depth == 2:
                count += 1
                if album_pattern.match(name) and not string_contains_trailing_space(
                    name
                ):
                    # test album year format (4 digits)
                    album_year = 0
                    try:
                        tokens: List[str] = re.findall(r"\[(\d{4})\]", name)
                        album_year = int(tokens[-1])
                        match_count += 1
                        print(album_year)
                    except Exception:
                        print(
                            "bad album dir name format (invalid year): {}".format(
                                fullpath
                            )
                        )
                else:
                    print("bad album dir name format: {}".format(fullpath))
    print(
        "test_dir_name: bad album dir format: {} out of {}".format(
            count - match_count, count
        )
    )
    print(
        "test_dir_name: good album dir format: {} out of {}".format(match_count, count)
    )
    assert count == match_count, "One or more invalid album names"


# TODO: Write test to disallow periods in filenames except as file extension separator
# TODO: Write test to find duplicated artists, e.g. "The Dave Matthews Band" vs "Dave Matthews Band"
# TODO: Validate filenames, prohibited chars in filenames


def do_test_album_cover_jpg(media_path: str):
    base_depth = get_path_depth(media_path)
    count = 0
    match_count = 0
    for root, dirs, _ in os.walk(media_path, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            current_depth = get_path_depth(fullpath)
            # 1 = artist dir
            # 2 = album [year] dir
            if current_depth - base_depth == 2:
                count += 1
                if directory_contains_cover_jpg(fullpath):
                    match_count += 1
                else:
                    print("Missing cover.jpg dir: {}".format(fullpath))
    print(
        "test_album_cover_jpg: Missing cover.jpg dir: {} out of {}".format(
            count - match_count, count
        )
    )
    print(
        "test_album_cover_jpg: has cover.jpg dir: {} out of {}".format(
            match_count, count
        )
    )
    assert count == match_count, "One or more album dirs missing cover.jpg"


# begin tests


@pytest.mark.parametrize("media_path", [LIB1_MEDIA_PATH, LIB2_MEDIA_PATH])
def test_allowed_exts(media_path: str):
    do_test_allowed_exts(media_path)


@pytest.mark.parametrize(
    "media_path,expected_media_count,expected_lrc_count",
    [
        (LIB1_MEDIA_PATH, LIB1_EXPECTED_MEDIA_COUNT, LIB1_EXPECTED_LRC_COUNT),
        (LIB2_MEDIA_PATH, LIB2_EXPECTED_MEDIA_COUNT, LIB2_EXPECTED_LRC_COUNT),
    ],
)
def test_media_file_count(
    media_path: str, expected_media_count: int, expected_lrc_count: int
):
    do_test_media_file_count(media_path, expected_media_count, expected_lrc_count)


@pytest.mark.parametrize("media_path", [LIB1_MEDIA_PATH, LIB2_MEDIA_PATH])
def test_no_empty_dirs(media_path: str):
    do_test_allowed_exts(media_path)


@pytest.mark.parametrize("media_path", [LIB1_MEDIA_PATH, LIB2_MEDIA_PATH])
def test_album_dir_name(media_path: str):
    do_test_album_dir_name(media_path)


@pytest.mark.parametrize("media_path", [LIB1_MEDIA_PATH, LIB2_MEDIA_PATH])
def test_album_cover_jpg(media_path: str):
    do_test_album_cover_jpg(media_path)


def test_lib1_total_filesize_limit():
    """Ensures that the total filesize of my LIB1 folder does not exceed
    LIB1_TOTAL_FILESIZE_LIMIT_GB
    Reason: I sync LIB1 (my primary music collection) to my 128 GB tablet,
    so I need to keep it small enough to fit on said tablet.
    I put all my other music in LIB2 (MusicOther), where the size is not limited.
    """
    size = 0
    for path, _, files in os.walk(LIB1_MEDIA_PATH):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    print(size)
    size_gb = size / 1024**3
    print("size_gb=", size_gb)
    assert size_gb < LIB1_TOTAL_FILESIZE_LIMIT_GB
