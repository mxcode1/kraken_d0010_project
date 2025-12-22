#!/bin/bash

# ============================================================================
# KRAKEN D0010 - PYTHON ENVIRONMENT SETUP
# ============================================================================
# Creates Python virtual environment and installs dependencies
# Usage: bash setup_python_environment.sh
# ============================================================================

set -e

# Source common utilities
source "$(dirname "$0")/common.sh"

echo -e "${CYAN}"
echo "============================================================================"
echo "  KRAKEN D0010 - PYTHON ENVIRONMENT SETUP"
echo "============================================================================"
echo -e "${NC}"

# Check if we're in the Django project directory
if [[ ! -f "manage.py" ]]; then
    echo -e "${RED}[ERROR] Not in Django project directory. Please run from kraken_d0010_project/${NC}"
    exit 1
fi

# Check Python version
check_python() {
    echo -e "${YELLOW}[CHECK] Python installation...${NC}"
    
    local python_cmd=""
    if command -v python3.11 &> /dev/null; then
        python_cmd="python3.11"
    elif command -v python3 &> /dev/null; then
        python_cmd="python3"
    else
        echo -e "${RED}[ERROR] Python 3 not found. Please install Python 3.10+${NC}"
        exit 1
    fi
    
    local python_version=$($python_cmd --version 2>&1 | awk '{print $2}')
    echo -e "${GREEN}[OK] Python version: $python_version${NC}"
    
    # Check if version is 3.10+
    if $python_cmd -c 'import sys; exit(0 if sys.version_info >= (3, 10) else 1)'; then
        echo -e "${GREEN}[OK] Python version compatible${NC}"
    else
        echo -e "${RED}[ERROR] Python 3.10+ required${NC}"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    echo -e "${YELLOW}[CREATE] Virtual environment...${NC}"
    
    if [[ -d "venv" ]]; then
        echo -e "${YELLOW}[WARNING] Virtual environment exists, removing...${NC}"
        rm -rf venv
    fi
    
    python3 -m venv venv
    echo -e "${GREEN}[OK] Virtual environment created${NC}"
}

# Install dependencies
install_dependencies() {
    echo -e "${YELLOW}[INSTALL] Python dependencies...${NC}"
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Upgrade pip
    pip install --upgrade pip
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        pip install -r requirements.txt
        echo -e "${GREEN}[OK] Dependencies installed from requirements.txt${NC}"
    else
        echo -e "${RED}[ERROR] requirements.txt not found${NC}"
        exit 1
    fi
}

# Validate installation
validate_installation() {
    echo -e "${YELLOW}[VALIDATE] Python environment...${NC}"
    
    source venv/bin/activate
    
    # Test Django import
    python -c "import django; print(f'Django version: {django.get_version()}')" || {
        echo -e "${RED}[ERROR] Django import failed${NC}"
        exit 1
    }
    
    # Test psycopg2 import
    python -c "import psycopg2; print('PostgreSQL adapter available')" || {
        echo -e "${YELLOW}[WARNING] PostgreSQL adapter (psycopg2) not available${NC}"
    }
    
    echo -e "${GREEN}[OK] Python environment validation complete${NC}"
}

# Main execution
main() {
    check_python
    create_venv
    install_dependencies
    validate_installation
    
    echo ""
    echo -e "${GREEN}[COMPLETE] Python environment setup complete${NC}"
    echo ""
    echo -e "${CYAN}Environment ready:${NC}"
    echo -e "   Virtual environment: ${YELLOW}venv/${NC}"
    echo -e "   Django installed and tested"
    echo -e "   PostgreSQL adapter available"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "   1. Activate: ${GREEN}source venv/bin/activate${NC}"
    echo -e "   2. Setup databases: ${GREEN}../deployment_scripts/setup_databases.sh${NC}"
}

# Run main function
main "$@"