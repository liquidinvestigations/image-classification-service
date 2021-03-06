FROM python:3.7.6-buster

WORKDIR /opt/app/

RUN apt-get update \
&& apt-get install -y ffmpeg libsm6 libxext6  \
&& rm -rf /var/lib/apt/lists/*


COPY Pipfile Pipfile.lock ./
COPY download_models.sh ./
COPY checksums ./
RUN chmod +x download_models.sh
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

RUN ./download_models.sh
WORKDIR /opt/app/


EXPOSE 5001
COPY app.py .
COPY tests ./tests
COPY runserver.sh ./runserver.sh
RUN chmod +x runserver.sh

ENV FLASK_APP app.py
ENV FLASK_DEBUG 0
ENV WORKER_COUNT 4

CMD ./runserver.sh
