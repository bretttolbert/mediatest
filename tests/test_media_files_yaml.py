import pytest
from typing import Dict, List, Optional, Set

from mediascan import load_files_yaml, Genre, MediaFiles, MediaFile

from tests.test_config import *

files = load_files_yaml(MEDIASCAN_FILES_PATH)


NO_ERRORS = "(no errors)"


def run_tests() -> List[str]:
    errors: List[str] = []
    errors += run_test_yaml("artist")
    errors += run_test_yaml("albumartist")
    errors += run_test_yaml("album", "albumartist")
    return errors


def pytest_generate_tests(metafunc):
    """Indirect parametrization for pytest to run
    test_per_error for each error found.
    parametrizes with a list of errors or [NO_ERRORS]
    i.e. the length of the list is at least 1
    (the sentinel value element NO_ERRORS allows
    at least one test to run and pass,
    otherwise the test would just be greyed out)
    """
    if "error" in metafunc.fixturenames:
        errors = run_tests()
        if len(errors) == 0:
            errors.append(NO_ERRORS)
        metafunc.parametrize("error", errors)


def test_per_error(error: str):
    """Test that fails for each error found.
    If there are no errors, it will run once and pass.
    Works with pytest using indirect parametrization.
    (See pytest_generate_tests above)
    """
    assert error == NO_ERRORS


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


def run_test_yaml(tag_type: str, tag_type_2: Optional[str] = None) -> List[str]:
    """
    tag_type: the tag to test
    tag_type_2: optional secondary qualifier, makes it skip validation if tag_type_2
    doesn't match. E.g. tag_type="album" and tag_type_2="artist" => only compare
    two albums if the artist is the same for both of them.
    """
    errors: List[str] = []
    grouped: Dict[str, List[MediaFile]] = {}
    for file in files.files:
        key = str(getattr(file, tag_type)).upper()
        if key in grouped:
            grouped[key].append(file)
        else:
            grouped[key] = [file]
    for _, v_l in grouped.items():
        f0 = v_l[0]
        for f in v_l[1:]:
            v1 = getattr(f, tag_type)
            v2 = getattr(f0, tag_type)
            if v1 != v2:
                if tag_type_2 is not None:
                    v2_1 = getattr(f0, tag_type_2)
                    v2_2 = getattr(f, tag_type_2)
                    if v2_1 != v2_2:
                        # e.g. albums with different capitalizaiton but different albumartists
                        # so it doesn't really matter so much
                        continue
                errors.append(
                    f"{tag_type.capitalize()} {f.artist} - {f.album} - {f.title} "
                    + f"tagged with inconsistent case-sensitivity ({v1} != {v2}) "
                    + f"\nf1={f0}\nf2={f}"
                )
    return errors
