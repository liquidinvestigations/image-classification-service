FROM python:3.7.6-buster

WORKDIR /opt/app/
ENV GUNICORN_WORKERS=2
ENV GUNICORN_THREADS=30

ENV OBJECT_DETECTION_ENABLED=true
ENV OBJECT_DETECTION_MODEL=yolo

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y 

COPY Pipfile Pipfile.lock ./
COPY download_models.sh ./
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN download_models.sh
WORKDIR /opt/app/


EXPOSE 5001
COPY app.py .
COPY tests ./tests

ENV FLASK_APP app.py
ENV FLASK_DEBUG 0

CMD gunicorn -b 0.0.0.0:5001 --keep-alive=120 --timeout=300 --worker-class=gthread app:app
