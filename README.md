# yt2mp3

A youtube to mp3 converter.

Note: The website does not work; the program only works locally.

---

## Features

- Paste any YouTube URL and download it as an MP3
- Attach a custom image to embed as album art (ID3 cover tag)
- Tracks total conversions since launch

## Stack

| Layer | Tech |
|-------|------|
| Frontend | React, Vite, Tailwind CSS |
| Backend | FastAPI, yt-dlp, mutagen |
| Database | Supabase (conversion logging) |

## Running locally

### Prerequisites

- Python 3.10+
- Node.js 18+
- [ffmpeg](https://ffmpeg.org/download.html) on your `PATH`
- A [Supabase](https://supabase.com) project

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create `backend/.env`:

```
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

```bash
python yt2mp3.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create `frontend/.env` if pointing to a non-local backend:

```
VITE_BACKEND_URL=https://your-backend-url.com
```
