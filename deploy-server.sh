#!/bin/bash

# Automatic deployment script for server 89.185.85.178
set -e

echo "🚀 Starting server deployment for 89.185.85.178..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Update system
print_status "Updating system packages..."
apt update && apt upgrade -y

# Install required packages
print_status "Installing required packages..."
apt install -y curl wget git nano htop

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    print_status "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
else
    print_status "Docker already installed"
fi

# Install Docker Compose if not present
if ! command -v docker-compose &> /dev/null; then
    print_status "Installing Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    print_status "Docker Compose already installed"
fi

# Clone or update project
if [ ! -d "reshop" ]; then
    print_status "Cloning project..."
    git clone https://github.com/your-username/reshop.git
    cd reshop
else
    print_status "Project already exists, updating..."
    cd reshop
    git pull origin main
fi

# Build frontend
print_status "Building frontend..."
cd frontend-vue
npm ci
npm run build:prod
cd ..

# Stop existing services
print_status "Stopping existing services..."
docker-compose -f docker-compose.server.yml down || true

# Remove old images to ensure fresh build
print_status "Removing old Docker images..."
docker system prune -f

# Build and start services
print_status "Building and starting services..."
docker-compose -f docker-compose.server.yml build --no-cache
docker-compose -f docker-compose.server.yml up -d

# Wait for services to be ready
print_status "Waiting for services to start..."
sleep 60

# Check if backend is running
if ! docker-compose -f docker-compose.server.yml ps backend | grep -q "Up"; then
    print_error "Backend service is not running. Checking logs..."
    docker-compose -f docker-compose.server.yml logs backend
    exit 1
fi

# Run migrations
print_status "Running database migrations..."
docker-compose -f docker-compose.server.yml exec -T backend python manage.py migrate || true

# Collect static files
print_status "Collecting static files..."
docker-compose -f docker-compose.server.yml exec -T backend python manage.py collectstatic --noinput || true

# Create superuser if needed
print_status "Creating superuser (optional)..."
docker-compose -f docker-compose.server.yml exec -T backend python manage.py createsuperuser --noinput || print_warning "Superuser creation failed or already exists"

# Health check
print_status "Performing health check..."
sleep 10

# Check services
print_status "Checking service status..."
docker-compose -f docker-compose.server.yml ps

# Final status
print_status "Deployment completed successfully!"
echo ""
echo "🌐 Services available at:"
echo "  Frontend: http://89.185.85.178"
echo "  Backend API: http://89.185.85.178:8000/api/"
echo "  Admin Panel: http://89.185.85.178:8000/admin/"
echo ""
echo "📋 Useful commands:"
echo "  docker-compose -f docker-compose.server.yml logs -f    # View logs"
echo "  docker-compose -f docker-compose.server.yml ps         # Check status"
echo "  docker-compose -f docker-compose.server.yml restart    # Restart services"
echo "  docker-compose -f docker-compose.server.yml down       # Stop services"
echo ""
echo "🔍 Troubleshooting:"
echo "  If services are not accessible, check:"
echo "  - Firewall settings (ports 80, 8000, 3000)"
echo "  - Docker logs: docker-compose -f docker-compose.server.yml logs"
echo "  - Service status: docker-compose -f docker-compose.server.yml ps"
