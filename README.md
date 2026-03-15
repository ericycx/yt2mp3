# yt2mp3

A simple command-line tool to download YouTube videos and convert them to MP3.

## Requirements

- Python 3.8+
- [ffmpeg](https://ffmpeg.org/download.html) installed and available on your `PATH`

## Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/your-username/yt2mp3.git
   cd yt2mp3
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install ffmpeg (if not already installed):
   - **macOS:** `brew install ffmpeg`
   - **Ubuntu/Debian:** `sudo apt install ffmpeg`
   - **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Usage

```bash
python yt2mp3.py <youtube_url> [output_dir]
```

**Examples:**

```bash
# Save to current directory
python yt2mp3.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Save to a specific folder
python yt2mp3.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" ~/Music
```

The MP3 file will be saved using the video's title as the filename.

