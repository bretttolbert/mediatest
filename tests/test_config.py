from typing import List
from datetime import datetime

from mediascan import Genre # type: ignore

from mediatest.path_utils import KILOBYTE


# For running tests on the yaml file output by mediascan
# E.g. for ID3-tag tests
# E.g. testing if year is a valid year or something weird like 0
MEDIASCAN_FILES_PATH = "../mediascan/out/files.yaml"


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
EXTS_METADATA = ["yaml"]  # artist metadata files
EXTS_EXTRA = ["pdf"]  # some albums include pdf booklets
ALLOWED_EXTS = EXTS_MEDIA + EXTS_ART + EXTS_LYRICS + EXTS_METADATA + EXTS_EXTRA

LIB_GENRES_MODE_BLACKLIST = (
    False  # Set to True if you want LIBS_GENRES lists to be blacklists instead of whitelists (default)
)

# Multiple music libraries are supported.
# LIB1 (/data/Music) is my primary music library
# LIB2 (/data/MusicOther) is for any audio that is not music (lectures, speeches, podcasts)
# Variables beginning with LIBS_ are arrays of size LIB_COUNT
LIB_COUNT = 2
LIBS_MEDIA_PATH = ["/data/Music/", "/data/MusicOther/"]
LIBS_EXPECTED_MEDIA_COUNT = [21589, 0]
LIBS_EXPECTED_LRC_COUNT = [11547, 0]
LIBS_TOTAL_FILESIZE_LIMIT_GB = [200, 1]
LIBS_EXPECTED_FILESIZE_GB = [167, 0]

# Genre constraints may be enforced to limit a library to specified genres
# With current implementation, a given genre must belong to a single library
# This becomes complicated when an artist spans multiple genres
# I will probably only use this to keep things like lectures, speeches and podcasts out
# of the primary Music directory.
# Hence currently basically all of the genres are in LIB1.
LIBS_GENRES: List[List[Genre]] = [
    [
        Genre.AcidPunk,
        Genre.AcidRock,
        Genre.Afrobeat,
        Genre.Afropop,
        Genre.Alternative,
        Genre.AlternativeMetal,
        Genre.AlternativeRock,
        Genre.Ambient,
        Genre.ArtPop,
        Genre.ArtPunk,
        Genre.ArtRock,
        Genre.Bachata,
        Genre.BigBand,
        Genre.BlackMetal,
        Genre.Bluegrass,
        Genre.Blues,
        Genre.BluesRock,
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
        Genre.ClassicPop,
        Genre.ClassicProg,
        Genre.ClassicRock,
        Genre.Comedy,
        Genre.Country,
        Genre.CountryPop,
        Genre.Cumbia,
        Genre.Dabke,
        Genre.DanceElectronic,
        Genre.DeathMetal,
        Genre.DeepHouse,
        Genre.DirtyBlues,
        Genre.Disco,
        Genre.DixielandJazz,
        Genre.DoomMetal,
        Genre.DooWop,
        Genre.Downtempo,
        Genre.DreamPop,
        Genre.Drumline,
        Genre.EasyListening,
        Genre.Electronic,
        Genre.Electronica,
        Genre.ElectronicInstrumental,
        Genre.Electropop,
        Genre.EmoPopRock,
        Genre.Eurodance,
        Genre.Experimental,
        Genre.ExperimentalAmbientRock,
        Genre.Folk,
        Genre.FolkPop,
        Genre.FolkPunk,
        Genre.FolkRock,
        Genre.FolkRockJazz,
        Genre.FrenchHouse,
        Genre.Funk,
        Genre.FunkInstrumental,
        Genre.FunkMetal,
        Genre.FunkRock,
        Genre.FunkSoul,
        Genre.Funktronica,
        Genre.GlamMetal,
        Genre.GlamRock,
        Genre.Gospel,
        Genre.GothRock,
        Genre.Grindcore,
        Genre.Grunge,
        Genre.HeavyMetal,
        Genre.HipHop,
        Genre.HipHopElectronic,
        Genre.HipHopFrançais,
        Genre.HipHopInstrumental,
        Genre.HipHopReggae,
        Genre.HonkyTonk,
        Genre.HorrorPunk,
        Genre.House,
        Genre.IndieFolk,
        Genre.IndiePop,
        Genre.IndieRock,
        Genre.Industrial,
        Genre.IndustrialMetal,
        Genre.JamRock,
        Genre.JapaneseRock,
        Genre.Jazz,
        Genre.JazzFunk,
        Genre.JazzPop,
        Genre.JazzRock,
        Genre.KoreanRock,
        Genre.KPop,
        Genre.Latin,
        Genre.LatinFunk,
        Genre.LatinPop,
        Genre.Literature,
        Genre.Merengue,
        Genre.Metalcore,
        Genre.Motown,
        Genre.NeoSoul,
        Genre.NewAge,
        Genre.NewDisco,
        Genre.NewWave,
        Genre.NewWaveFrançais,
        Genre.NoiseRock,
        Genre.Norteño,
        Genre.NuJazz,
        Genre.NuJazzInstrumental,
        Genre.NuMetal,
        Genre.NuMetalFrançais,
        Genre.Political,
        Genre.Pop,
        Genre.PopFrançaise,
        Genre.PopItaliano,
        Genre.PopPunk,
        Genre.PopRock,
        Genre.PostBlackMetal,
        Genre.PostGrunge,
        Genre.PostHardcore,
        Genre.PostIndustrial,
        Genre.PostMetal,
        Genre.PostPunk,
        Genre.PostRock,
        Genre.PowerPop,
        Genre.ProgressiveMetal,
        Genre.ProgressivePop,
        Genre.ProgRock,
        Genre.ProtoPunk,
        Genre.PsychedelicFolk,
        Genre.PsychedelicPop,
        Genre.PsychedelicRock,
        Genre.Punk,
        Genre.PunkFrançais,
        Genre.PunkRock,
        Genre.Reggae,
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
        Genre.RussianFolk,
        Genre.RussianPop,
        Genre.Salsa,
        Genre.Shoegaze,
        Genre.SkaPunk,
        Genre.SludgeMetal,
        Genre.SmoothJazz,
        Genre.SoftRock,
        Genre.SophistiPop,
        Genre.Soundtrack,
        Genre.SouthernPunkRock,
        Genre.SouthernRock,
        Genre.SpeechSample,
        Genre.StonerRock,
        Genre.SufiRock,
        Genre.SurfPunk,
        Genre.SurfRock,
        Genre.Swing,
        Genre.SynthPop,
        Genre.Techno,
        Genre.ThrashMetal,
        Genre.TraditionalPop,
        Genre.Trance,
        Genre.TripHop,
        Genre.UkrainianPop,
        Genre.Urbano,
        Genre.Volksmusik,
        Genre.World,
        Genre.Zamrock,
        Genre.Zydeco,
    ],
    [],
]
