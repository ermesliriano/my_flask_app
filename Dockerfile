# Usar una imagen base de Python (por ejemplo, versión 3.9 slim)
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro de la imagen
WORKDIR /app

# Copiar los archivos de requerimientos e instalarlos
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiar el código de la aplicación al contenedor
COPY . .

# Establecer variables de entorno necesarias (ejemplo de Flask)
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Exponer el puerto 5000 para la aplicación Flask
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]