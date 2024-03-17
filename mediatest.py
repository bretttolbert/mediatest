# !/usr/bin/python3
import pytest
import os
import re

MEDIA_PATH = "/data/Music/"
# MEDIA_PATH = "D:\\Music\\"
EXPECTED_MEDIA_COUNT = 13260
EXPECTED_LRC_COUNT = 6427

# MEDIA_PATH = "/media/brett/MUSIC_20240107/Music/"
# EXPECTED_MEDIA_COUNT = 12082

# MEDIA_PATH = "/media/brett/MUSIC-2023-10-15/Music/"
# EXPECTED_MEDIA_COUNT = 11434

# intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = ["jpg", "webp", "png"]
EXTS_LYRICS = ["lrc", "txt"]
EXTS_EXTRA = ["pdf"]
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_EXTRA


@pytest.fixture(scope="session")
def media_path():
    return MEDIA_PATH


def get_file_ext(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.strip(".")


def get_path_depth(path: str):
    return len(path.strip(os.path.sep).split(os.path.sep))


def test_allowed_exts(media_path: str):
    count = 0
    for _, _, files in os.walk(media_path, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            assert ext in ALLOWED_EXTS, "{} not in allowed extensions".format(name)
    print(count)


def test_media_file_count(media_path: str):
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
    assert count_media == EXPECTED_MEDIA_COUNT
    assert count_lrc == EXPECTED_LRC_COUNT


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


def test_no_empty_dirs(media_path: str):
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


def string_contains_trailing_space(s: str) -> bool:
    """Trailing space can causes problems e.g. when burning to a BluRay on Windows,
    I was getting 'file not found' errors for some albums that had trailing space"""
    return bool(s != s.strip())


# @pytest.mark.skip(reason="wip")
def test_album_dir_name(media_path: str):
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
                    match_count += 1
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


def test_album_cover_jpg(media_path: str):
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
