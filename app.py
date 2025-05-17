from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from audiocraft.models import MusicGen
from scipy.io.wavfile import write
import torch, uuid, os, tempfile

app = Flask(__name__, static_folder="static", static_url_path="/static")
CORS(app)

# Load model once at startup (GPU recommended)
model = MusicGen.get_pretrained("facebook/musicgen-small").cuda().eval()

@app.route("/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json(force=True)
    prompt   = data.get("prompt", "")
    duration = int(data.get("duration", 10))  # seconds (max 30)

    # Generate
    wav_tensor = model.generate(
        descriptions=[prompt],
        progress=False,
        use_sampling=True,
        top_k=250,
        duration=duration,
    )[0].cpu()   # (channels, samples)

    sample_rate = 32000
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmp.name, sample_rate, wav_tensor.T)

    os.makedirs(app.static_folder, exist_ok=True)
    out_name = f"{uuid.uuid4()}.wav"
    out_path = os.path.join(app.static_folder, out_name)
    os.replace(tmp.name, out_path)

    return jsonify({ "audio_url": request.url_root.rstrip("/") + "/static/" + out_name })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
