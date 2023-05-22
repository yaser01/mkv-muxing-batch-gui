# MKV Muxing Batch GUI

A robust application for muxing(merging) videos with subtitles, audios, chapters, attachments alongside many customization options.

[![Github All Releases](https://img.shields.io/github/downloads/yaser01/mkv-muxing-batch-gui/total.svg?color=4DC71F&label=Downloads&logo=github")](https://github.com/yaser01/mkv-muxing-batch-gui/releases/latest)
[![Donate](https://img.shields.io/badge/Donate-Buy_Me_A_Coffe-blueviolet.svg)](https://www.buymeacoffee.com/yaser01)

- [App Preview](#app-preview)
- [Features](#features)
    - [Video Options](#video-options)
    - [Subtitle Options](#subtitle-options)
    - [Audio Options](#audio-options)
    - [Chapter Options](#chapter-options)
    - [Attachment Options](#attachment-options)
    - [Source Files Options](#source-files-options)
    - [Muxing Options](#muxing-options)
- [Notes](#notes)
- [Supported Extensions](#supported-extensions)
- [Downloads](#downloads)
    - [For Linux Users](#for-linux-users)
    - [Updating the MKVmerge version](#updating-the-mkvmerge-version)
- [Attribution](#attribution)
- [Report a Bug](#report-a-bug)
- [License](#license)

## ✨App Preview
_A preview of the application in action:_

https://user-images.githubusercontent.com/52576632/166163331-b8fe2e9c-3f5c-4967-9ce5-9b6f5231956d.mp4

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
- Position the new subtitle at the top of subtitles tracks in the output video
- Add multiple subtitles to each video file with individual settings for each subtitle

### Audio Options
- Add new audios to each video file
- Audios names **don't have to match** videos names
- Reorder the audios to match the right video
- Remove files from the audio tab
- Set audios to be default/forced
- Set audio delay, track name, language
- Position the new audio at the top of audios tracks in the output video
- Add multiple audios to each video file with individual settings for each audio

### Chapter Options
- Add new chapters to each video file
- Chapters names **don't have to match** videos names
- Reorder the chapters to match the right video
- Remove files from the chapter tab

### Attachment Options
- Add new attachments to all video files
- Discard old attachments files from all videos

### Source Files Options
- Discard old subtitles
- Keep subtitles with specific language(s) and/or track id(s) while discarding any other subtitle
- Discard old audios
- Keep audios with specific language(s) or track id(s) while discarding any other audio
- Set an old subtitle track to be default/forced
- Set an old audio track to be default/forced
- Optimize your muxing by modifying the source file when feasible. A prompt will appear when this option is available

### Muxing Options
- Override global settings by changing subtitle/audio settings (delay, track name, language) for each subtitle/audio file
- Save a log file
- Set your default directories, languages, and file extensions to be remembered for future runs

## 📝Notes
>**Note**

>1. The video destination folder shouldn't be the same as source folder
>1. When the option [make this subtitle/audio default] is activated with language/track that does not exists in the source, then the option will be ignored
>1. When the option [keep this subtitle/audio only] is activated with language/track that does not exist in the source video, then the option will lead to output video with only chosen language/track (even if it means to discard all subtitle/audio from the source)

## 📁Supported Extensions
- **Video**: AVI, MKV, MP4, M4V, MOV, MPEG, TS, OGG, OGM, H264, H265, WEBM, WMV
- **Subtitle**: ASS, SRT, SSA, SUP, PGS, MKS, VTT
- **Audio**: AAC, AC3, FLAC, EAC3, MKA, M4A, MP3, DTS, DTSMA, THD, WAV, OGG, OPUS
- **Chapter**: XML

## ⬇Downloads

The MKV Muxing Batch GUI is compatible with Windows 7/8/8.1/10/11 32-bit/64-bit and most Linux distributions. 
You can download it from the project's [releases&nbsp;page](https://github.com/yaser01/mkv-muxing-batch-gui/releases).

### For Linux Users
Before starting the app, install the following libraries:
```bash
sudo apt-get install -y libpugixml-dev
sudo apt-get install -y libmatroska-dev
```

### Updating The MKVmerge version
You can manually update the mkvmerge version the app uses, but do this only if you're sure of what you're doing, as it may require a reinstall:
```bash
# Navigate to the app's installation directory, e.g. on Windows:
"C:\\Program Files (x86)\\MKV Muxing Batch GUI"
# Go to Resources\\Tools\\ [your operating system], and replace mkvmerge.exe and mkvpropedit.exe with the newer version you have
```

## 🙏Attribution
- The application relies heavily on [MKVToolNix](https://gitlab.com/mbunkus/mkvtoolnix), so a big thanks to them.
- Thanks to my friends who helped test the app and offered numerous ideas.

## 🦟Report a Bug
Any software bugs can be reported on the project's [issues page](https://github.com/yaser01/mkv-muxing-batch-gui/issues). Suggestions for future updates are also welcome.

## 🏷License

[![GitHub](https://img.shields.io/github/license/yaser01/mkv-muxing-batch-gui?style=for-the-badge)](https://github.com/yaser01/mkv-muxing-batch-gui/blob/main/LICENSE)

<div align="right">
<table><td>
<a href="#start-of-content">👆 Scroll to top</a>
</td></table>
</div>
