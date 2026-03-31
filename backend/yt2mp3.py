#!/usr/bin/env python3
"""
yt2mp3 - FastAPI backend to download a YouTube video and convert it to MP3.
"""

import base64
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from urllib.parse import quote
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()
import yt_dlp
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from mutagen.id3 import ID3, APIC, error as ID3Error
from mutagen.mp3 import MP3
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


def log_conversion(url: str) -> None:
    supabase.table("conversions").insert({
        "url": url,
        "converted_at": datetime.now(timezone.utc).isoformat(),
    }).execute()


COOKIES_FILE = os.environ.get("COOKIES_FILE")
COOKIES_BASE64 = os.environ.get("COOKIES_BASE64")

# If COOKIES_BASE64 is set, decode it to a temp file on startup
if COOKIES_BASE64 and not COOKIES_FILE:
    _cookies_path = os.path.join(tempfile.gettempdir(), "yt2mp3_cookies.txt")
    with open(_cookies_path, "wb") as f:
        f.write(base64.b64decode(COOKIES_BASE64))
    COOKIES_FILE = _cookies_path


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
        "remote_components": ["ejs:github"],
        "js_runtimes": {"node": {}, "deno": {}, "bun": {}},
    }
    if COOKIES_FILE and os.path.exists(COOKIES_FILE):
        ydl_opts["cookiefile"] = COOKIES_FILE

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        # For playlists/radio that slip through, grab the first entry
        if "entries" in info:
            info = info["entries"][0]
        raw = ydl.prepare_filename(info)
        base = os.path.splitext(os.path.basename(raw))[0]
        filepath = os.path.join(output_dir, f"{base}.mp3")
        return filepath, f"{base}.mp3"


@app.get("/stats")
def stats():
    result = supabase.table("conversions").select("converted_at", count="exact").order("converted_at", desc=False).limit(1).execute()
    return {
        "count": result.count,
        "since": result.data[0]["converted_at"] if result.data else None,
    }


@app.post("/convert")
async def convert(url: str = Form(...), image: UploadFile | None = File(None)):
    if not url:
        raise HTTPException(status_code=400, detail="No URL provided.")
    try:
        tmp_dir = tempfile.mkdtemp()
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(download_mp3, url, tmp_dir)
            try:
                filepath, filename = future.result(timeout=60)
            except FuturesTimeoutError:
                raise HTTPException(status_code=504, detail="Download timed out. The video may be too long or the server is slow.")

        if image is not None:
            image_data = await image.read()
            mime = image.content_type or "image/jpeg"
            audio = MP3(filepath, ID3=ID3)
            try:
                audio.add_tags()
            except ID3Error:
                pass
            audio.tags.add(APIC(encoding=3, mime=mime, type=3, desc="Cover", data=image_data))
            audio.save()

        log_conversion(url)
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
