#!/bin/bash -ex

exec gunicorn -b 0.0.0.0:5001 \
  --timeout=3600 \
  --worker-class=gthread --threads 8 --workers 5 \
  --max-requests 100 --max-requests-jitter 50 \
  app:app
