#!/usr/bin/env python3
"""
yt2mp3 - FastAPI backend to download a YouTube video and convert it to MP3.
"""

import os
import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    url: str


def download_mp3(url: str, output_dir: str = DOWNLOADS_DIR) -> str:
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
        "quiet": True,
        "no_warnings": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "audio")
        filename = os.path.join(output_dir, f"{title}.mp3")
        return filename


@app.post("/convert")
def convert(request: ConvertRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="No URL provided.")
    try:
        filepath = download_mp3(request.url)
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            filename=os.path.basename(filepath),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("yt2mp3:app", host="0.0.0.0", port=8000, reload=True)
