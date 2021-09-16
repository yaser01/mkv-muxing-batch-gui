# ALL CONSTANTS HERE
def generate_track_ids(max):
    res = []
    for i in range(max):
        id = i + 1
        if (id < 10):
            id = "0" + str(id)
        else:
            id = str(id)
        res.append("Track " + id)
    return res


tracks_list = generate_track_ids(10)
ISO_639_2_LANGUAGES = {
    "Amharic": "amh",
    "Arabic": "ara",
    "Azerbaijani": "aze",
    "Bengali": "ben",
    "Bhojpuri": "bho",
    "Bulgarian": "bul",
    "Burmese": "bur",
    "Cebuano": "ceb",
    "Central Khmer": "khm",
    "Chinese": "chi",
    "Czech": "cze",
    "Danish": "dan",
    "Dutch": "dut",
    "English": "eng",
    "Finnish": "fin",
    "French": "fre",
    "German": "ger",
    "Greek, Modern": "gre",
    "Gujarati": "guj",
    "Hausa": "hau",
    "Hebrew": "heb",
    "Hindi": "hin",
    "Hungarian": "hun",
    "Igbo": "ibo",
    "Indonesian": "ind",
    "Italian": "ita",
    "Japanese": "jpn",
    "Javanese": "jav",
    "Kannada": "kan",
    "Kazakh": "kaz",
    "Kinyarwanda": "kin",
    "Korean": "kor",
    "Kurdish": "kur",
    "Magahi": "mag",
    "Maithili": "mai",
    "Malay": "may",
    "Malayalam": "mal",
    "Marathi": "mar",
    "Nepali": "nep",
    "No linguistic content": "zxx",
    "Oriya": "ori",
    "Panjabi": "pan",
    "Persian": "per",
    "Polish": "plo",
    "Portuguese": "por",
    "Pushto": "pus",
    "Romanian": "rum",
    "Rundi": "run",
    "Russian": "rus",
    "Serbian": "srp",
    "Sindhi": "snd",
    "Sinhala": "sin",
    "Somali": "som",
    "Spanish": "spa",
    "Sundanese": "sun",
    "Swedish": "swe",
    "Tamil": "tam",
    "Telugu": "tel",
    "Thai": "tha",
    "Turkish": "tur",
    "Ukrainian": "ukr",
    "Undetermined": "und",
    "Urdu": "urd",
    "Uzbek": "uzb",
    "Vietnamese": "vie",
    "Yoruba": "yor",
    "Zulu": "zul",
}
AllVideosExtensions = ['AVI', 'MKV', 'MP4', 'M4V', 'MOV', 'MPEG', 'OGG', 'OGM', 'H264', 'H265', "WEBM", 'WMV']
AllSubtitlesExtensions = ['ASS', 'SRT', 'SSA', 'SUP', 'PGS']
AllSubtitlesLanguages = list(ISO_639_2_LANGUAGES.keys())
AllChapterExtensions = ['XML']
AllSubtitlesTracks = ["---Tracks---"]
AllSubtitlesTracks.extend(tracks_list)
AllSubtitlesTracks.append("---Languages---")
AllSubtitlesTracks.extend(list(ISO_639_2_LANGUAGES.keys()))
AllAudiosTracks = AllSubtitlesTracks
AllVideoDefaultDurationFPSLanguages = ['Default', '24p', '25p', '30p', '48p', '50i', '50p', '60i', '60p', '24000/1001p',
                                      '30000/1001p', '48000/1001p', '60000/1001i', '60000/1001p']
