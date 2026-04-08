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

## Deployment

The frontend and backend are deployed separately:

### Frontend — Vercel

1. Import the repo on [Vercel](https://vercel.com)
2. Set the root directory to `frontend`
3. Add environment variable: `VITE_BACKEND_URL=https://your-railway-backend.up.railway.app`
4. Deploy

### Backend — Railway

1. Create a new project on [Railway](https://railway.app) and connect the repo
2. Set the root directory to `backend`
3. Add environment variables: `SUPABASE_URL`, `SUPABASE_KEY`
4. Railway will auto-detect Python — add a start command: `python yt2mp3.py`
5. Make sure ffmpeg is available (add it via a `nixpacks.toml` or Railway's nixpacks config)

Once the backend is deployed, copy its Railway URL and set it as `VITE_BACKEND_URL` on Vercel.
