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
- Genre ID3 tag must be in allowed genres (see Genres below)

Of course you can adjust the rules as desired my modifying the Python.

## Genres

My genres below, with counts (output of [mediastats](https://github.com/bretttolbert/mediascan/blob/main/mediastats.py) `print_genre_counts`). I am in the process of consolidating the least populated genres.

```python
{'Classic Rock': 2170, 'Indie Rock': 1381, 'Alternative Rock': 1294, 'Hip-Hop': 662, 'Classic Country': 603, 'Classic Prog': 584, 'Funk Rock': 429, 'Post-Punk': 313, 'Post-Hardcore': 304, 'Electropop': 303, 'R&B/Soul': 271, 'Electronic (Instrumental)': 268, 'Electronica': 246, 'Indie Folk': 234, 'Electronic': 228, 'Punk': 221, 'Classical': 219, 'New Wave': 218, 'Country': 194, 'Stoner Rock': 182, 'Funk': 175, 'Classic Pop': 169, 'Funk (Instrumental)': 168, 'Jazz': 164, 'Alternative Metal': 153, 'Britpop': 152, 'Punk Rock': 148, 'Folk': 144, 'Pop': 125, 'Industrial Metal': 125, 'New Wave français': 123, 'Folk Punk': 121, 'Post-Grunge': 120, 'Reggae': 117, 'Emo / Pop-Rock': 114, 'Southern Rock': 111, 'Heavy Metal': 108, 'R&B': 101, 'Nu Metal': 101, 'Rock': 98, 'Grunge': 95, 'Indie Pop': 94, 'Pop Rock': 91, 'Dream Pop': 86, 'Bluegrass': 69, 'Pop-Punk': 64, 'Progressive Pop': 62, 'Hip-Hop/Electronic': 62, 'Blues': 59, 'Punk français': 55, 'Hip-Hop français': 54, 'Psychedelic Rock': 53, 'Soft Rock': 53, 'Thrash Metal': 50, 'Latin': 48, 'Post-Rock': 43, 'Disco': 42, 'Rock en español': 42, 'Post-Industrial': 42, 'Honky Tonk': 40, 'Surf Rock': 38, 'Easy Listening': 37, 'Synth-pop': 34, 'Rock français': 32, 'Nu Jazz': 32, 'Funk Metal': 31, 'Industrial': 30, 'Psychedelic Pop': 29, 'Jazz/Funk': 28, 'Neo-Soul': 28, 'Pop française': 27, 'Folk Rock': 27, 'World': 27, 'Ska Punk': 24, 'Progressive Metal': 24, 'Soundtrack': 23, 'Deep House': 21, 'Southern Punk Rock': 19, 'Nu Jazz (Instrumental)': 17, 'Hip Hop, Jazz, Funk / Soul': 17, 'Folk rock, Jazz': 16, 'Dance & DJ': 16, 'Funk/Soul': 15, 'Art Rock': 15, 'Swing': 14, 'Gospel': 14, 'Bossa Nova': 14, 'Metal': 13, 'Indie': 13, 'Cumbia': 12, 'Genesis': 12, 'Shoegaze': 12, 'Celtic Rock': 12, 'Eurodance': 12, 'Gothic Rock': 11, 'Trip hop': 11, 'Cajun': 10, 'Acid Rock': 10, 'Pop Punk': 10, 'Progressive Rock': 9, 'Post-Black Metal': 9, 'Urbano': 9, 'Prog Rock': 9, 'Experimental': 9, 'Comedy': 8, 'Reggae Rock': 8, 'Doo-wop': 7, 'Latin Pop': 7, 'Hip-hop français': 7, 'Dance/Electronic': 6, 'Dance': 6, 'Glam Rock': 5, 'Bollywood': 5, 'Alternative Pop': 5, 'Psychedelic Folk': 4, 'Celtic': 4, 'Norteño': 4, 'Death Metal': 4, 'Downtempo': 4, 'Trip-Hop': 4, 'Post-Metal': 4, 'Soul/R&B': 3, 'Dub': 3, 'Drumline': 3, 'Folk Pop': 3, 'Black Metal': 3, 'Americana': 2, 'Traditional Pop': 2, 'Rockabilly': 2, 'Political': 2, 'Surf Punk': 2, 'Sophisti-pop': 2, 'New Age': 2, 'Chinese': 2, 'Art Pop': 2, 'Acid Punk': 2, 'Nu Metal français': 2, 'Grindcore': 2, 'Metalcore': 2, 'Hip-Hop/Reggae': 2, 'House': 2, 'Electro': 2, 'Japanese Rock': 2, 'Chillwave': 2, 'Russian Folk': 1, 'Dixieland Jazz': 1, 'Dirty Blues': 1, 'Big Band': 1, 'Motown': 1, 'Rock brasileiro': 1, 'Disco/Soul': 1, 'Korean Rock': 1, 'Post-Disco': 1, 'Pop italiano': 1, 'Rock italiano': 1, 'Goth Rock': 1, 'New-age': 1, 'Literature': 1, 'Experimental Ambient Rock': 1, 'Alternative': 1, 'Jazz Rock': 1, 'Acid House': 1, 'Rap Rock': 1, 'Doom Metal': 1, 'French House': 1, 'Techno': 1, 'Ukrainian Pop': 1, 'K-Pop': 1, 'Volksmusik': 1, 'Dance/Hip-Hop': 1, 'Acid Jazz': 1, 'Afropop': 1, 'Indietronica': 1, 'Power Pop': 1, 'New Disco': 1, 'Post-disco': 1, 'Funktronica': 1, 'Dabke': 1, 'Afrobeat': 1, 'Trance': 1, 'R&B (Instrumental)': 1, 'RnB français': 1}
```
