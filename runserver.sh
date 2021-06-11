#!/bin/bash -ex

waitress-serve --port 5001 --threads=$WAITRESS_THREADS app:app
