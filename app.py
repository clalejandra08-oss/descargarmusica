import os
import subprocess
import zipfile
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
DOWNLOAD_DIR = "descargas"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/descargar", methods=["POST"])
def descargar():
    lista_texto = request.form.get("canciones", "").strip()
    if not lista_texto:
        return "No se proporcionó ninguna canción", 400

    canciones = [line.strip() for line in lista_texto.splitlines() if line.strip()]
    archivos_generados = []

    for cancion in canciones:
        # ytsearch1: busca en YouTube y toma el primer resultado
        query = f"ytsearch1:{cancion}"
        comando = [
            "yt-dlp",
            query,
            "-x",                      # extraer audio
            "--audio-format", "mp3",   # convertir a MP3
            "--audio-quality", "0",    # mejor calidad
            "-o", os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
            "--no-playlist",
            "--quiet",
        ]
        try:
            subprocess.run(comando, check=True, timeout=300)
            # Buscar el archivo MP3 generado (puede tener un nombre dinámico)
            # Para simplificar, asumimos que el archivo se creó en DOWNLOAD_DIR
            # En producción, se puede capturar la salida de yt-dlp para obtener el nombre exacto.
        except subprocess.CalledProcessError:
            print(f"Error al descargar: {cancion}")
            continue

    # Empaquetar todos los MP3 en un ZIP
    zip_path = os.path.join(DOWNLOAD_DIR, "canciones.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for archivo in os.listdir(DOWNLOAD_DIR):
            if archivo.endswith(".mp3"):
                zipf.write(os.path.join(DOWNLOAD_DIR, archivo), arcname=archivo)

    return send_file(zip_path, as_attachment=True, download_name="canciones.zip")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
