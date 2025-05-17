from flask import Flask, request, jsonify
from flask_cors import CORS
from audiocraft.models import MusicGen
from scipy.io.wavfile import write
import torch, uuid, os, tempfile

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# ───────────  Load model once (CPU או CUDA) ───────────
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[Harmony-AI] Loading MusicGen-small on {device} …")
model = MusicGen.get_pretrained("small")   # אין .eval / .to ב-0.0.2

@app.route("/", methods=["GET"])
def ping():
    return "OK", 200

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data      = request.get_json(force=True) or {}
    prompt    = data.get("prompt", "")
    duration  = max(1, min(int(data.get("duration", 10)), 30))  # 1-30 s

    wav_tensor = model.generate(
        descriptions=[prompt],
        progress=False,
        use_sampling=True,
        top_k=250,
        duration=duration,
    )[0].cpu()   # (channels, samples)

    # save wav
    sample_rate = 32_000
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmp.name, sample_rate, wav_tensor.T)

    os.makedirs(app.static_folder, exist_ok=True)
    out_name = f"{uuid.uuid4()}.wav"
    os.replace(tmp.name, os.path.join(app.static_folder, out_name))

    return jsonify({
        "audio_url": request.url_root.rstrip("/") + "/static/" + out_name
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
