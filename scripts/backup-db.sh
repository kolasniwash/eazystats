#!/bin/bash
set -e
pwd

if [[ -f .env ]]; then
  source .env
else
  echo "Error: .env file not found."
  exit 1
fi

docker exec -i $POSTGRES_CONTAINER_NAME \
 /bin/bash -c \
 "PGPASSWORD=$POSTGRES_PASSWORD pg_dump --username $POSTGRES_USER $POSTGRES_DB" \
 > ./data/backups/eazystats.dump