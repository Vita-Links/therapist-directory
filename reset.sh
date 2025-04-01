#!/bin/bash

echo "🛑 Stopping all containers..."
docker-compose down

echo "🧹 Pruning Docker system (containers, images, volumes)..."
docker system prune -af --volumes

echo "🗑️ Removing dangling volumes..."
docker volume prune -f

echo "🚧 Rebuilding containers with no cache..."
docker-compose build --no-cache

echo "🚀 Starting all services..."
docker-compose up -d

echo "✅ All services rebuilt and restarted!"
