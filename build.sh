#!/bin/bash
# ============================================================================
# build.sh - IRCA Project Build Script
# ============================================================================
# This script builds the Angular frontend and copies it to the backend
# static directory, preparing for Docker image creation.
#
# Usage:
#   ./build.sh
#
# Requirements:
#   - Node.js 18+ and npm
#   - Angular CLI (installed via npm)
#
# Output:
#   - Compiled Angular app in: back/static/
#   - Ready for: docker build -t irca-backend:latest ./back
# ============================================================================

set -e  # Exit immediately if any command fails

# Colors for pretty output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Print banner
echo ""
echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}║  🚀 IRCA Project - Build Script                              ║${NC}"
echo -e "${CYAN}║     Backend + Frontend Unified Build                         ║${NC}"
echo -e "${CYAN}║                                                               ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Step 1: Build Angular Frontend
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📦 Step 1/3: Building Angular frontend...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd front

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}⚠️  node_modules not found. Running npm install...${NC}"
    echo ""
    npm install
    echo ""
fi

# Build for production
echo -e "${BLUE}🔨 Running Angular production build...${NC}"
echo -e "${CYAN}   Using environment.production.ts${NC}"
echo ""

npm run build -- --configuration production

echo ""

# Verify build output
if [ ! -d "dist/coreui-free-angular-admin-template/browser" ]; then
    echo ""
    echo -e "${RED}❌ BUILD FAILED!${NC}"
    echo -e "${RED}   dist/coreui-free-angular-admin-template/browser not found${NC}"
    echo ""
    exit 1
fi

echo -e "${GREEN}✅ Frontend build complete!${NC}"
echo ""

# Show build output size
BUILD_DIR="dist/coreui-free-angular-admin-template/browser"
BUILD_SIZE=$(du -sh "$BUILD_DIR" | cut -f1)
FILE_COUNT=$(find "$BUILD_DIR" -type f | wc -l)
echo -e "${CYAN}   Output: $BUILD_DIR${NC}"
echo -e "${CYAN}   Size: $BUILD_SIZE${NC}"
echo -e "${CYAN}   Files: $FILE_COUNT${NC}"
echo ""

# ============================================================================
# Step 2: Copy Frontend to Backend Static Directory
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📂 Step 2/3: Copying frontend to backend static folder...${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

cd ..

# Remove old static directory
if [ -d "back/static" ]; then
    echo -e "${YELLOW}   Removing old static directory...${NC}"
    rm -rf back/static
fi

# Create static directory
echo -e "${CYAN}   Creating back/static directory...${NC}"
mkdir -p back/static

# Copy frontend build
echo -e "${CYAN}   Copying files...${NC}"
cp -r front/dist/coreui-free-angular-admin-template/browser/* back/static/

# Verify copy
if [ ! -f "back/static/index.html" ]; then
    echo ""
    echo -e "${RED}❌ COPY FAILED!${NC}"
    echo -e "${RED}   index.html not found in back/static/${NC}"
    echo ""
    exit 1
fi

echo ""
echo -e "${GREEN}✅ Frontend copied to back/static/${NC}"
echo ""

# ============================================================================
# Step 3: Show Result & Next Steps
# ============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Step 3/3: Build Summary${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Show files in static directory
echo -e "${CYAN}Files in back/static/:${NC}"
ls -lh back/static/ | head -15
if [ $(ls back/static/ | wc -l) -gt 14 ]; then
    echo -e "${CYAN}   ... ($(ls back/static/ | wc -l) files total)${NC}"
fi
echo ""

# Calculate total size
STATIC_SIZE=$(du -sh back/static/ | cut -f1)
echo -e "${CYAN}Total size: $STATIC_SIZE${NC}"
echo ""

# Success banner
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}║  ✅ BUILD COMPLETE!                                           ║${NC}"
echo -e "${GREEN}║                                                               ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Next steps
echo -e "${YELLOW}📝 Next steps:${NC}"
echo ""
echo -e "${CYAN}  1. Test locally with Docker Compose:${NC}"
echo -e "     ${GREEN}docker-compose up --build${NC}"
echo ""
echo -e "${CYAN}  2. Or build Docker image directly:${NC}"
echo -e "     ${GREEN}docker build -t irca-backend:latest ./back${NC}"
echo ""
echo -e "${CYAN}  3. Run the container:${NC}"
echo -e "     ${GREEN}docker run -p 8000:8000 --network bridge \\${NC}"
echo -e "     ${GREEN}  -e DB_HOST=mysql_local -e DB_USER=root \\${NC}"
echo -e "     ${GREEN}  -e DB_PASSWORD=1234 -e DB_NAME=calidad_agua \\${NC}"
echo -e "     ${GREEN}  irca-backend:latest${NC}"
echo ""
echo -e "${CYAN}  4. Access the application:${NC}"
echo -e "     ${GREEN}http://localhost:8000${NC}          (Frontend - Angular SPA)"
echo -e "     ${GREEN}http://localhost:8000/api${NC}      (API - FastAPI)"
echo -e "     ${GREEN}http://localhost:8000/docs${NC}     (API Docs - Swagger UI)"
echo -e "     ${GREEN}http://localhost:8000/health${NC}   (Health Check)"
echo ""
echo -e "${CYAN}  5. Deploy to Google Cloud Run:${NC}"
echo -e "     ${GREEN}See DEPLOYMENT.md for detailed instructions${NC}"
echo ""

# Final message
echo -e "${BLUE}🎉 Ready to containerize and deploy!${NC}"
echo ""
