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

# Paths & Directories
DATABASE_PATH = BASE_DIR / 'database.db'
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
