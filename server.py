from flask import Flask, request, jsonify
import requests
import whisper
import tempfile
import os

app = Flask(__name__)

# Carregar o modelo Whisper local
model = whisper.load_model("base")  # pode usar "tiny", "base", "small" ou "medium"

@app.route("/audio", methods=["POST"])
def process_audio():
    data = request.json
    audio_url = data.get("message", {}).get("url")

    if not audio_url:
        return jsonify({"error": "sem URL de áudio"}), 400

    # Baixar o áudio do WhatsApp (enviado pela FiQOn)
    audio_data = requests.get(audio_url).content

    # Salvar temporariamente
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as f:
        f.write(audio_data)
        temp_path = f.name

    # Transcrever com Whisper (rodando localmente)
    result = model.transcribe(temp_path, language="pt")

    # Deletar o arquivo temporário
    os.remove(temp_path)

    texto = result["text"].strip()

    # Retornar texto reconhecido
    return jsonify({
        "type": "text",
        "text": texto
    })

if __name__ == "__main__":
    app.run(port=5000)
