#!/usr/bin/env python3
"""
Download audio from a YouTube playlist using yt-dlp.

Use this only for videos you own, videos with a license that permits downloads,
or content you otherwise have permission to download. This script does not
bypass DRM or access controls.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

try:
    import yt_dlp
except ImportError as exc:
    raise SystemExit(
        "Missing dependency: yt-dlp\n"
        "Install it with: python -m pip install -r requirements_youtube_audio.txt"
    ) from exc


SUPPORTED_AUDIO_FORMATS = ("mp3", "m4a", "opus", "wav", "flac", "vorbis")


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed < 1:
        raise argparse.ArgumentTypeError("must be 1 or greater")
    return parsed


def build_options(args: argparse.Namespace) -> dict[str, Any]:
    output_dir = Path(args.output).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    postprocessors: list[dict[str, Any]] = []
    if args.audio_format:
        postprocessors.append(
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": args.audio_format,
                "preferredquality": str(args.audio_quality),
            }
        )

    options: dict[str, Any] = {
        "format": "bestaudio/best",
        "ignoreerrors": True,
        "noplaylist": False,
        "outtmpl": str(output_dir / "%(playlist_index)03d - %(title).200B.%(ext)s"),
        "postprocessors": postprocessors,
        "restrictfilenames": args.safe_filenames,
        "writethumbnail": args.thumbnail,
        "writesubtitles": False,
        "quiet": False,
        "no_warnings": False,
    }

    if args.start or args.end:
        options["playliststart"] = args.start or 1
        if args.end:
            options["playlistend"] = args.end

    if args.archive:
        archive_path = Path(args.archive).expanduser().resolve()
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        options["download_archive"] = str(archive_path)

    return options


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download audio from a YouTube playlist you have permission to save."
    )
    parser.add_argument("playlist_url", help="YouTube playlist URL")
    parser.add_argument(
        "-o",
        "--output",
        default="downloads",
        help="folder to save audio files in, default: downloads",
    )
    parser.add_argument(
        "-f",
        "--audio-format",
        choices=SUPPORTED_AUDIO_FORMATS,
        default="mp3",
        help="audio format to save, default: mp3; requires ffmpeg",
    )
    parser.add_argument(
        "-q",
        "--audio-quality",
        type=positive_int,
        default=192,
        help="audio bitrate/quality passed to ffmpeg, default: 192",
    )
    parser.add_argument(
        "--start",
        type=positive_int,
        help="first playlist item number to download",
    )
    parser.add_argument(
        "--end",
        type=positive_int,
        help="last playlist item number to download",
    )
    parser.add_argument(
        "--archive",
        help="path to a download archive file so reruns skip completed videos",
    )
    parser.add_argument(
        "--thumbnail",
        action="store_true",
        help="also save video thumbnails",
    )
    parser.add_argument(
        "--safe-filenames",
        action="store_true",
        help="restrict filenames to ASCII-safe characters",
    )

    args = parser.parse_args()
    if args.end and args.start and args.end < args.start:
        parser.error("--end must be greater than or equal to --start")
    return args


def main() -> int:
    args = parse_args()
    options = build_options(args)

    print("Only download content you own or have permission to download.")
    with yt_dlp.YoutubeDL(options) as downloader:
        downloader.download([args.playlist_url])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
