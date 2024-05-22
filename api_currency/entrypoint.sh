#!/bin/bash

alembic -c alembic.ini upgrade head

uvicorn src.entrypoints.main:app --host 0.0.0.0 --port 8000  --reload --log-config=log_conf.yaml
