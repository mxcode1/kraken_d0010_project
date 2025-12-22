#!/bin/bash

# ============================================================================
# KRAKEN ENERGY D0010 - SYSTEM DEPENDENCIES SETUP
# ============================================================================
# Installs system-level dependencies via Homebrew (macOS) or apt-get (Linux)
# Usage: bash setup_system_dependencies.sh
# ============================================================================

set -e

# Source common utilities
source "$(dirname "$0")/common.sh"

echo -e "${CYAN}"
echo "============================================================================"
echo "  KRAKEN D0010 - SYSTEM DEPENDENCIES SETUP"
echo "============================================================================"
echo -e "${NC}"

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        echo -e "${CYAN}[DETECTED] macOS${NC}"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        echo -e "${CYAN}[DETECTED] Linux${NC}"
    else
        echo -e "${RED}[ERROR] Unsupported operating system: $OSTYPE${NC}"
        exit 1
    fi
}

# Install Homebrew on macOS
install_homebrew() {
    echo -e "${YELLOW}[INSTALL] Homebrew...${NC}"
    
    if command -v brew &> /dev/null; then
        echo -e "${GREEN}[OK] Homebrew already installed${NC}"
        return
    fi
    
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon Macs
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
    
    echo -e "${GREEN}[OK] Homebrew installed successfully${NC}"
}

# Install dependencies on macOS
install_macos_dependencies() {
    echo -e "${YELLOW}[INSTALL] macOS dependencies...${NC}"
    
    # Update Homebrew
    brew update
    
    # Install Python
    if ! brew list python@3.11 &> /dev/null; then
        echo -e "${YELLOW}[INSTALL] Python 3.11...${NC}"
        brew install python@3.11
    else
        echo -e "${GREEN}[OK] Python 3.11 already installed${NC}"
    fi
    
    # Install PostgreSQL
    if ! brew list postgresql@15 &> /dev/null; then
        echo -e "${YELLOW}[INSTALL] PostgreSQL 15...${NC}"
        brew install postgresql@15
    else
        echo -e "${GREEN}[OK] PostgreSQL 15 already installed${NC}"
    fi
    
    # Install other utilities
    local packages=("git" "curl" "wget")
    for package in "${packages[@]}"; do
        if ! brew list "$package" &> /dev/null; then
            echo -e "${YELLOW}[INSTALL] $package...${NC}"
            brew install "$package"
        else
            echo -e "${GREEN}[OK] $package already installed${NC}"
        fi
    done
}

# Install dependencies on Linux
install_linux_dependencies() {
    echo -e "${YELLOW}[INSTALL] Linux dependencies...${NC}"
    
    # Update package manager
    sudo apt-get update
    
    # Install Python
    echo -e "${YELLOW}[INSTALL] Python 3.11...${NC}"
    sudo apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
    
    # Install PostgreSQL
    echo -e "${YELLOW}[INSTALL] PostgreSQL...${NC}"
    sudo apt-get install -y postgresql postgresql-contrib postgresql-client libpq-dev
    
    # Install other utilities
    echo -e "${YELLOW}[INSTALL] Utilities...${NC}"
    sudo apt-get install -y git curl wget build-essential
    
    echo -e "${GREEN}[OK] Linux dependencies installed${NC}"
}

# Verify Python installation
verify_python() {
    echo -e "${YELLOW}[VERIFY] Python installation...${NC}"
    
    local python_cmd=""
    if command -v python3.11 &> /dev/null; then
        python_cmd="python3.11"
    elif command -v python3 &> /dev/null; then
        python_cmd="python3"
    else
        echo -e "${RED}[ERROR] Python 3 not found${NC}"
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

# Verify PostgreSQL installation
verify_postgresql() {
    echo -e "${YELLOW}[VERIFY] PostgreSQL installation...${NC}"
    
    if command -v psql &> /dev/null; then
        local pg_version=$(psql --version | awk '{print $3}')
        echo -e "${GREEN}[OK] PostgreSQL version: $pg_version${NC}"
    else
        echo -e "${RED}[ERROR] PostgreSQL not found${NC}"
        exit 1
    fi
    
    # Start PostgreSQL service
    if [[ "$OS" == "macos" ]]; then
        echo -e "${YELLOW}[START] PostgreSQL service...${NC}"
        brew services start postgresql@15 || true
    elif [[ "$OS" == "linux" ]]; then
        echo -e "${YELLOW}[START] PostgreSQL service...${NC}"
        sudo systemctl start postgresql || true
        sudo systemctl enable postgresql || true
    fi
    
    echo -e "${GREEN}[OK] PostgreSQL service started${NC}"
}

# Install from Brewfile if present
install_from_brewfile() {
    if [[ -f "Brewfile" && "$OS" == "macos" ]]; then
        echo -e "${YELLOW}[INSTALL] From Brewfile...${NC}"
        brew bundle install
        echo -e "${GREEN}[OK] Brewfile dependencies installed${NC}"
    elif [[ -f "deployment_scripts/Brewfile" && "$OS" == "macos" ]]; then
        echo -e "${YELLOW}[INSTALL] From deployment_scripts/Brewfile...${NC}"
        cd deployment_scripts && brew bundle install && cd ..
        echo -e "${GREEN}[OK] Brewfile dependencies installed${NC}"
    fi
}

# Main execution
main() {
    echo -e "${CYAN}[SETUP] System dependencies for Kraken D0010...${NC}"
    echo ""
    
    detect_os
    
    if [[ "$OS" == "macos" ]]; then
        install_homebrew
        install_from_brewfile
        install_macos_dependencies
    elif [[ "$OS" == "linux" ]]; then
        install_linux_dependencies
    fi
    
    verify_python
    verify_postgresql
    
    echo ""
    echo -e "${GREEN}[COMPLETE] System dependencies setup complete${NC}"
    echo ""
    echo -e "${CYAN}Installed components:${NC}"
    echo -e "   [*] Python 3.11+ with pip and venv"
    echo -e "   [*] PostgreSQL 15+ with client tools"
    echo -e "   [*] Git version control"
    echo -e "   [*] Essential build tools"
    echo -e "   [*] PostgreSQL service started"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "   1. Run: ${GREEN}./setup_python_environment.sh${NC}"
    echo -e "   2. Run: ${GREEN}./setup_databases.sh${NC}"
    echo ""
}

# Run main function
main "$@"