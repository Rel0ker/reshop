#!/bin/bash

# Quick fix for frontend build issue
echo "🔧 Fixing frontend build issue..."

# Update the frontend Dockerfile
cat > frontend-vue/Dockerfile.production.optimized << 'EOF'
# Build stage
FROM node:18-alpine as build-stage

WORKDIR /app

# Install build dependencies
RUN apk add --no-cache python3 make g++

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies for build)
RUN npm ci

# Copy source code
COPY . .

# Build for production
RUN npm run build:prod

# Production stage
FROM nginx:alpine as production-stage

# Copy built app
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
EOF

echo "✅ Frontend Dockerfile fixed!"

# Update docker-compose to use the fixed Dockerfile
sed -i 's|dockerfile: Dockerfile.production|dockerfile: Dockerfile.production.optimized|' docker-compose.server.yml

echo "✅ Docker-compose updated!"

# Clean up and rebuild
echo "🧹 Cleaning up Docker..."
docker-compose -f docker-compose.server.yml down
docker system prune -f

echo "🔨 Rebuilding frontend..."
docker-compose -f docker-compose.server.yml build --no-cache frontend

echo "🚀 Starting services..."
docker-compose -f docker-compose.server.yml up -d

echo "✅ Frontend build issue fixed!"
echo "🌐 Check status: docker-compose -f docker-compose.server.yml ps"


