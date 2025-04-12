# !/usr/bin/python3
from __future__ import annotations
import yaml
import pytest
import os
import re
import sys
from typing import Dict, List, Set

from dataclasses import dataclass
from datetime import datetime

from dataclass_wizard import YAMLWizard  # type: ignore

from mediatest.genres import Genre

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
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = [
    "jpg",
    "webp",
    "png",
]  # intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_LYRICS = ["lrc", "txt"]
EXTS_EXTRA = ["pdf"]  # some albums include pdf booklets
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_EXTRA
LIB_GENRES_MODE_BLACKLIST = False  # Set to True if you want LIBS_GENRES lists to be blacklists instead of whitelists (default)

# Multiple music libraries are supported.
# For my personal use, I bifurcate my music into two libraries.
# One reason for this is because I backup my libraries to Blu-Ray M-discs for
# long-term cold-storage and triple-layer Blu-Rays have a max capacity of 100 GB.
# The other reason I do this is I have some Android tablets with a maximum storage
# capacity of 128 GB and I sync my primary library (LIB1) to it, for a party shuffle mix.
# Consequently LIB2 is primarily for non-party music.
# I bifurcate my music library based on genre tags.
# Certain genres exclusively belong in LIB1, and other genres exclusively belong in LIB2.
# I use pytest to enforce this constraint.
# The essential dichotomy is popular/upbeat genres vs. more obscure/melancholic genres
# LIB1 (/data/Music) is my primary music library - party mix: rock/pop/hip-hop/r&b/disco
# LIB2 (/data/MusicOther) is for everything that doesn't fit in LIB1: alternative/jazz/metal
# Variables beginning with LIBS_ are arrays of size LIB_COUNT
LIB_COUNT = 2
LIBS_MEDIA_PATH = ["/data/Music/", "/data/MusicOther/"]
LIBS_EXPECTED_MEDIA_COUNT = [10450, 8723]
LIBS_EXPECTED_LRC_COUNT = [6229, 2969]
LIBS_TOTAL_FILESIZE_LIMIT_GB = [100, 100]
LIBS_EXPECTED_FILESIZE_GB = [79, 68]
LIBS_GENRES: List[List[Genre]] = [
    [
        Genre.Afrobeat,
        Genre.Afropop,
        Genre.ArtPunk,
        Genre.ClassicPop,
        Genre.ClassicRock,
        Genre.Cumbia,
        Genre.Dabke,
        Genre.DanceElectronic,
        Genre.DeepHouse,
        Genre.Disco,
        Genre.Downtempo,
        Genre.DreamPop,
        Genre.Electropop,
        Genre.Eurodance,
        Genre.FolkPop,
        Genre.FrenchHouse,
        Genre.Funk,
        Genre.FunkMetal,
        Genre.FunkRock,
        Genre.FunkSoul,
        Genre.Funktronica,
        Genre.GlamRock,
        Genre.Grunge,
        Genre.HeavyMetal,
        Genre.HipHop,
        Genre.HipHopFrançais,
        Genre.HipHopReggae,
        Genre.House,
        Genre.IndiePop,
        Genre.IndieRock,
        Genre.JapaneseRock,
        Genre.KPop,
        Genre.KoreanRock,
        Genre.Latin,
        Genre.LatinPop,
        Genre.Motown,
        Genre.NeoSoul,
        Genre.NewAge,
        Genre.NewDisco,
        Genre.NewWave,
        Genre.Norteño,
        Genre.NuMetal,
        Genre.Pop,
        Genre.PopFrançaise,
        Genre.PopItaliano,
        Genre.PopRock,
        Genre.PostBlackMetal,
        Genre.PostHardcore,
        Genre.PostMetal,
        Genre.PowerPop,
        Genre.ProgressiveMetal,
        Genre.ProgRock,
        Genre.PsychedelicFolk,
        Genre.PsychedelicPop,
        Genre.PsychedelicRock,
        Genre.Punk,
        Genre.PunkFrançais,
        Genre.PunkRock,
        Genre.RnB,
        Genre.RnBFunk,
        Genre.RnBSoul,
        Genre.Reggaeton,
        Genre.ReggaeRock,
        Genre.RnBFrançais,
        Genre.Rockabilly,
        Genre.RockBrasileiro,
        Genre.RockEnEspañol,
        Genre.RockFrançais,
        Genre.RockItaliano,
        Genre.RussianPop,
        Genre.SkaPunk,
        Genre.SludgeMetal,
        Genre.SophistiPop,
        Genre.SouthernPunkRock,
        Genre.SurfRock,
        Genre.SurfPunk,
        Genre.SynthPop,
        Genre.Techno,
        Genre.ThrashMetal,
        Genre.TraditionalPop,
        Genre.TripHop,
        Genre.UkrainianPop,
        Genre.Urbano,
        Genre.World,
    ],
    [
        Genre.AcidPunk,
        Genre.AcidRock,
        Genre.Alternative,
        Genre.AlternativeRock,
        Genre.AlternativeMetal,
        Genre.Ambient,
        Genre.ArtRock,
        Genre.EasyListening,
        Genre.Electronic,
        Genre.Electronica,
        Genre.ElectronicInstrumental,
        Genre.Experimental,
        Genre.ExperimentalAmbientRock,
        Genre.Blues,
        Genre.BigBand,
        Genre.BlackMetal,
        Genre.Bluegrass,
        Genre.Bollywood,
        Genre.BossaNova,
        Genre.Britpop,
        Genre.Chillwave,
        Genre.Chinese,
        Genre.Cajun,
        Genre.Celtic,
        Genre.CelticRock,
        Genre.Classical,
        Genre.ClassicProg,
        Genre.Comedy,
        Genre.Country,
        Genre.ClassicCountry,
        Genre.DeathMetal,
        Genre.DirtyBlues,
        Genre.DixielandJazz,
        Genre.DoomMetal,
        Genre.DooWop,
        Genre.Drumline,
        Genre.EmoPopRock,
        Genre.Folk,
        Genre.FolkPunk,
        Genre.FolkRockJazz,
        Genre.FunkInstrumental,
        Genre.Gospel,
        Genre.Grindcore,
        Genre.GothRock,
        Genre.HipHopElectronic,
        Genre.HipHopInstrumental,
        Genre.HonkyTonk,
        Genre.IndieFolk,
        Genre.Industrial,
        Genre.IndustrialMetal,
        Genre.Jazz,
        Genre.JazzFunk,
        Genre.JazzRock,
        Genre.Literature,
        Genre.Metalcore,
        Genre.NewWaveFrançais,
        Genre.NoiseRock,
        Genre.NuJazz,
        Genre.NuJazzInstrumental,
        Genre.NuMetalFrançais,
        Genre.Political,
        Genre.PostGrunge,
        Genre.PostIndustrial,
        Genre.PostRock,
        Genre.PostPunk,
        Genre.ProgressivePop,
        Genre.ProtoPunk,
        Genre.Reggae,
        Genre.RussianFolk,
        Genre.Shoegaze,
        Genre.SpeechSample,
        Genre.SoftRock,
        Genre.Soundtrack,
        Genre.SouthernRock,
        Genre.StonerRock,
        Genre.Swing,
        Genre.Volksmusik,
        Genre.Zydeco,
    ],
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
    albumartist: str
    album: str
    genre: str
    year: int
    duration: int


@dataclass
class Data(YAMLWizard):  # type: ignore
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


@pytest.mark.parametrize("media_path", LIBS_MEDIA_PATH)
def test_allowed_exts(media_path: str):
    do_test_allowed_exts(media_path)


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


def get_all_genre_strings() -> List[str]:
    return [g.value for g in Genre]


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_allowed_genres(file: Mediafile):
    assert file.genre in get_all_genre_strings(), f"{file.path}"


@pytest.mark.parametrize("lib_idx", list(range(LIB_COUNT)))
def test_lib_genres_no_dupes(lib_idx: int):
    s: Set[str] = set()
    for genre in LIBS_GENRES[lib_idx]:
        if genre in s:
            pytest.exit(f"Duplicate genre detected in LIB{lib_idx}_GENRES: {genre}")
        s.add(genre)


def test_lib_genres_no_intersections():
    """TODO: Make this work for more than two libs"""
    for idx in range(LIB_COUNT):
        if idx == LIB_COUNT - 1:
            return
        intersection = set(LIBS_GENRES[idx]) & set(LIBS_GENRES[idx + 1])
        if len(intersection):
            pytest.exit(
                f"Duplicate genres in both LIB{idx+1} and LIB{idx+2}: {str(intersection)}"
            )


def test_lib_genres_all_genres_used():
    for genre in get_all_genre_strings():
        found = False
        for i in range(LIB_COUNT):
            if genre in LIBS_GENRES[i]:
                found = True
                break
        if not found:
            pytest.exit("Genre not in any lib genres: " + genre)


def genre_string_to_enum(s: str):
    try:
        return Genre[s]
    except KeyError:
        return None


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_libs_genres_mode_whitelist(file: Mediafile):
    if LIB_GENRES_MODE_BLACKLIST:
        return
    for idx in range(LIB_COUNT):
        if file.path.find(LIBS_MEDIA_PATH[idx]) != -1:
            g = genre_string_to_enum(file.genre)
            assert (
                g is not None and g in LIBS_GENRES[idx]
            ), f"{file.path} (genre: {file.genre}) is not allowed by by LIB{idx+1}_GENRES"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_libs_genres_mode_blacklist(file: Mediafile):
    if not LIB_GENRES_MODE_BLACKLIST:
        return
    for idx in range(LIB_COUNT):
        if file.path.find(LIBS_MEDIA_PATH[idx]) != -1:
            g = genre_string_to_enum(file.genre)
            assert (
                g is not None and g not in LIBS_GENRES[idx]
            ), f"{file.path} (genre: {file.genre}) is prohibited by LIB{idx+1}_GENRES"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_artist_is_not_empty(file: Mediafile):
    assert len(file.artist) > 0, f"{file.path}"


@pytest.mark.parametrize("file", files.mediafiles)
def test_yaml_albumartist_is_not_empty(file: Mediafile):
    assert len(file.albumartist) > 0, f"{file.path}"


def test_yaml_albumartist_same_for_every_track_in_every_album():
    """
    Different tracks may have different artists e.g. "Dr. Dre feat. Snoop Dog"
    but all tracks in a an albums should have the same albumartist e.g. "Dr. Dre"
    """
    albums: Dict[str, str] = {}
    for file in files.mediafiles:
        albumkey = f"{file.albumartist} - {file.album} [{file.year}]"
        if albumkey in albums:
            assert albums[albumkey] == file.albumartist
        else:
            albums[albumkey] = file.albumartist


# end mediascan yaml tests
