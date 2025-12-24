"""
Django settings for config.

Environment Variables Required:
- SECRET_KEY (production only)
- DB_PASSWORD (if USE_POSTGRESQL=true)

Optional Environment Variables:
- DEBUG (default: False)
- USE_POSTGRESQL (default: False)
- ALLOWED_HOSTS (comma-separated)

NOTE: The meter_readings app is mounted at both root (/) and /meter_readings/
for backward compatibility. This causes a URL namespace warning which is
intentional and can be safely ignored.
"""

import os
from pathlib import Path

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# Secret key - MUST be set via environment in production
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    if os.environ.get("DJANGO_ENV") == "production":
        raise ValueError("SECRET_KEY must be set in production")
    # Development fallback
    SECRET_KEY = "dev-only-insecure-key-" + str(BASE_DIR)

# Debug mode - defaults to True for development
DEBUG = os.environ.get("DEBUG", "True").lower() == "true"

# Allowed hosts
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0").split(
    ","
)
if DEBUG:
    ALLOWED_HOSTS.append("*")

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"

# SSL/HTTPS (production only)
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Session security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Allow "remember me"

# CSRF security
CSRF_COOKIE_HTTPONLY = False  # JavaScript needs to read this
CSRF_COOKIE_SAMESITE = "Lax"
CSRF_USE_SESSIONS = False

# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",  # Number formatting
    # Third-party apps
    "rest_framework",
    "django_filters",
    "drf_spectacular",
    "corsheaders",
    # Local apps
    "meter_readings",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # CORS support (must be early)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "postgresql": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "kraken_d0010"),
        "USER": os.environ.get("DB_USER", "kraken_user"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),  # Required if USE_POSTGRESQL
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "CONN_MAX_AGE": 600,  # Connection pooling (10 minutes)
        "OPTIONS": {"options": "-c default_transaction_isolation=read committed"},
        "TEST": {
            "NAME": "test_kraken_d0010",
        },
    },
}

# Switch to PostgreSQL if environment variable set
if os.environ.get("USE_POSTGRESQL", "false").lower() == "true":
    if not os.environ.get("DB_PASSWORD"):
        raise ValueError("DB_PASSWORD must be set when USE_POSTGRESQL=true")
    DATABASES["default"] = DATABASES["postgresql"].copy()

# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-gb"  # British English
TIME_ZONE = "Europe/London"  # Kraken Energy headquarters timezone
USE_I18N = True
USE_TZ = True  # Store all datetimes as UTC

# ==============================================================================
# STATIC FILES
# ==============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# Production static file handling
if not DEBUG:
    STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    )

# ==============================================================================
# DEFAULT PRIMARY KEY FIELD TYPE
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# REST FRAMEWORK CONFIGURATION
# ==============================================================================

REST_FRAMEWORK = {
    # Authentication
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",  # Admin/browser
        "rest_framework.authentication.BasicAuthentication",  # Simple auth
    ],
    # Permissions
    "DEFAULT_PERMISSION_CLASSES": [
        # Read public, write auth
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    # Pagination
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 100,  # Default page size
    # Filtering
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # Response rendering
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",  # Dev only
    ],
    # Schema generation
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # Rate limiting
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",  # Anonymous users
        "user": "1000/hour",  # Authenticated users
    },
}

# ==============================================================================
# API DOCUMENTATION (Swagger/OpenAPI)
# ==============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Kraken D0010 Meter Readings API",
    "DESCRIPTION": "REST API for accessing D0010 meter reading data",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": "/api/v1",
}

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================

# CORS - Allow frontend apps to access API
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True  # Development only
else:
    CORS_ALLOWED_ORIGINS = os.environ.get(
        "CORS_ALLOWED_ORIGINS", "https://kraken.tech,https://app.kraken.tech"
    ).split(",")

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

# Ensure logs directory exists
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "[{levelname}] {asctime} {name} "
                "{module}.{funcName}:{lineno} - {message}"
            ),
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose" if DEBUG else "simple",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "django.log",
            "maxBytes": 10 * 1024 * 1024,  # 10 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "import_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOGS_DIR / "imports.log",
            "maxBytes": 50 * 1024 * 1024,  # 50 MB (imports can be verbose)
            "backupCount": 10,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "meter_readings": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "meter_readings.management.commands.import_d0010": {
            "handlers": ["console", "import_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
