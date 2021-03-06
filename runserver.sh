#!/bin/bash -ex

python app.py || ( echo "runserver.sh: setup test failed!" && sleep 60 && exit 1 )

exec gunicorn -b 0.0.0.0:5001 \
  --name image-classification \
  --timeout=500 \
  --worker-class=sync --workers $WORKER_COUNT --threads 1 \
  --max-requests 100 --max-requests-jitter 50 \
  app:app
