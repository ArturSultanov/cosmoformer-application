#!/bin/sh
if [ -z "$WEB_CONCURRENCY" ]; then
  export WEB_CONCURRENCY=$(nproc)
fi

echo "INFO:     Number of workers: $WEB_CONCURRENCY"

exec uvicorn main:app --host 0.0.0.0 --port 8000 --workers "$WEB_CONCURRENCY"
