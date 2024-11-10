FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV FLASK_ENV=development

# Install FFmpeg dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Run the application when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
