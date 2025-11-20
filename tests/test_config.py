from __future__ import annotations

from mediatest.genres import Genre

from typing import List

from datetime import datetime

# For running tests on the yaml file output by mediascan
# E.g. for ID3-tag tests
# E.g. testing if year is a valid year or something weird like 0
MEDIASCAN_FILES_PATH = "../mediascan/out/files.yaml"

KILOBYTE = 10**3
MEGABYTE = 10**6
GIGABYTE = 10**9
PRESENT_YEAR: int = datetime.now().year
MINIMUM_FILESIZE = 10 * KILOBYTE
EXTS_MEDIA = ["mp3", "m4a"]
EXTS_ART = [
    "jpg",
    "webp",
    "png",
    "xcf",
]  # intentionally lowercase for consistency, ".JPG" not allowed, etc.
EXTS_LYRICS = ["lrc", "txt"]
EXTS_EXTRA = ["pdf"]  # some albums include pdf booklets
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_EXTRA

LIB_GENRES_MODE_BLACKLIST = False  # Set to True if you want LIBS_GENRES lists to be blacklists instead of whitelists (default)

# Multiple music libraries are supported.
# For my personal use, I split my music into two libraries.
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
LIBS_EXPECTED_MEDIA_COUNT = [11159, 9255]
LIBS_EXPECTED_LRC_COUNT = [7207, 4239]
LIBS_TOTAL_FILESIZE_LIMIT_GB = [100, 100]
LIBS_EXPECTED_FILESIZE_GB = [84, 73]
LIBS_GENRES: List[List[Genre]] = [
    [
        Genre.Afrobeat,
        Genre.Afropop,
        Genre.ArtPunk,
        Genre.ClassicPop,
        Genre.ClassicRock,
        Genre.CountryPop,
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
        Genre.GlamMetal,
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
        Genre.KoreanRock,
        Genre.KPop,
        Genre.Latin,
        Genre.LatinFunk,
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
        Genre.PopPunk,
        Genre.PopRock,
        Genre.PostBlackMetal,
        Genre.PostHardcore,
        Genre.PostMetal,
        Genre.PowerPop,
        Genre.ProgressiveMetal,
        Genre.PsychedelicFolk,
        Genre.PsychedelicPop,
        Genre.PsychedelicRock,
        Genre.Punk,
        Genre.PunkFrançais,
        Genre.PunkRock,
        Genre.ReggaeRock,
        Genre.Reggaeton,
        Genre.RnB,
        Genre.RnBFrançais,
        Genre.RnBFunk,
        Genre.RnBInstrumental,
        Genre.RnBSoul,
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
        Genre.SurfPunk,
        Genre.SurfRock,
        Genre.SynthPop,
        Genre.Techno,
        Genre.ThrashMetal,
        Genre.TraditionalPop,
        Genre.Trance,
        Genre.TripHop,
        Genre.UkrainianPop,
        Genre.Urbano,
        Genre.World,
    ],
    [
        Genre.AcidPunk,
        Genre.AcidRock,
        Genre.Alternative,
        Genre.AlternativeMetal,
        Genre.AlternativeRock,
        Genre.Ambient,
        Genre.ArtRock,
        Genre.BigBand,
        Genre.BlackMetal,
        Genre.Bluegrass,
        Genre.Blues,
        Genre.Bollywood,
        Genre.BossaNova,
        Genre.Britpop,
        Genre.Cajun,
        Genre.Celtic,
        Genre.CelticRock,
        Genre.Chillwave,
        Genre.Chinese,
        Genre.Classical,
        Genre.ClassicCountry,
        Genre.ClassicProg,
        Genre.Comedy,
        Genre.Country,
        Genre.DeathMetal,
        Genre.DirtyBlues,
        Genre.DixielandJazz,
        Genre.DoomMetal,
        Genre.DooWop,
        Genre.Drumline,
        Genre.EasyListening,
        Genre.Electronic,
        Genre.Electronica,
        Genre.ElectronicInstrumental,
        Genre.EmoPopRock,
        Genre.Experimental,
        Genre.ExperimentalAmbientRock,
        Genre.Folk,
        Genre.FolkPunk,
        Genre.FolkRock,
        Genre.FolkRockJazz,
        Genre.FunkInstrumental,
        Genre.Gospel,
        Genre.GothRock,
        Genre.Grindcore,
        Genre.HipHopElectronic,
        Genre.HipHopInstrumental,
        Genre.HonkyTonk,
        Genre.HorrorPunk,
        Genre.IndieFolk,
        Genre.Industrial,
        Genre.IndustrialMetal,
        Genre.Jazz,
        Genre.JazzFunk,
        Genre.JazzPop,
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
        Genre.PostPunk,
        Genre.PostRock,
        Genre.ProgRock,
        Genre.ProgressivePop,
        Genre.ProtoPunk,
        Genre.Reggae,
        Genre.RussianFolk,
        Genre.Shoegaze,
        Genre.SmoothJazz,
        Genre.SoftRock,
        Genre.Soundtrack,
        Genre.SouthernRock,
        Genre.SpeechSample,
        Genre.StonerRock,
        Genre.Swing,
        Genre.Volksmusik,
        Genre.Zydeco,
    ],
]
