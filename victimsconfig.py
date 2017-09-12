from os import environ, makedirs
from os.path import isfile, isdir, join
from datetime import timedelta
from imp import load_source
from logging import getLogger, INFO as LOG_LEVEL_INFO

# Base Dir
VICTIMS_BASE_DIR = '/opt/app-root/'

LOGGER = getLogger()
LOG_FOLDER = join(VICTIMS_BASE_DIR, 'logs')
LOG_LEVEL = LOG_LEVEL_INFO

FLASK_HOST = environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(environ.get('FLASK_PORT', 8080))

DEBUG = False
TESTING = False
SECRET_KEY = b'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

# File upload
UPLOAD_FOLDER = join(VICTIMS_BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = set(['egg', 'jar', 'gem'])

# File download
DOWNLOAD_FOLDER = join(VICTIMS_BASE_DIR, "downloads")

CACHE_DIR = join(VICTIMS_BASE_DIR, 'cache')

# MongoDB Configuration
MONGODB_SETTINGS = {
    'DB': environ.get('VICTIMS_DB', 'victims'),
    'HOST': environ.get('MONGODB_DB_HOST', 'mongodb.victims.svc'),
    'PORT': 27017,
    'USERNAME': environ.get('MONGODB_DB_USERNAME', ''),
    'PASSWORD': environ.get('MONGODB_DB_PASSWORD', '')
}

# Hashing commands for each group
# This will be used as command.format(archive=filename)
# Eg: 'java': 'victims-java hash {archive!s}'
HASHING_COMMANDS = {
    'java': VICTIMS_BASE_DIR + 'src/bin/victims-hash-java {archive!s}',
}

PREFERRED_URL_SCHEME = 'https'

