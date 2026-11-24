"""
settings.py - Cấu hình chính cho dự án Django Cửa Hàng Gấu Bông
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-gaubong-teddy-shop-secret-key-2026-thawngs'

DEBUG = True

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://192.168.*',
    'https://*.onrender.com',
    'https://*.pythonanywhere.com',
    'https://*.trycloudflare.com',
    'https://*.lhr.life',
    'https://*.pinggy.link',
    'https://*.loca.lt',
    'https://*.ngrok-free.app',
]

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'django.contrib.messages',
    'django.contrib.sessions',
    'widget_tweaks',
    'shop',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'gaubong.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart_count',
            ],
        },
    },
]

WSGI_APPLICATION = 'gaubong.wsgi.application'

# ============================================================
# CẤU HÌNH DATABASE: TỰ ĐỘNG CHỌN SQL SERVER HOẶC SQLITE
# ============================================================
# Mặc định dùng SQLite (chuẩn cho Cloud / Render / 24/7 không cần máy ảo)
USE_SQLITE = os.environ.get('USE_SQLITE', '1') == '1'

if USE_SQLITE or os.environ.get('RENDER'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'mssql',
            'NAME': 'QLBanGauBong',
            'HOST': r'.\SQLEXPRESS',
            'PORT': '',
            'USER': '',
            'PASSWORD': '',
            'OPTIONS': {
                'driver': 'ODBC Driver 17 for SQL Server',
                'trusted_connection': 'yes',
                'TrustServerCertificate': 'yes',
            },
        }
    }

# Session
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400  # 1 ngày

LANGUAGE_CODE = 'vi'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = False

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Messages
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
