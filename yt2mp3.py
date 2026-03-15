#!/usr/bin/env python3
"""
yt2mp3 - Download a YouTube video and convert it to MP3.

Usage:
    python yt2mp3.py <youtube_url> [output_dir]
"""

import sys
import os
import yt_dlp


def download_mp3(url: str, output_dir: str = ".") -> None:
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
        "no_warnings": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main() -> None:
    url = input("Enter YouTube URL: ").strip()
    if not url:
        print("No URL provided.")
        sys.exit(1)

    print(f"Downloading: {url}")
    download_mp3(url, ".")
    print("Done.")

if __name__ == "__main__":
    main()
