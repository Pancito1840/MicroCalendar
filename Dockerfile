#Imagen base ligera
FROM python:3.12-slim

#definir directorio de trabajo
WORKDIR /app

#instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

#copiar e instalar dependencias de requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#copiar el codigo de la aplicacion
COPY . .

#crear usuario sin privilegios
RUN useradd -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

#Exponer puerto 8000 y comando de arranque de uvicorn en 0.0.0.0
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1" ]

#Instrucción HEALTHCHECK consultando /health/live
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
CMD curl -f http://localhost:8000/health/live || exit 1
