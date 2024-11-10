# !/usr/bin/python3
from __future__ import annotations
import yaml
import pytest
import os
import re
import sys
from typing import List

from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import YAMLWizard  # type: ignore

"""
I run this script with pytest to keep my music folders organized.
"""

KILOBYTE = 10**3
MEGABYTE = 10**6
GIGABYTE = 10**9
PRESENT_YEAR: int = datetime.now().year

# For running tests on the yaml file output by mediascan
# E.g. for ID3-tag tests
# E.g. testing if year is a valid year or something weird like 0
MEDIASCAN_FILES_PATH = "../mediascan/files.yaml"
MINIMUM_FILESIZE = 10 * KILOBYTE

# LIB1 is my primary music library - party mix: rock/pop/hip-hop
LIB1_MEDIA_PATH = "/data/Music/"
LIB1_EXPECTED_MEDIA_COUNT = 13040
LIB1_EXPECTED_LRC_COUNT = 5531
# Goal: Keep LIB1 small enough to fit on 128 GB tablets or 100 GB (triple-layer) blu-rays
LIB1_TOTAL_FILESIZE_LIMIT_GB = 100

# LIB2 is for everything that doesn't fit in LIB1
# LIB2 is for all the music that isn't suitable for parties
# LIB2 genres: classical music, classic country, soundtracks, doom metal,
# the smiths, the cure, anything too whiny or melancholic
LIB2_MEDIA_PATH = "/data/MusicOther/"
LIB2_EXPECTED_MEDIA_COUNT = 3305
LIB2_EXPECTED_LRC_COUNT = 949
# Goal: Keep LIB2 small enough to fit on 128 GB tablets or 100 GB (triple-layer) blu-rays
LIB2_TOTAL_FILESIZE_LIMIT_GB = 100

# intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = ["jpg", "webp", "png"]
EXTS_LYRICS = ["lrc", "txt"]
EXTS_EXTRA = ["pdf"]
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_EXTRA

ALLOWED_GENRES = [
    "Acid Punk",
    "Acid Rock",
    "Afrobeat",
    "Afropop",
    "Alternative",
    "Alternative Metal",
    "Alternative Rock",
    "Ambient",
    "Art Rock",
    "Art Punk",
    "Big Band",
    "Black Metal",
    "Bluegrass",
    "Blues",
    "Bollywood",
    "Bossa Nova",
    "Britpop",
    "Cajun",
    "Celtic",
    "Celtic Rock",
    "Chillwave",
    "Chinese",
    "Classic Country",
    "Classic Pop",
    "Classic Prog",
    "Classic Rock",
    "Classical",
    "Comedy",
    "Country",
    "Cumbia",
    "Dabke",
    "Dance/Electronic",
    "Death Metal",
    "Deep House",
    "Dirty Blues",
    "Disco",
    "Dixieland Jazz",
    "Doo-wop",
    "Doom Metal",
    "Downtempo",
    "Dream Pop",
    "Drumline",
    "Easy Listening",
    "Electronic",
    "Electronic (Instrumental)",
    "Electronica",
    "Electropop",
    "Emo / Pop-Rock",
    "Eurodance",
    "Experimental",
    "Experimental Ambient Rock",
    "Folk",
    "Folk Pop",
    "Folk Punk",
    "Folk Rock",
    "Folk rock, Jazz",
    "French House",
    "Funk",
    "Funk (Instrumental)",
    "Funk Metal",
    "Funk Rock",
    "Funk/Soul",
    "Funktronica",
    "Glam Rock",
    "Gospel",
    "Goth Rock",
    "Gothic Rock",
    "Grindcore",
    "Grunge",
    "Heavy Metal",
    "Hip-Hop",
    "Hip-Hop français",
    "Hip-Hop/Electronic",
    "Hip-Hop/Reggae",
    "Honky Tonk",
    "House",
    "Indie",
    "Indie Folk",
    "Indie Pop",
    "Indie Rock",
    "Industrial",
    "Industrial Metal",
    "Japanese Rock",
    "Jazz",
    "Jazz Rock",
    "Jazz/Funk",
    "K-Pop",
    "Korean Rock",
    "Latin",
    "Latin Pop",
    "Literature",
    "Metal",
    "Metalcore",
    "Motown",
    "Neo-Soul",
    "New Age",
    "New Disco",
    "New Wave",
    "New Wave français",
    "Norteño",
    "Nu Jazz",
    "Nu Jazz (Instrumental)",
    "Nu Metal",
    "Nu Metal français",
    "Political",
    "Pop",
    "Pop Punk",
    "Pop Rock",
    "Pop française",
    "Pop italiano",
    "Pop-Punk",
    "Post-Black Metal",
    "Post-Grunge",
    "Post-Hardcore",
    "Post-Industrial",
    "Post-Metal",
    "Post-Punk",
    "Post-Rock",
    "Power Pop",
    "Prog Rock",
    "Progressive Metal",
    "Progressive Pop",
    "Psychedelic Folk",
    "Psychedelic Pop",
    "Psychedelic Rock",
    "Punk",
    "Punk Rock",
    "Punk français",
    "R&B",
    "R&B/Funk",
    "R&B (Instrumental)",
    "R&B/Soul",
    "Reggae",
    "Reggae Rock",
    "RnB français",
    "Rock",
    "Rock en español",
    "Rock brasileiro",
    "Rock français",
    "Rock italiano",
    "Rockabilly",
    "Russian Folk",
    "Russian Pop",
    "Shoegaze",
    "Ska Punk",
    "Soft Rock",
    "Sophisti-pop",
    "Soundtrack",
    "Southern Punk Rock",
    "Southern Rock",
    "Stoner Rock",
    "Surf Punk",
    "Surf Rock",
    "Swing",
    "Synth-pop",
    "Techno",
    "Thrash Metal",
    "Traditional Pop",
    "Trip hop",
    "Ukrainian Pop",
    "Urbano",
    "Volksmusik",
    "World",
    "Zydeco",
]


