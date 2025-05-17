# MusicGen Backend (Flask)

A minimal Flask API that wraps Meta's MusicGen-small model and returns a WAV file link.

## Build locally
```bash
docker build -t musicgen-backend .
docker run --gpus all -p 8080:8080 musicgen-backend
