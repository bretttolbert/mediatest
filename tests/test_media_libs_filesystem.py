# !/usr/bin/python3
from __future__ import annotations
import pytest
import os
import re

from tests.test_config import *


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
            assert ext in ALLOWED_EXTS, f"{name} not in allowed extensions"
    print(count)


# '’' is prohibited because it's problematic with ID3 tags (converts to '?' if ripped from CD),
# so I need to check the tags on these files and change '?' to ''' if needed.
# also disallow both regular question mark and weird unicode question mark
# >>> ord('?')
# 63
# >>> ord('？')
# 65311

FILENAME_PROHIBITED_CHARS = "’？?"


def do_test_filenames(media_path: str):
    failing = []
    for _, _, files in os.walk(media_path, topdown=False):
        for name in files:
            for c in FILENAME_PROHIBITED_CHARS:
                if c in name:
                    fail = f"character {c} not allowed in filename {name}"
                    print(fail)
                    failing.append(fail)
    print(f"do_test_filenames fail count: {len(failing)}")
    assert failing == []


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


# begin filesystem tests


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_allowed_exts(media_path: str):
    do_test_allowed_exts(media_path)


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_filenames(media_path: str):
    do_test_filenames(media_path)


@pytest.mark.parametrize("lib_idx", list(range(LIB_COUNT)))
def test_media_file_count(lib_idx: int):
    do_test_media_file_count(
        LIBS_MEDIA_PATH[lib_idx],
        LIBS_EXPECTED_MEDIA_COUNT[lib_idx],
        LIBS_EXPECTED_LRC_COUNT[lib_idx],
    )


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_no_empty_dirs(media_path: str):
    do_test_allowed_exts(media_path)


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_album_dir_name(media_path: str):
    do_test_album_dir_name(media_path)


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_album_cover_jpg(media_path: str):
    do_test_album_cover_jpg(media_path)


def get_lib_total_filesize_gb(media_path: str) -> float:
    size = 0
    for path, _, files in os.walk(media_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    print(size)
    size_gb = size / GIGABYTE
    print("size_gb=", size_gb)
    return size_gb


@pytest.mark.parametrize("lib_idx", list(range(LIB_COUNT)))
def test_lib_total_filesize_limit(lib_idx: int):
    """Ensures that the total filesize of LIB folder does not exceed LIBS_TOTAL_FILESIZE_LIMIT_GB"""
    media_path = LIBS_MEDIA_PATH[lib_idx]
    size_gb = get_lib_total_filesize_gb(media_path)
    assert size_gb < LIBS_TOTAL_FILESIZE_LIMIT_GB[lib_idx]


@pytest.mark.parametrize("lib_idx", list(range(LIB_COUNT)))
def test_lib_expected_filesize(lib_idx: int):
    """Ensures that the total filesize of LIB folder is equal to LIBS_EXPECTED_FILESIZE_GB"""
    media_path = LIBS_MEDIA_PATH[lib_idx]
    size_gb = get_lib_total_filesize_gb(media_path)
    assert round(size_gb) == LIBS_EXPECTED_FILESIZE_GB[lib_idx]
