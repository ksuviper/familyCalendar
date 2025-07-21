#!/bin/bash
# filepath: update.sh

set -e

echo "Pulling latest source from git..."
git pull

echo "Rebuilding Docker images..."
docker-compose build

echo "Restarting containers..."
docker-compose up -d

echo "Update complete."