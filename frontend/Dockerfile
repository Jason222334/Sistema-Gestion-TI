FROM python:3.11-slim

WORKDIR /app

# Actualizamos e instalamos solo curl para el healthcheck
# Se eliminó el paquete "software-properties-common" que causaba el error
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Exponer el puerto de Streamlit
EXPOSE 8501

# Chequeo de salud para verificar que la app responda
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Comando de arranque específico para Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]