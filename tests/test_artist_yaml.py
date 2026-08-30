import os
from pathlib import Path

from mediatest.path_utils import get_file_ext, get_path_depth

from tests.test_config import *


def get_artist_directory_paths(media_lib_path: Path) -> List[Path]:
    ret = set()
    base_depth = get_path_depth(media_lib_path)
    for root, dirs, _ in os.walk(media_lib_path, topdown=False):
        for name in dirs:
            fullpath = os.path.join(root, name)
            current_depth = get_path_depth(fullpath)
            relative_depth = current_depth - base_depth
            # 1 = artist dir
            if relative_depth == 1:
                ret.add(fullpath)
    return list(ret)


def pytest_generate_tests(metafunc):
    artist_dir_paths = []
    for lib_idx in range(LIB_COUNT):
        media_lib_path = Path(LIBS_MEDIA_PATH[lib_idx])
        artist_dir_paths.extend(get_artist_directory_paths(media_lib_path))
    metafunc.parametrize("artist_path", artist_dir_paths)


def test_artist_yaml_exists(artist_path: Path):
    """
    That that verifies that artist.yaml file exists for the given artist path
    """
    artist_yaml_path = Path(artist_path) / "artist.yaml"
    assert artist_yaml_path.exists()
