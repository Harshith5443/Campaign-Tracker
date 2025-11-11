# This file is used by PythonAnywhere to run your Flask app
# It acts as the entry point for the web server

import os
import sys

# Add your project directory to the Python path so imports work
path = os.path.expanduser('~/mysite')
if path not in sys.path:
    sys.path.append(path)

# Import your Flask app
from app_sqlite import app as application

# Set Flask configuration
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'development-secret-key-change-in-production')

# Ensure the database directory exists and is writable
db_dir = os.path.expanduser('~/mysite')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

# Optional: Initialize database on first run
try:
    from app_sqlite import init_db
    init_db()
except Exception as e:
    print(f"Database initialization message: {e}")

if __name__ == '__main__':
    application.run()
