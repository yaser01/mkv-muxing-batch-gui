# MKV Muxing Batch GUI

**For anyone who found this repo from this [issue](https://github.com/yaser01/mkv-muxing-batch-gui/issues/170). I will attempt to continue develop this. Not guarantee that development will last or not.**

A robust application for muxing(merging) videos with subtitles, audios, chapters, attachments alongside many customization options.

[![Github All Releases](https://img.shields.io/github/downloads/Khaoklong51/mkv-muxing-batch-gui/total.svg?color=4DC71F&label=Downloads&logo=github")](https://github.com/Khaoklong51/mkv-muxing-batch-gui/releases/latest)

- [MKV Muxing Batch GUI](#mkv-muxing-batch-gui)
  - [✨App Preview](#app-preview)
  - [📖Features](#features)
    - [Video Options](#video-options)
    - [Subtitle Options](#subtitle-options)
    - [Audio Options](#audio-options)
    - [Chapter Options](#chapter-options)
    - [Attachment Options](#attachment-options)
    - [Source Files Options](#source-files-options)
    - [Muxing Options](#muxing-options)
  - [📝Notes](#notes)
  - [📁Supported Extensions](#supported-extensions)
  - [⬇Downloads](#downloads)
    - [For Linux Users](#for-linux-users)
    - [Using Python Code Version](#using-python-code-version)
    - [Updating The MKVmerge version](#updating-the-mkvmerge-version)
  - [🙏Attribution](#attribution)
  - [🦟Report a Bug](#report-a-bug)
  - [🏷License](#license)

## ✨App Preview

_A preview of the application in action:_

<https://github.com/yaser01/mkv-muxing-batch-gui/assets/52576632/33f8bf3e-600c-4e0d-8ee2-ca51abdf79dc>

## 📖Features

### Video Options

- View media info of each file to monitor the video tracks
- Change default video duration/FPS [use this feature cautiously]

### Subtitle Options

- Add new subtitles to each video file
- Subtitles names **don't have to match** videos names
- Reorder the subtitles to match the right video
- Remove files from the subtitle tab
- Set subtitles to be default/forced
- Set subtitle delay, track name, language
- Mux the new subtitle at any desired position in the output video
- Add multiple subtitles to each video file with individual settings for each subtitle

### Audio Options

- Add new audios to each video file
- Audios names **don't have to match** videos names
- Reorder the audios to match the right video
- Remove files from the audio tab
- Set audios to be default/forced
- Set audio delay, track name, language
- Mux the new audio at any desired position in the output video
- Add multiple audios to each video file with individual settings for each audio

### Chapter Options

- Add new chapters to each video file
- Chapters names **don't have to match** videos names
- Reorder the chapters to match the right video
- Remove files from the chapter tab

### Attachment Options

- Add new attachments to all video files
- Discard old attachments files from all videos
- Ability to attach file/folder for each video separately [expert mode]
- Option to prevent adding duplicate existing attachments [any existing attachment in source video will be skipped]

### Source Files Options

- Discard old subtitles
- Keep subtitles with specific language(s) and/or track id(s) while discarding any other subtitle
- Discard old audios
- Keep audios with specific language(s) or track id(s) while discarding any other audio
- Set an old subtitle track to be default/forced
- Set an old audio track to be default/forced
- Modify existing tracks **(each track separately)** like: track name,delete,set default,set forced and language, even you can change their order with shortcuts `Ctrl + Up Arrow / Ctrl + Down Arrow`

### Muxing Options

- Override global settings by changing subtitle/audio settings (delay, track name, language) for each subtitle/audio file
- Save a log file
- Set your default directories, languages, and file extensions to be remembered for future runs
- Optimize your muxing by modifying the source file when feasible. A prompt will appear when this option is available

## 📝Notes

> [!NOTE]
>
>1. Leaving destination folder empty will lead to overwrite source videos a popup will shown to confirm this action.
>2. When the option [make this subtitle/audio default] is activated with language/track that does not exist in the source, then the option will be ignored.
>3. When the option [keep this subtitle/audio only] is activated with language/track that does not exist in the source video, then the option will lead to output video with only chosen language/track (even if it means to discard all subtitle/audio from the source).
>4. When using `Modify Old Tracks` in video tab, the following options: (make this subtitle/audio default, keep this subtitle/audio only, mux new subtitle/audio in desired position) will be **disabled/limited**.
>5. When using `mux subtitle/audio` at same position for the same track type, they will be added respecting to the order of all other new subtitles/audio.
>6. In every tab/dialog you can reorder tracks using shortcuts `Ctrl + Up Arrow / Ctrl + Down Arrow` except for: (Attachment/Muxing Tab).

## 📁Supported Extensions

|     Type    |                                        Extensions                                       |
|:-----------:|:---------------------------------------------------------------------------------------:|
|   Video     | AVI, MKV, MP4, M4V, MOV, MPEG, TS, OGG, OGM, H264, H265, WEBM, WMV, IVF, M2TS, VOB      |
|  Subtitle   | ASS, SRT, SSA, SUP, PGS, MKS, VTT, SUB                                                  |
|   Audio     | AAC, AC3, FLAC, EAC3, MKA, M4A, MP3, DTS, DTSMA, THD, WAV, OGG, OPUS                    |
|   Chapter   | XML                                                                                     |

## ⬇Downloads

The MKV Muxing Batch GUI is compatible with Windows 10/11 64-bit and most Linux distributions.
You can download it from the project's [releases&nbsp;page](https://github.com/Khaoklong51/mkv-muxing-batch-gui/releases/).

### For Linux Users

The deployed app available in downloads only support glibc 2.17 and above.
Before starting the app, install the following libraries [not always needed as most of them included in the app]:

```bash
sudo apt-get install -y libpugixml-dev
sudo apt-get install -y libmatroska-dev
sudo apt install libxcb-cursor0
```

### Using Python Code Version

1. Clone the repository :`git clone https://github.com/Khaoklong51/mkv-muxing-batch-gui.git`.
2. The main branch use ``PySide6`` library on version `6.10.0` which is tested on `python 3.13.3` working good and only supporting x64 systems.
3. After selecting the branch just make sure to use the mentioned python version as it's guaranteed to work perfect.
4. Just run `pip install -r requirements.txt`.
5. Then run `python main.py` and you are all good :D.
6. You may use `python3/pip3` instead of `python/pip` depending on your system.
7. For linux users if you want to use another python version from the one that is already on your system it's recommended to use `uv`,if you didn't hear about it, you may read [this](https://github.com/astral-sh/uv).
8. Also, for linux users: as this app depends on mkvtoolnix it's very recommended to install it on your system before run the app from your distro repository.

### Updating The MKVmerge version

Program will automatically detect install mkvtoolnix in this order PATH >> Common install location (Windows Only) (C:\\Program Files\\MKVToolNix) >> Portable (Resources\\Tools\\[your operating system])

You can manually update the mkvmerge version for portable version, but do this only if you're sure of what you're doing, as it may require a reinstallation:

```bash
# Navigate to the app's installation directory, e.g. on Windows:
"C:\\Program Files (x86)\\MKV Muxing Batch GUI"
# Go to Resources\\Tools\\ [your operating system], and replace mkvmerge.exe and mkvpropedit.exe with the newer version you have
```

> For linux users it's recommended to install mkvtoolnix from your distro repository and the app will automatically detect it.

## 🙏Attribution

- The application relies heavily on [MKVToolNix](https://codeberg.org/mbunkus/mkvtoolnix), so a big thanks to them.
- Thanks to my friends who helped test the app and offered numerous ideas.

## 🦟Report a Bug

Any software bugs can be reported on the project's [issues page](https://github.com/Khaoklong51/mkv-muxing-batch-gui/blob/main/LICENSE). Suggestions for future updates are also welcome.

## 🏷License

[![GitHub](https://img.shields.io/github/license/Khaoklong51/mkv-muxing-batch-gui?style=for-the-badge)](https://github.com/Khaoklong51/mkv-muxing-batch-gui/blob/main/LICENSE)
