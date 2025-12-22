#!/bin/bash

# ============================================================================
# KRAKEN D0010 - DATABASE SETUP
# ============================================================================
# Sets up SQLite3 and/or PostgreSQL databases based on configuration
# Usage: bash setup_databases.sh [--sqlite-only|--with-postgresql|--postgresql-primary]
# ============================================================================

set -e

# Source common utilities
source "$(dirname "$0")/common.sh"

# Default configuration
DATABASE_CONFIG="both"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --sqlite-only)
            DATABASE_CONFIG="sqlite"
            shift
            ;;
        --with-postgresql)
            DATABASE_CONFIG="both"
            shift
            ;;
        --postgresql-primary)
            DATABASE_CONFIG="postgresql-primary"
            shift
            ;;
        --help)
            echo "Usage: $0 [--sqlite-only|--with-postgresql|--postgresql-primary]"
            echo ""
            echo "Database Configurations:"
            echo "  --sqlite-only          Setup SQLite3 database only"
            echo "  --with-postgresql      Setup both SQLite3 and PostgreSQL"
            echo "  --postgresql-primary   Setup PostgreSQL as primary database"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${CYAN}"
echo "============================================================================"
echo "  KRAKEN D0010 - DATABASE SETUP ($DATABASE_CONFIG)"
echo "============================================================================"
echo -e "${NC}"

# Check if we're in the right directory
if [[ ! -f "manage.py" ]]; then
    echo -e "${RED}[ERROR] Not in Django project directory. Please run from kraken_d0010_project/${NC}"
    exit 1
fi

# Activate virtual environment
if [[ ! -d "venv" ]]; then
    echo -e "${RED}[ERROR] Virtual environment not found. Please run setup_python_environment.sh first${NC}"
    exit 1
fi

source venv/bin/activate

# Setup PostgreSQL database and user
setup_postgresql_database() {
    echo -e "${YELLOW}[SETUP] PostgreSQL database...${NC}"
    
    # Check if PostgreSQL is running
    if ! pgrep -x "postgres" > /dev/null; then
        echo -e "${YELLOW}[START] PostgreSQL service...${NC}"
        if command -v brew &> /dev/null; then
            brew services start postgresql@15 || brew services start postgresql
        else
            sudo systemctl start postgresql || true
        fi
        
        # Wait a moment for PostgreSQL to start
        sleep 3
    fi
    
    # Create database
    echo -e "${YELLOW}[CREATE] kraken_d0010 database...${NC}"
    createdb kraken_d0010 2>/dev/null || echo "Database may already exist"
    
    # Create user
    echo -e "${YELLOW}[CREATE] kraken_user...${NC}"
    psql -c "CREATE USER kraken_user WITH PASSWORD 'kraken_dev_pass';" 2>/dev/null || echo "User may already exist"
    
    # Grant permissions
    echo -e "${YELLOW}[GRANT] Permissions...${NC}"
    psql -c "GRANT ALL PRIVILEGES ON DATABASE kraken_d0010 TO kraken_user;" 2>/dev/null || true
    psql kraken_d0010 -c "GRANT ALL ON SCHEMA public TO kraken_user;" 2>/dev/null || true
    psql kraken_d0010 -c "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO kraken_user;" 2>/dev/null || true
    
    # Test connection
    echo -e "${YELLOW}[TEST] PostgreSQL connection...${NC}"
    if USE_POSTGRESQL=1 python manage.py check --database=default &>/dev/null; then
        echo -e "${GREEN}[OK] PostgreSQL database ready${NC}"
    else
        echo -e "${RED}[ERROR] PostgreSQL connection failed${NC}"
        exit 1
    fi
}

# Setup SQLite3 database
setup_sqlite_database() {
    echo -e "${YELLOW}[SETUP] SQLite3 database...${NC}"
    
    # Remove existing database if present
    if [[ -f "db.sqlite3" ]]; then
        echo -e "${YELLOW}[WARNING] Removing existing SQLite3 database...${NC}"
        rm -f db.sqlite3
    fi
    
    # Run migrations
    python manage.py makemigrations
    python manage.py migrate
    
    # Test database
    if python manage.py check --database=default &>/dev/null; then
        echo -e "${GREEN}[OK] SQLite3 database ready${NC}"
    else
        echo -e "${RED}[ERROR] SQLite3 setup failed${NC}"
        exit 1
    fi
}

# Setup databases based on configuration
setup_databases() {
    case $DATABASE_CONFIG in
        sqlite)
            setup_sqlite_database
            ;;
        both)
            setup_postgresql_database
            setup_sqlite_database
            # Run PostgreSQL migrations
            USE_POSTGRESQL=1 python manage.py migrate
            ;;
        postgresql-primary)
            setup_postgresql_database
            # Set PostgreSQL as default and run migrations
            export USE_POSTGRESQL=1
            python manage.py makemigrations
            python manage.py migrate
            ;;
        *)
            echo -e "${RED}[ERROR] Invalid database configuration: $DATABASE_CONFIG${NC}"
            exit 1
            ;;
    esac
}

# Display database status
display_status() {
    echo ""
    echo -e "${CYAN}Database Status:${NC}"
    
    if [[ "$DATABASE_CONFIG" != "postgresql-primary" ]]; then
        echo -e "${YELLOW}SQLite3:${NC}"
        local sqlite_check=$(python manage.py check --database=default 2>/dev/null && echo "[OK] Ready" || echo "[FAIL] Failed")
        echo -e "   Status: $sqlite_check"
        if [[ "$sqlite_check" == "[OK] Ready" ]]; then
            echo -e "   Location: $(pwd)/db.sqlite3"
        fi
    fi
    
    if [[ "$DATABASE_CONFIG" == "both" || "$DATABASE_CONFIG" == "postgresql-primary" ]]; then
        echo -e "${YELLOW}PostgreSQL:${NC}"
        local pg_check=$(USE_POSTGRESQL=1 python manage.py check --database=default 2>/dev/null && echo "[OK] Ready" || echo "[FAIL] Failed")
        echo -e "   Status: $pg_check"
        if [[ "$pg_check" == "[OK] Ready" ]]; then
            echo -e "   Database: kraken_d0010"
            echo -e "   User: kraken_user"
            echo -e "   Host: localhost:5432"
        fi
    fi
}

# Main execution
main() {
    setup_databases
    display_status
    
    echo ""
    echo -e "${GREEN}[COMPLETE] Database setup complete${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo -e "   1. Create admin user: ${GREEN}python manage.py createsuperuser${NC}"
    echo -e "   2. Import sample data: ${GREEN}../deployment_scripts/import_sample_data.sh${NC}"
    
    if [[ "$DATABASE_CONFIG" == "both" ]]; then
        echo ""
        echo -e "${CYAN}[NOTE] Dual Database Usage:${NC}"
        echo -e "   SQLite3: ${GREEN}python manage.py runserver${NC}"
        echo -e "   PostgreSQL: ${GREEN}USE_POSTGRESQL=1 python manage.py runserver 8001${NC}"
    fi
}

# Run main function
main "$@"