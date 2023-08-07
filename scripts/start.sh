#!/bin/bash
gunicorn src.main:app --workers 13 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8001