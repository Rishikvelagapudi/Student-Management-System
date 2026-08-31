"""
NRIIT Student Management System - Project Configuration Module
"""

import os
from pathlib import Path

# Base Directory
BASE_DIR = Path(__file__).resolve().parent

# General Application Settings
APP_NAME = "NRIIT Student Management System"
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-nriit-lms-key-for-development')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '127.0.0.1')
ALLOWED_HOSTS = ['*']

# Database Configuration (SQLite3)
DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = 'database.db'
DATABASE_PATH = BASE_DIR / DATABASE_NAME

# Paths & Directories
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
