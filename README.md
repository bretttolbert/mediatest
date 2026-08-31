# mediatest
Simple way to use PyTest to help you keep your media collections (e.g. mp3 music libraries) organized

The idea is to write tests to enforce rules for your media collection.

## Basic Usage

Update settings in [tests/test_config.py](./tests/test_config.py) as needed, then:

```bash
pip install .
pytest .
```

## Example Test Failure

```bash
tests/test_media_lib_counts.py:97: AssertionError
======================================================= short test summary info ========================================================
FAILED tests/test_media_artist_dirs.py::test_artist_yaml_exists[artist_path2151] - AssertionError: assert False
 +  where False = exists()
 +    where exists = PosixPath('/data/Music/Various Artists/artist.yaml').exists
FAILED tests/test_media_files_yaml.py::test_mediafile_albumartist_matches_artist_directory_name - AssertionError: File (path=/data/Music/Crosby, Stills and Nash/Crosby, Stills and Nash - Crosby, Stills and Nash [1969]/01.01 - Suite_ Judy Blue Eyes.mp3) albumartist 'Crosby, Stills & Nash' (escaped=Crosby, Stills & Nash)  does not match artist directory name 'Crosby, Stills and Nash'
assert 'David Crosby & Stephen Stills' == 'Crosby, Stills & Nash'
  
  - Crosby, Stills & Nash
  + David Crosby & Stephen Stills

```


## Advanced Usage

Only run filesystem tests (and not the slower files.yaml tests):

```bash
pytest -k filesystem
```

## Depedencies
- [mediascan](https://github.com/bretttolbert/mediascan) (Required for ID3 tag tests) - A simple and fast Go (golang) command-line utility to recursively scan a directory for media files, extract metadata (including ID3v2 tags from both MP3 and M4A files), and save the output in a simple YAML format (e.g. [files.yaml](https://github.com/bretttolbert/mediascan/blob/main/out/files.yaml), and a Python library with data classes for working with the YAML files output by `mediascan.go`.

## Rules Enforced

- Top level folders are _artist_ folders
- Inside each _artist_ folder is one or more _album_ folders
- Every _album_ folder is required to have a `cover.jpg`
- Every _album_ folder name is required to have the year in square brackets
- No empty directories
- _album_ folders must contain one or more media files
- Media files types are `.mp3` and `.m4a`
- Media file count matches expected media file count
- Folder names don't contain prohibited characters which may cause problems with other filesystems (e.g. Windows)
- etc.
- Year ID3 tag must be greater than 0 (requires mediascan)
- Year ID3 tag must be less than current year (requires mediascan)
- Genre ID3 tag must be in allowed genres (see Genres below)

Of course you can adjust the rules as desired my modifying the Python.

## Genres

This library utilizes the comprehensive [`Genre` enum provided by `mediascan`](https://github.com/bretttolbert/mediascan/blob/main/python/mediascan/src/genres.py) with string values corresponding to the expected ID3 tag values. This helps avoid inconsistencies e.g. _"Post-punk"_ vs. _"Post-Punk"_ vs. _"Post punk"_ vs. _"Post Punk"_.
