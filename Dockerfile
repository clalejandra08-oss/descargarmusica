# Usa una imagen oficial de Python ligera
FROM python:3.11-slim

# Instala FFmpeg y dependencias del sistema
RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    rm -rf /var/lib/apt/lists/*

# Instala yt-dlp a nivel de sistema para que esté disponible en el PATH
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp && \
    chmod a+rx /usr/local/bin/yt-dlp

# Establece el directorio de trabajo
WORKDIR /app

# Copia e instala las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto (Render inyecta la variable $PORT, pero exponer 8000 o 5000 es buena práctica)
EXPOSE 8000

# Comando para ejecutar la app con Gunicorn (producción)
# Se usa $PORT para que Render asigne el puerto dinámicamente
CMD gunicorn --bind 0.0.0.0:$PORT app:app
