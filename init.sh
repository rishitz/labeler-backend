#!/bin/bash
set -eu -o pipefail
export APP_PORT=${APP_PORT:=8000}
case $1 in
  app)

    python manage.py collectstatic --no-input

    daphne -b 0.0.0.0 -p ${APP_PORT} labeler.asgi:application
    ;;
  *)
    # The command is something like bash, not an script subcommand. Just run it in the right environment.
    exec "$@"
    ;;
esac
