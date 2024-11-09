FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP run.py
ENV FLASK_ENV=development

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Run the application when the container starts
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
