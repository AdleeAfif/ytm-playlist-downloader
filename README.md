# YouTube Playlist Audio Helper

This folder contains scripts for downloading audio from a YouTube playlist you own, a playlist with content licensed for download, or content you otherwise have permission to save.

## Files You Need

Keep these 3 files together in the same folder:

- `youtube_playlist_audio.py`
- `requirements_youtube_audio.txt`
- `run_playlist_audio_and_archive.ps1`

The `__pycache__` folder is created automatically by Python and is not needed.

## First-Time Requirements

You need Python installed.

For MP3 conversion, you also need `ffmpeg` installed and available on your PATH.

For `.rar` archives, install WinRAR. If WinRAR/RAR is not found, the helper script will create a `.zip` archive instead.

## Run It For Any Playlist

Open PowerShell and run:

```powershell
cd "C:\Users\{username}\Documents\Codex\2026-06-23\cr\outputs"

powershell -ExecutionPolicy Bypass -File .\run_playlist_audio_and_archive.ps1 -PlaylistUrl "PASTE_PLAYLIST_URL_HERE"
```

Example:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_playlist_audio_and_archive.ps1 -PlaylistUrl "https://music.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
```

## Where Files Are Saved

Audio files are saved here:

```text
C:\Users\{username}\Downloads\youtube_playlist_audio
```

The archive is saved in your Downloads folder with a timestamped name, for example:

```text
C:\Users\{username}\Downloads\youtube_playlist_audio_20260623_143012.rar
```

If WinRAR/RAR is not installed, it will create:

```text
C:\Users\{username}\Downloads\youtube_playlist_audio_20260623_143012.zip
```

## Useful Options

Change audio format:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_playlist_audio_and_archive.ps1 -PlaylistUrl "PASTE_PLAYLIST_URL_HERE" -AudioFormat m4a
```

Change audio quality:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_playlist_audio_and_archive.ps1 -PlaylistUrl "PASTE_PLAYLIST_URL_HERE" -AudioQuality 320
```

Supported formats include:

- `mp3`
- `m4a`
- `opus`
- `wav`
- `flac`
- `vorbis`

## Notes

The helper installs or updates `yt-dlp` automatically using:

```powershell
python -m pip install -r requirements_youtube_audio.txt
```

It also uses a download archive file at:

```text
C:\Users\{username}\Downloads\youtube_playlist_audio\downloaded.txt
```

That means rerunning the same playlist should skip tracks that already downloaded successfully.
