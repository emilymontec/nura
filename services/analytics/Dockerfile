FROM python:3.11-slim

WORKDIR /app

# Actualizar pip
RUN pip install --upgrade pip

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

EXPOSE 8000
