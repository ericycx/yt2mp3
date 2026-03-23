#!/usr/bin/env python3
"""
yt2mp3 - FastAPI backend to download a YouTube video and convert it to MP3.
"""

import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from urllib.parse import quote
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Filename"],
)


class ConvertRequest(BaseModel):
    url: str


def log_conversion(url: str) -> None:
    supabase.table("conversions").insert({
        "url": url,
        "converted_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


def download_mp3(url: str, output_dir: str) -> tuple[str, str]:
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
        "noplaylist": True,       # never download full playlists
        "quiet": True,
        "no_warnings": True,
        "socket_timeout": 30,     # bail if connection stalls
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # For playlists/radio that slip through, grab the first entry
        if "entries" in info:
            info = info["entries"][0]
        raw = ydl.prepare_filename(info)
        base = os.path.splitext(os.path.basename(raw))[0]
        filepath = os.path.join(output_dir, f"{base}.mp3")
        return filepath, f"{base}.mp3"


@app.post("/convert")
def convert(request: ConvertRequest):
    if not request.url:
        raise HTTPException(status_code=400, detail="No URL provided.")
    try:
        tmp_dir = tempfile.mkdtemp()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(download_mp3, request.url, tmp_dir)
            try:
                filepath, filename = future.result(timeout=120)
            except FuturesTimeoutError:
                raise HTTPException(status_code=504, detail="Download timed out. The video may be too long or the server is slow.")
        log_conversion(request.url)
        return FileResponse(
            filepath,
            media_type="audio/mpeg",
            headers={"X-Filename": quote(filename)},
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("yt2mp3:app", host="0.0.0.0", port=8000, reload=True)
