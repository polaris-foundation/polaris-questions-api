#!/usr/bin/env bash
SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=dhos-questions-api
export DATABASE_PASSWORD=dhos-questions-api
export DATABASE_NAME=dhos-questions-api
export FLASK_APP=dhos_questions_api/autoapp.py
export ENVIRONMENT=DEVELOPMENT
export ALLOW_DROP_DATA=true
export IGNORE_JWT_VALIDATION=true
export AUTH0_AUDIENCE=https://dev.sensynehealth.com/
export PROXY_URL=http://localhost
export REDIS_INSTALLED=False
export LOG_LEVEL=${LOG_LEVEL:-DEBUG}
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}

if [ -z "$*" ]
then
  flask db upgrade
  python -m dhos_questions_api
else
  flask $*
fi
