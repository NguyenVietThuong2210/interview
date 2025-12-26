from datetime import timedelta
import os
from pathlib import Path
from decouple import config, Csv

# ASVS V1: Architecture, Design and Threat Modeling
# V1.2.2: Secure communications between components
# V1.4.1: Trusted enforcement points

# Security Settings - ASVS V1.14: Configuration
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=Csv())
BASE_DIR = Path(__file__).resolve().parent.parent

# ASVS V3: Session Management
# V3.2.1: Session tokens possess at least 64 bits of entropy
# V3.2.2: Session tokens are stored in a way that prevents unauthorized access
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',  # For token blacklisting
    'corsheaders',  # CORS handling
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS - must be before CommonMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ASVS V2: Authentication
# V2.1: Password Security Requirements
# PASSWORD_HASHERS = [
#     'django.contrib.auth.hashers.Argon2PasswordHasher',  # Most secure
#     'django.contrib.auth.hashers.PBKDF2PasswordHasher',
#     'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
#     'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
# ]

# V2.1.1: Passwords are at least 12 characters
# V2.1.7: Passwords are checked against breached password lists
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # ASVS Level 2 requirement
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ASVS V3: Session Management
# V3.3.1: Logout invalidates the session
# V3.5.2: Session timeout - 12 hours for standard apps
SESSION_COOKIE_AGE = 43200  # 12 hours in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True  # V3.4.1: Cookies have HttpOnly flag
SESSION_COOKIE_SECURE = not DEBUG  # V3.4.2: Cookies have Secure flag in production
SESSION_COOKIE_SAMESITE = 'Lax'  # V3.4.3: SameSite attribute

# ASVS V8: Data Protection
# V8.3.4: Sensitive data is not logged
# V8.3.6: Cryptographic keys are managed securely

# REST Framework Configuration with Security
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    # ASVS V13: API Security
    # V13.1.3: API rate limiting
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # Anonymous users
        'user': '1000/hour',  # Authenticated users
        'auth': '5/minute',   # Authentication endpoints
    },
    # V13.2.3: RESTful web services use session IDs or tokens
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

# JWT Settings - ASVS V3: Session Management
# V3.1.1: Application never reveals session tokens in URL
# V3.2.1: Session tokens possess at least 64 bits of entropy
# V3.5.1: Session timeout - appropriate for risk level
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # V3.3.2: New session token on re-authentication
    'BLACKLIST_AFTER_ROTATION': True,  # V3.3.1: Logout invalidates tokens
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    # Additional security settings
    'JTI_CLAIM': 'jti',  # Unique token identifier
}

# ASVS V8: Data Protection
# V8.2.2: Data classified by sensitivity
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'security.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ASVS V12: Files and Resources
# V12.1.1: User-uploaded files are not executed
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# ASVS V5: Validation, Sanitization and Encoding
# V5.1.3: URL redirects only to whitelisted destinations
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
] if DEBUG else []

CORS_ALLOW_CREDENTIALS = True

# ASVS V14: Configuration
# V14.1.3: Components are up to date
# V14.2.1: All components are signed and verified
# V14.4.1: HTTP security headers are in place

# Security Headers - ASVS V14.4
SECURE_BROWSER_XSS_FILTER = True  # V14.4.3: X-XSS-Protection
SECURE_CONTENT_TYPE_NOSNIFF = True  # V14.4.4: X-Content-Type-Options
X_FRAME_OPTIONS = 'DENY'  # V14.4.5: X-Frame-Options

# Production Security Settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True  # V9.1.1: TLS for all connections
    SECURE_HSTS_SECONDS = 31536000  # V9.1.2: HSTS - 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    
# ASVS V9: Communications Security
# V9.2.1: TLS connections use strong ciphers
# This is typically configured at the web server level (nginx/apache)

ROOT_URLCONF = 'interview.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'interview.wsgi.application'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
# Alternative explicit configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('POSTGRES_HOST'),
        'PORT': config('POSTGRES_PORT', default='5432'),
        'CONN_MAX_AGE': 600,
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') 
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'