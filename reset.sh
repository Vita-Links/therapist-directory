#!/bin/bash

echo "🛑 Stopping only therapist directory containers..."
docker compose -f docker-compose.therapist.yml down

echo "🧹 Pruning only unused Docker data (will not touch Nath's volumes or containers)..."
docker system prune -af --volumes

echo "🚧 Rebuilding therapist containers with no cache..."
docker compose -f docker-compose.therapist.yml build --no-cache

echo "🚀 Starting therapist directory stack..."
docker compose -f docker-compose.therapist.yml up -d

echo "🌐 Restarting Cloudflare tunnel for therapist-directory..."
pkill cloudflared
nohup cloudflared tunnel run therapist-directory > cloudflared.log 2>&1 &
echo "✅ Cloudflare tunnel restarted and logging to cloudflared.log"
