# mediatest
Simple way to use PyTest to help you keep your media collections (e.g. mp3 music libraries) organized

The idea is to write tests to enforce rules for your media collection.

## Basic Usage

```bash
pytest mediatest.py
```

## Depedencies
- [mediascan](https://github.com/bretttolbert/mediascan)

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

Of course you can adjust the rules as desired my modifying the Python.
