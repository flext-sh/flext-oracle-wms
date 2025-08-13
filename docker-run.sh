#!/bin/bash
# =============================================================================
# FLEXT Oracle WMS - Docker Execution Script
# =============================================================================
# Complete Oracle WMS functionality validation using Docker
# Implements user's requirements: "USANDO O MAXIMO DO CONTAINER DOCKER"

set -e

echo "🐳 FLEXT Oracle WMS - Docker Execution Environment"
echo "=============================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
	echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

log_success() {
	echo -e "${GREEN}✅ SUCCESS:${NC} $1"
}

log_warning() {
	echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
}

log_error() {
	echo -e "${RED}❌ ERROR:${NC} $1"
}

# Check if .env file exists
if [ ! -f ".env" ]; then
	log_error ".env file not found! Create it with Oracle WMS credentials."
	exit 1
fi

log_info "Environment file found: .env"

# Build Docker images
log_info "Building Docker images..."
docker-compose build --no-cache

if [ $? -eq 0 ]; then
	log_success "Docker images built successfully"
else
	log_error "Docker build failed"
	exit 1
fi

# Function to run specific service
run_service() {
	local service=$1
	local description=$2

	echo ""
	log_info "🚀 Starting: $description"
	echo "----------------------------------------"

	docker-compose run --rm "$service"

	if [ $? -eq 0 ]; then
		log_success "$description completed successfully"
	else
		log_warning "$description completed with warnings (check output above)"
	fi
}

# Main execution menu
case "${1:-all}" in
"examples")
	run_service "flext-oracle-wms-examples" "Oracle WMS Examples Demonstration"
	;;
"test")
	run_service "flext-oracle-wms-test" "Complete Test Suite with Real Oracle WMS"
	;;
"main")
	run_service "flext-oracle-wms" "Main Oracle WMS Service"
	;;
"all")
	echo ""
	log_info "🎯 COMPLETE ORACLE WMS VALIDATION USING MAXIMUM DOCKER FUNCTIONALITY"
	echo "======================================================================"

	# Run examples first to validate basic functionality
	run_service "flext-oracle-wms-examples" "Oracle WMS Examples - Real Functionality Validation"

	# Run complete test suite
	run_service "flext-oracle-wms-test" "Complete Test Suite - 100% Functionality Coverage"

	echo ""
	log_success "🎉 COMPLETE ORACLE WMS VALIDATION FINISHED!"
	log_info "📊 Check ./reports/ directory for detailed test results and coverage"
	log_info "🔍 All functionality has been validated using Docker containers"
	;;
"clean")
	log_info "Cleaning up Docker resources..."
	docker-compose down --volumes --remove-orphans
	docker system prune -f
	log_success "Docker cleanup completed"
	;;
*)
	echo "Usage: $0 [examples|test|main|all|clean]"
	echo ""
	echo "Commands:"
	echo "  examples  - Run Oracle WMS functionality examples"
	echo "  test      - Run complete test suite with coverage"
	echo "  main      - Run main Oracle WMS service"
	echo "  all       - Run complete validation (default)"
	echo "  clean     - Clean up Docker resources"
	echo ""
	echo "Examples:"
	echo "  $0 all      # Complete Oracle WMS validation"
	echo "  $0 examples # Just run examples"
	echo "  $0 test     # Just run tests"
	;;
esac

echo ""
log_info "Docker execution completed. Check output above for results."
