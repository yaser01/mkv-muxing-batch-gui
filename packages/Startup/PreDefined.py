# ALL CONSTANTS HERE
import json

from packages.Startup.GlobalFiles import LanguagesFilePath


def generate_track_ids(max):
    res = []
    for i in range(max):
        id = i + 1
        if id < 10:
            id = "0" + str(id)
        else:
            id = str(id)
        res.append("Pista " + id)
    return res


ISO_639_2_LANGUAGES = {}


def generate_languages_tracks():
    global ISO_639_2_LANGUAGES
    with open(LanguagesFilePath, "r", encoding="UTF-8") as setting_file:
        ISO_639_2_LANGUAGES = json.load(setting_file)


tracks_list = generate_track_ids(10)
generate_languages_tracks()
ISO_639_2_SYMBOLS = {v: k for k, v in ISO_639_2_LANGUAGES.items()}
AllVideosExtensions = [
    "MKV",
    "AVI",
    "MP4",
    "M4V",
    "MOV",
    "MPEG",
    "TS",
    "OGG",
    "OGM",
    "H264",
    "H265",
    "WEBM",
    "WMV",
    "IVF",
    "M2TS",
    "VOB",
]
AllSubtitlesExtensions = ["ASS", "SRT", "SSA", "SUP", "PGS", "MKS", "VTT", "SUB"]
AllAudiosExtensions = [
    "AAC",
    "AC3",
    "FLAC",
    "EAC3",
    "MKA",
    "M4A",
    "MP3",
    "DTS",
    "DTSMA",
    "THD",
    "WAV",
    "OGG",
    "OPUS",
]
AllVideosLanguages = list(ISO_639_2_LANGUAGES.keys())
AllSubtitlesLanguages = list(ISO_639_2_LANGUAGES.keys())
AllAudiosLanguages = list(ISO_639_2_LANGUAGES.keys())
AllChapterExtensions = ["XML"]
AllSubtitlesTracks = ["---Pistas---"]
AllSubtitlesTracks.extend(tracks_list)
AllSubtitlesTracks.append("---Idiomas---")
AllSubtitlesTracks.extend(list(ISO_639_2_LANGUAGES.keys()))
AllAudiosTracks = AllSubtitlesTracks
AllVideoDefaultDurationFPSLanguages = [
    "Predeterminado",
    "24p",
    "25p",
    "30p",
    "48p",
    "50i",
    "50p",
    "60i",
    "60p",
    "24000/1001p",
    "30000/1001p",
    "48000/1001p",
    "60000/1001i",
    "60000/1001p",
]
GitHubRepoUrlTag = (
    '<a href="https://github.com/Khaoklong51/mkv-muxing-batch-gui">Nuestra página principal</a> '
)
GPLV2UrlTag = '<a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">GPLv2</a>'
GitHubIssuesUrlTag = (
    '<a href="https://github.com/Khaoklong51/mkv-muxing-batch-gui/issues">página de incidencias</a>'
)