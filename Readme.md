# MKV Muxing Batch GUI

App for muxing(merging) videos with [subtitles,audios,chapters,attachments] with many options.

## App Preview
https://user-images.githubusercontent.com/52576632/136703937-ee0e7eb5-c6f2-456e-a890-0fed94f54f42.mp4
## Videos Options

>1. You can view media info of each file so you can keep an eye on the video tracks
>1. You can change default video duration/FPS [only if you really know what you are doing] 

## Subtitles Options

>1. Add new subtitle to each video file
>1. Subtitles names **don't have to match** videos names
>1. You can reorder the subtitles so that each subtitle is matched with the right video
>1. You can set subtitles to be default/forced
>1. You can set subtitle delay, track name, language
>1. You can set the new subtitle to be at the top of subtitles tracks in the output video [instead of adding it at the last]
>1. You can add multiple subtitles to each video file [individual settings for each subtitle]

## Audios Options

>1. Add new audio to each video file
>1. Audios names **don't have to match** videos names
>1. You can reorder the audios so that each audio is matched with the right video
>1. You can set audios to be default/forced
>1. You can set audio delay, track name, language
>1. You can set the new audio to be at the top of audios tracks in the output video [instead of adding it at the last]
>1. You can add multiple audios to each video file [individual settings for each audio]

## Chapters Options

>1. add new chapter to each video file
>1. Chapters names **don't have to match** videos names
>1. You can reorder the chapters so that each chapter is matched with the right video

## Attachments Options

>1. Add new attachments to all video files
>1. You can discard old attachments files from all videos

## Source Files Options [Only Works for MKV files]

>1. You can discard old subtitles  
>1. You can keep subtitles with specific language(s) and/or track id(s) and discard any other subtitle
>1. You can discard old audios
>1. You can keep audios with specific language(s) or track id(s) and discard any other audio
>1. You can set an old subtitle track to be default/forced
>1. You can set an old audio track to be default/forced
>1. If your muxing is limited to add/delete [attachments,chapters], or make old track default/forced, you can make it fast [by modifying the source file], a prompt will appear when this happen

## Muxing Options

>1. You can change subtitle/audio settings(delay, track name, language) for each subtitle/audio file to override global settings
>1. You can save a log file
>1. You can set your default [directories - languages - files extensions] so the app will remember them in the next run.

## Notes

>1. the video destination folder shouldn't be the same as source folder
>1. When the option [keep this subtitle/audio only] is activated with language/track that does not exist in the source video, then the option will lead to output video with only chosen language/track (even if it means to discard all subtitle/audio from the source)
>1. When the option [make this subtitle/audio default] is activated with language/track that does not exists in the source, then the option will be ignored

## Supported Extensions

**Video**:
[AVI, MKV, MP4, M4V, MOV, MPEG, TS, OGG, OGM, H264, H265, WEBM, WMV]

**Subtitle**:
[ASS, SRT, SSA, SUP, PGS, MKS, VTT]

**Audio**:
[AAC, AC3, FLAC, EAC3, MKA, M4A, MP3, DTS, DTSMA, THD, WAV, OGG, OPUS]

**Chapter**:
[XML]

## 💾 Downloads

[![Github All Releases](https://img.shields.io/github/downloads/yaser01/mkv-muxing-batch-gui/total.svg?color=4DC71F&label=Downloads&logo=github")](https://github.com/yaser01/mkv-muxing-batch-gui/releases/latest)
[![Donate](https://img.shields.io/badge/Donate-Buy_Me_A_Coffe-blueviolet.svg)](https://www.buymeacoffee.com/yaser01)
<br>
MKV Muxing Batch GUI works on Windows 7/8/8.1/10/11 32-bit/64-bit
<br>Now Support most of Linux distributions :D
See the project's [releases&nbsp;page](https://github.com/yaser01/mkv-muxing-batch-gui/releases) for download links

### For Linux Users
Before starting the app make sure to install the following libraries using commands:
>sudo apt-get install -y libpugixml-dev
> <br>
>sudo apt-get install -y libmatroska-dev
## 🙏 Attribution

- The whole app depends on mkvmerge and mkvpropedit so Big thanks to [MKVToolNix](https://gitlab.com/mbunkus/mkvtoolnix)
- Big thanks to my friends who helped me in testing the app and provided a lot of ideas

## 🦟 Software bugs

Bugs reported on the project's [issues page](https://github.com/yaser01/mkv-muxing-batch-gui/issues) will be checked weakly and I'm looking forward any suggestions for future updates

## 🏷️ License

GPLv2 © [yaser01](https://github.com/yaser01/mkv-muxing-batch-gui/blob/main/LICENSE)
