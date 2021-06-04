FROM python:3.7.6-buster

WORKDIR /opt/app/
ENV GUNICORN_WORKERS=2
ENV GUNICORN_THREADS=30

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y 

COPY Pipfile Pipfile.lock ./
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN curl -O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo.h5 \
	-O -L https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5
WORKDIR /opt/app/


EXPOSE 5001
COPY app.py .

ENV FLASK_APP app.py
ENV FLASK_DEBUG 0

CMD gunicorn -b 0.0.0.0:5001 --keep-alive=120 --timeout=300 --worker-class=gthread app:app
