# --- Etapa 1: Builder (Instalación de dependencias) ---
FROM python:3.14-slim AS builder

# Evitar archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN pip install --upgrade pip

# Instalar dependencias en un directorio específico
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


# --- Etapa 2: Runtime (Imagen final pequeña) ---
FROM python:3.14-slim

# Crear usuario no privilegiado por seguridad
RUN groupadd -g 1000 appuser && \
    useradd -r -u 1000 -g appuser appuser

WORKDIR /app

# Copiar solo los paquetes instalados de la etapa builder
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Ajustar permisos
RUN chown -R appuser:appuser /app

# Usar el usuario no root
USER appuser

# Añadir las dependencias al PATH
ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

# Lanzar con workers para producción (Uvicorn + Gunicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
