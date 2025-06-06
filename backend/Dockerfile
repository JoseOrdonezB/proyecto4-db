# Usa imagen oficial de Python
FROM python:3.10-slim

# Establece variables de entorno recomendadas
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea y define el directorio de trabajo
WORKDIR /app

# Copia los archivos del backend al contenedor
COPY . .

# Instala dependencias
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto donde correrá Flask
EXPOSE 8000

# Comando por defecto para ejecutar Flask directamente
CMD ["python", "app.py"]