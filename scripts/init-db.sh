#!/bin/bash
set -e

# Import the data dump
psql \
    -v ON_ERROR_STOP=1 \
    --username $POSTGRES_USER \
    --dbname $POSTGRES_DB \
    < /docker-entrypoint-initdb.d/eazystats.dump


# Check if the path is a directory using the -d flag and
#  there are SQL files in the directory using the -f command
#   (the [] brackets are used for conditional expressions)
if [ -d /docker-entrypoint-initdb.d/db ]; then
  echo "[SUCCESS]: Located homework directory"
  # Run any additional initialization scripts
    for f in /docker-entrypoint-initdb.d/db/*.sql; do
      if [ -f "$f" ]; then
        echo "[SUCCESS] Running SQL file: $f"
        psql -U $POSTGRES_USER -d $POSTGRES_DB -f $f
      else
        echo "[INFO] No SQL file found inside the db directory"
      fi
    done
else
    echo "[ERROR] Directory not found: /docker-entrypoint-initdb.d/db/"
fi
