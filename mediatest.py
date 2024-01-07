# !/usr/bin/python3
import os
import re

MUSIC_DIR = "/data/Music/"
EXPECTED_MEDIA_COUNT = 12261

# intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = ["jpg", "webp", "png"]
EXTS_EXTRA = ["pdf"]
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_EXTRA


def get_file_ext(path: str) -> str:
    _, ext = os.path.splitext(path)
    return ext.strip(".")


def test_allowed_exts():
    count = 0
    for _, _, files in os.walk(MUSIC_DIR, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            assert ext in ALLOWED_EXTS, "{} not in allowed extensions".format(name)
    print(count)


def test_media_file_count():
    count_media = 0
    count_mp3 = 0
    count_m4a = 1
    for _, _, files in os.walk(MUSIC_DIR, topdown=False):
        for name in files:
            ext = get_file_ext(name)
            if ext in EXTS_MEDIA:
                count_media += 1
            if ext == "mp3":
                count_mp3 += 1
            elif ext == "m4a":
                count_m4a += 1
    print("count_mp3={}".format(count_mp3))
    print("count_m4a={}".format(count_m4a))
    print("count_media={}".format(count_media))
    assert count_media == EXPECTED_MEDIA_COUNT


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


def test_no_empty_dirs():
    baselevel = len(MUSIC_DIR.split(os.path.sep))
    for root, dirs, _ in os.walk(MUSIC_DIR, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            curlevel = len(fullpath.split(os.path.sep))
            level = curlevel - baselevel
            # 0 = artist dir
            if level == 0:
                assert_directory_contains_subdirectories(fullpath)
            # 1 = album [year] dir
            elif level == 1:
                assert_directory_contains_media(fullpath)
            else:
                assert False, "folder nested too deep: {}".format(fullpath)


def string_contains_trailing_space(s: str) -> bool:
    """Trailing space can causes problems e.g. when burning to a BluRay on Windows,
    I was getting 'file not found' errors for some albums that had trailing space"""
    return bool(s != s.strip())


# @pytest.mark.skip(reason="wip")
def test_album_dir_name():
    # prohibit chars not allowed in windows filenames
    # and other problematic characters
    album_pattern = re.compile(r'[^:\?&#%{}\\\.`$!<>\*"+|=]*\[\d+(-\d+)?\]')
    baselevel = len(MUSIC_DIR.split(os.path.sep))
    count = 0
    match_count = 0
    for root, dirs, _ in os.walk(MUSIC_DIR, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            curlevel = len(fullpath.split(os.path.sep))
            # 0 = artist
            # 1 = album [year]
            if curlevel - baselevel == 1:
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


def test_album_cover_jpg():
    baselevel = len(MUSIC_DIR.split(os.path.sep))
    count = 0
    match_count = 0
    for root, dirs, _ in os.walk(MUSIC_DIR, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            curlevel = len(fullpath.split(os.path.sep))
            # 0 = artist
            # 1 = album [year]
            if curlevel - baselevel == 1:
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
