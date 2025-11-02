# !/usr/bin/python3
from __future__ import annotations
import yaml
import pytest
import sys
from typing import Dict, List, Optional, Set

from mediascan import load_files_yaml, Genre, MediaFiles, MediaFile

from tests.test_config import *

files = load_files_yaml(MEDIASCAN_FILES_PATH)


@pytest.fixture(scope="session")
def files_yaml_file() -> MediaFiles:
    return files


@pytest.mark.parametrize("file", files.files)
def test_yaml_year_gt_zero(file: MediaFile):
    assert file.year > 0, f"{file.path}"


@pytest.mark.parametrize("file", files.files)
def test_yaml_years_lt_present(file: MediaFile):
    assert file.year <= PRESENT_YEAR, f"{file.path}"


@pytest.mark.parametrize("file", files.files)
def test_yaml_size_gt_min(file: MediaFile):
    assert file.size >= MINIMUM_FILESIZE, f"{file.path}"


def get_all_genre_strings() -> List[str]:
    return [g.value for g in Genre]


def genre_string_to_enum(s: str) -> Optional[Genre]:
    for genre in Genre:
        if genre.value == s:
            return genre
    return None


@pytest.mark.parametrize("file", files.files)
def test_yaml_allowed_genres(file: MediaFile):
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


@pytest.mark.parametrize("file", files.files)
def test_yaml_libs_genres_mode_whitelist(file: MediaFile):
    if LIB_GENRES_MODE_BLACKLIST:
        return
    for idx in range(LIB_COUNT):
        if file.path.find(LIBS_MEDIA_PATH[idx]) != -1:
            g = genre_string_to_enum(file.genre)
            assert (
                g is not None and g in LIBS_GENRES[idx]
            ), f"{file.path} (genre: {file.genre}) is not allowed by by LIB{idx+1} LIBS_GENRES"


@pytest.mark.parametrize("file", files.files)
def test_yaml_libs_genres_mode_blacklist(file: MediaFile):
    if not LIB_GENRES_MODE_BLACKLIST:
        return
    for idx in range(LIB_COUNT):
        if file.path.find(LIBS_MEDIA_PATH[idx]) != -1:
            g = genre_string_to_enum(file.genre)
            assert (
                g is not None and g not in LIBS_GENRES[idx]
            ), f"{file.path} (genre: {file.genre}) is prohibited by LIB{idx+1} LIBS_GENRES"


@pytest.mark.parametrize("file", files.files)
def test_yaml_artist_is_not_empty(file: MediaFile):
    assert len(file.artist) > 0, f"{file.path}"


@pytest.mark.parametrize("file", files.files)
def test_yaml_albumartist_is_not_empty(file: MediaFile):
    assert len(file.albumartist) > 0, f"{file.path}"


def test_yaml_albumartist_same_for_every_track_in_every_album():
    """
    Different tracks may have different artists e.g. "Dr. Dre feat. Snoop Dog"
    but all tracks in a an albums should have the same albumartist e.g. "Dr. Dre"
    """
    albums: Dict[str, str] = {}
    for file in files.files:
        albumkey = f"{file.albumartist} - {file.album} [{file.year}]"
        if albumkey in albums:
            assert albums[albumkey] == file.albumartist
        else:
            albums[albumkey] = file.albumartist
