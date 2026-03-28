# yt2mp3

A web app to download YouTube videos as MP3s, with optional album art embedding.

## Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** FastAPI + yt-dlp + mutagen

## Requirements

- Python 3.10+
- Node.js 18+
- [ffmpeg](https://ffmpeg.org/download.html) installed and on your `PATH`
- A [Supabase](https://supabase.com) project (for conversion logging)

## Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in `backend/`:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

Run the backend:

```bash
python yt2mp3.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Usage

1. Paste a YouTube URL into the input field
2. Optionally attach an image to embed as album art
3. Click **Convert** — the MP3 will download automatically
