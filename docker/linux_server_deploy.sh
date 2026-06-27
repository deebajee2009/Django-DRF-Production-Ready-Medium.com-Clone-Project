#!/bin/bash

set -Eeuo pipefail


if [ -z "$REMOTE_SERVER_IP_ADDRESS" ]
then
    echo "IP_ADDRESS of linux not difined"
    exit 1
fi

git archive --format tar --output ./project.tar main

echo 'Uploading project ..... :-)'
rsync ./project.tar deploy@"$REMOTE_SERVER_IP_ADDRESS":/tmp/project.tar
echo 'Upload complete...:-)'

echo 'Building then image ...'

ssh -o StrictHostKeyChecking=no deploy@"$REMOTE_SERVER_IP_ADDRESS" << 'ENDSSH'
    mkdir -p /app
    rm -rf /app/* && tar -xf /tmp/project.tar -C /app
    docker compose -f /app/production.yml up --build -d --remove-orphan
ENDSSH

echo 'Build completed successfully ...:-)'