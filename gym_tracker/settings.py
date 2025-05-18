import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ========== الأمان ==========
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-...')

DEBUG = os.environ.get('DEBUG') == 'True'

ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME'), '127.0.0.1']
if DEBUG:
    ALLOWED_HOSTS.append('*')


# ========== التطبيقات ==========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'workout_app',
]


# ========== البرامج الوسيطة ==========
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ========== الروابط و WSGI ==========
ROOT_URLCONF = 'gym_tracker.urls'
WSGI_APPLICATION = 'gym_tracker.wsgi.application'


# ========== القوالب ==========
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ========== قواعد البيانات ==========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('RENDER_DB_NAME'),
        'USER': os.environ.get('RENDER_DB_USER'),
        'PASSWORD': os.environ.get('RENDER_DB_PASSWORD'),
        'HOST': os.environ.get('RENDER_DB_HOST'),
        'PORT': os.environ.get('RENDER_DB_PORT', 5432),
    }
}


# ========== مدققات كلمة المرور ==========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ========== التدويل ==========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ========== الملفات الثابتة ==========
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'workout_app/static')]


# ========== ملفات الوسائط ==========
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ========== الحقل الافتراضي ==========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ========== التسجيل (Logging) ==========
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',  # أو 'INFO' أو 'WARNING' إلخ.
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'workout_app': {  # اسم التطبيق بتاعك
            'handlers': ['console'],
            'level': 'DEBUG',  # أو 'INFO' أو 'WARNING'
            'propagate': True,
        },
    },
}
