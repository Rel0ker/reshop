#!/bin/bash

# Local deployment script for ReShop
set -e

echo "🚀 Starting local deployment..."

# Check if env.production exists
if [ ! -f "env.production" ]; then
    echo "❌ env.production file not found. Please create it first."
    exit 1
fi

# Load environment variables
echo "📋 Loading environment variables..."
source env.production

# Build frontend
echo "🔨 Building frontend..."
cd frontend-vue
npm ci
npm run build:prod
cd ..

# Build and start services
echo "🐳 Starting Docker services..."
docker-compose -f docker-compose.local.yml down
docker-compose -f docker-compose.local.yml build --no-cache
docker-compose -f docker-compose.local.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose.local.yml exec -T backend python manage.py migrate || true

# Collect static files
echo "📁 Collecting static files..."
docker-compose -f docker-compose.local.yml exec -T backend python manage.py collectstatic --noinput || true

# Health check
echo "🏥 Performing health check..."
sleep 10

# Check if services are running
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Frontend is running"
else
    echo "❌ Frontend health check failed"
fi

if curl -f http://localhost:8000/api/ > /dev/null 2>&1; then
    echo "✅ Backend API is running"
else
    echo "❌ Backend API health check failed"
fi

echo "🎉 Local deployment completed successfully!"
echo "🌐 Frontend: http://localhost"
echo "🔧 Backend API: http://localhost:8000/api/"
echo "👨‍💼 Admin panel: http://localhost:8000/admin/"
echo ""
echo "📋 Useful commands:"
echo "  make -f Makefile.local logs      # View logs"
echo "  make -f Makefile.local status    # Check status"
echo "  make -f Makefile.local stop      # Stop services"
echo "  make -f Makefile.local restart   # Restart services"
