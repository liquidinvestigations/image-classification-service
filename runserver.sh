#!/bin/bash -ex

# waitress-serve --port 5001 --threads=$WAITRESS_THREADS app:app
exec gunicorn -b 0.0.0.0:5001 \
  --timeout=3600 \
  --worker-class=gthread --threads 8 --workers 5 \
  --max-requests 100 --max-requests-jitter 50 \
  app:app
