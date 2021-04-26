# MKV Muxing Batch GUI

App to muxing /merge/ videos with [subtitles,chapters,attachments] with many options.<br>

### App Preview
https://user-images.githubusercontent.com/52576632/116090926-0944f800-a6ad-11eb-8fc4-4732588ca00e.mp4

### Subtitles Options
>1. Add new subtitle to each video file
>1. Subtitles names **don't have to match** videos names
>1. The app provide a feature to reorder subtitles as you want
>1. You can set subtitles to be default/forced
>1. You can set subtitles delay ,track name,language
### Chapters Options
>1. add new chapter to each video file
>1. Chapters names **don't have to match** videos names
>1. The app provide a feature to reorder chapters as you want
## Attachments Options
>1. Add new attachments to all video files 
>1. You can discard old attachments files from all videos 
## Source Files Options [Only Works for MKV Source files]
>1. You can discard old subtitles  
>1. You can keep only subtitles with specific language(s) or tracks ids
>1. You can discard old audios  
>1. You can keep only audios with specific language(s) or tracks ids
>1. You can make an old subtitle track to be default/forced [can be determined with language or track id]
>1. You can make an old audio track to be default/forced [can be determined with language or track id]
>1. If your muxing is limited to add/delete [attachments,chapters] or make old track default/forced you can make it fast like flash [by modifying the source itself] a prompt will show when it happens

## Muxing Options
>1. You will progress bar for each video source plus a total progress for all
>1. You can change subtitle settings like:[delay ,track name,language] for each subtitle file to override global setting
>1. You can pause muxing if you forget some setting 
>1. You will have track of old and new file size for each video
>1. You can show log file to keep eye on everything happened 
## Notes
>1. In general case video source folder shouldn't match destination video folder
>1. When option [keep this subtitle/audio only] is activated with language/track isn't even exists in the source,
><br>the option will lead to output video with only chosen language/track  [even if it means to discard all subtitle/audio from the source]
>1. When option [make this subtitle/audio default] is activated with language/track isn't even exists in the source,
><br>the option will be ignored
## Supported Extensions
The following file types are supported.

**Video**:
[AVI, MKV, MP4, M4V, MOV, MPEG, OGG, OGM, H264, H265, WEBM, WMV]

**Subtitle**:
[ASS, SRT, SSA, SUP, PGS]

**Chapter**:
[XML]

## 💾 Downloads
MKV Muxing Batch GUI works on Windows 7  32-bit/64-bit and above operating systems  also linux version to make linux users happy :) <br>
See the project's [releases&nbsp;page](https://github.com/yaser01/mkv-muxing-batch-gui/releases) for download links.
<br><br>
## 🙏 Attribution
- The whole app depends on mkvmerge and mkvpropedit so Big thanks to [MKVToolNix](https://gitlab.com/mbunkus/mkvtoolnix)
- Icons used from different sources will all copyrights reserved
- Big thanks to my friends who help me testing the app and giving me lots of ideas :D
<br><br>
## 🦟 Software bugs
Bugs reported on the project's [issues page](https://github.com/yaser01/mkv-muxing-batch-gui/issues) will be checked weakly and i'm looking forward any reasonable idea to add :D
<br><br>

## 🏷️ License
GPLv2 © [yaser01](https://github.com/yaser01/mkv-muxing-batch-gui/blob/main/LICENSE)