@dataclass
class Mediafile:
    """
    Mediafile dataclass

    """

    path: str
    size: int
    format: str
    title: str
    artist: str
    album: str
    genre: str
    year: int
    duration: int


@dataclass
class Data(YAMLWizard):
    """
    Data dataclass

    """

    mediafiles: list[Mediafile]


def load_yaml_file(yaml_fname: str) -> Data:
    data = None
    with open(yaml_fname, "r") as stream:
        try:
            data = Data.from_yaml(stream)  # type: ignore
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)
    return data  # type: ignore


files = load_yaml_file(MEDIASCAN_FILES_PATH)


@pytest.fixture(scope="session")
def files_yaml_file() -> Data:
    return load_yaml_file(MEDIASCAN_FILES_PATH)


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


# begin filesystem tests


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


@pytest.mark.parametrize(
    "media_path,limit",
    [
        (LIB1_MEDIA_PATH, LIB1_TOTAL_FILESIZE_LIMIT_GB),
        (LIB2_MEDIA_PATH, LIB2_TOTAL_FILESIZE_LIMIT_GB),
    ],
)
def test_lib_total_filesize_limit(media_path: str, limit: int):
    """Ensures that the total filesize of my LIB1 folder does not exceed
    LIB1_TOTAL_FILESIZE_LIMIT_GB
    """
    size = 0
    for path, _, files in os.walk(media_path):
        for f in files:
            fp = os.path.join(path, f)
            size += os.stat(fp).st_size
    print(size)
    size_gb = size / GIGABYTE
    print("size_gb=", size_gb)
    assert size_gb < limit


# end filesystem tests

# begin mediascan yaml tests


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_year_gt_zero(file: Mediafile):
    assert file.year > 0, f"{file.path}"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_years_lt_present(file: Mediafile):
    assert file.year <= PRESENT_YEAR, f"{file.path}"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_size_gt_min(file: Mediafile):
    assert file.size >= MINIMUM_FILESIZE, f"{file.path}"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_allowed_genres(file: Mediafile):
    assert file.genre in ALLOWED_GENRES, f"{file.path}"


# end mediascan yaml tests
