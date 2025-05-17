# MusicGen Backend (Flask)

A minimal Flask API that wraps Meta's MusicGen-small model and returns a WAV file link.

## Build locally
    docker build -t musicgen-backend .
    docker run --gpus all -p 8080:8080 musicgen-backend

## Endpoint
POST `/generate-audio`
    {
      "prompt": "lofi chill beat with piano",
      "duration": 12
    }
Response:
    { "audio_url": "https://<host>/static/<uuid>.wav" }

## Deploy to Railway
1. Create new project → Deploy from GitHub repo → Enable **GPU Spot**.
2. Keep port **8080** (default).
3. Click **Deploy** – logs will show build & runtime.
