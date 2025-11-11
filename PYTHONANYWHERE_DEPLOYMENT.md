# Deploying Campaign Tracker on PythonAnywhere

## Overview

PythonAnywhere is a Python-hosting platform that makes it easy to deploy Flask apps. This guide walks through deploying your Campaign Tracker with SQLite to PythonAnywhere.

---

## ✅ Prerequisites

1. **PythonAnywhere Account** — Free account at https://www.pythonanywhere.com/
2. **Your Project Files** — Ready to upload (all files from `Ginder_media/`)
3. **GitHub Account (Optional)** — To clone repo instead of manual upload

---

## 📋 Step-by-Step Deployment Guide

### Step 1: Create PythonAnywhere Account & Web App

1. Go to https://www.pythonanywhere.com/ and sign up (free account is fine)
2. Log in to your dashboard
3. Click **"Web"** in the top menu
4. Click **"Add a new web app"**
5. Choose your domain name (e.g., `yourusername.pythonanywhere.com`)
6. Select **"Flask"** as the framework
7. Select **Python 3.10** (or latest available)
8. Click through to create the web app

PythonAnywhere will create a default Flask app with directory:
```
/home/yourusername/mysite/
```

---

### Step 2: Upload Your Project Files

#### Option A: Clone from GitHub (Recommended)

1. Go to **"Consoles"** → **"Bash"** (or open a terminal in Files)
2. Run:
```bash
cd ~
git clone https://github.com/YOUR_USERNAME/ginder_media.git
```

3. Rename if needed:
```bash
mv ginder_media mysite
```

#### Option B: Manual File Upload

1. Go to **"Files"** in PythonAnywhere dashboard
2. Create folder: `/home/yourusername/mysite/`
3. Upload all files:
   - `app_sqlite.py`
   - `gin.html`
   - `requirements.txt`
   - `migrate_json_to_sqlite.py`

---

### Step 3: Install Dependencies

1. Go to **"Consoles"** → **"Bash"**
2. Navigate to your project:
```bash
cd ~/mysite
```

3. Create a virtual environment:
```bash
mkvirtualenv --python=/usr/bin/python3.10 mysite
```

4. Install requirements:
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed Flask flask-cors flask-sqlalchemy
```

---

### Step 4: Create WSGI Configuration File

PythonAnywhere uses a WSGI file to run your Flask app.

1. Go to **"Files"** → Navigate to `/home/yourusername/mysite/`
2. Create a new file: `flask_app.py` (exact name for PythonAnywhere)

3. Paste this content:

```python
# PythonAnywhere WSGI Configuration
import os
import sys

# Add your project directory to Python path
path = os.path.expanduser('~/mysite')
if path not in sys.path:
    sys.path.append(path)

# Set Flask app
from app_sqlite import app as application

# Configuration
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# Ensure database directory exists
db_dir = os.path.expanduser('~/mysite')
if not os.path.exists(db_dir):
    os.makedirs(db_dir)

if __name__ == '__main__':
    application.run()
```

Save this file as `flask_app.py` in `/home/yourusername/mysite/`

---

### Step 5: Configure Web App Settings

1. Go to **"Web"** in top menu
2. Click on your web app (e.g., `yourusername.pythonanywhere.com`)
3. Scroll to **"Code"** section
4. Set:
   - **Source code:** `/home/yourusername/mysite`
   - **Working directory:** `/home/yourusername/mysite`
   - **WSGI configuration file:** `/home/yourusername/mysite/flask_app.py`

5. Scroll to **"Virtualenv"** section
6. Set virtualenv path: `/home/yourusername/.virtualenvs/mysite`

7. Click **"Reload yourusername.pythonanywhere.com"** button

---

### Step 6: Initialize Database

1. Go to **"Consoles"** → **"Bash"**
2. Activate your virtual environment:
```bash
workon mysite
```

3. Navigate to project:
```bash
cd ~/mysite
```

4. Initialize database:
```bash
python
```

5. In Python interactive shell:
```python
from app_sqlite import init_db
init_db()
exit()
```

You should see:
```
✓ Default user 'admin' created.
✓ Database initialized.
```

Verify `campaigns.db` was created:
```bash
ls -la campaigns.db
```

---

### Step 7: Update app_sqlite.py for PythonAnywhere

1. Go to **"Files"** → Open `app_sqlite.py`
2. Update the database path to be writable on PythonAnywhere:

Find this line:
```python
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///campaigns.db'
```

Replace with:
```python
import os

# Use absolute path for PythonAnywhere
db_path = os.path.expanduser('~/mysite/campaigns.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
```

Save the file.

---

### Step 8: Configure Static Files (if needed)

PythonAnywhere serves static files separately. Since you're serving HTML from Flask, no additional config is needed.

However, if you want to serve `gin.html` as a static file:

1. Go to **"Web"** → Your web app
2. Scroll to **"Static files"** section
3. Click **"Add a new static files mapping"**
4. Set:
   - **URL:** `/static/`
   - **Directory:** `/home/yourusername/mysite/`

Leave blank for now since Flask serves `gin.html` dynamically.

---

### Step 9: Test Your Deployment

1. Reload the web app: **"Web"** → Click **"Reload yourusername.pythonanywhere.com"**
2. Wait 10 seconds for reload
3. Visit: `https://yourusername.pythonanywhere.com/`
4. You should see the Campaign Tracker login page

---

## 🧪 Testing Your Deployed App

### Test Login
- Username: `admin`
- Password: `1234`
- You should see the dashboard with summary boxes

### Test Add Campaign
- Click form and fill:
  - Campaign Name: `Test Campaign`
  - Client: `Test Client`
  - Start Date: Today's date
  - Status: `Active`
- Click **"Add"**
- Campaign should appear in the table below

### Test Update Status
- In the campaign table, click the status dropdown
- Change from `Active` to `Paused`
- Status should update immediately

### Test Delete Campaign
- Click the red **"Delete"** button
- Campaign should disappear from the table

### Test Persistence
- Reload the page (F5)
- Your campaigns should still be there (stored in SQLite)

---

## 🔐 Security & Environment Variables

### Set Secret Key

1. Generate a strong secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. In PythonAnywhere **"Web"** tab:
   - Scroll to **"Environment variables"** (or use Web app config)
   - Add: `SECRET_KEY = your-generated-secret-here`

3. Reload the web app

### For Production (Important)

Update your WSGI file (`flask_app.py`) to use the environment variable:

```python
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'fallback-key')
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **"ImportError: No module named flask"** | Check virtualenv is set correctly in Web settings |
| **Database locked error** | Only one web worker can access SQLite at a time. PythonAnywhere defaults to this, so should be fine |
| **"campaigns.db" not found** | Run `python -c "from app_sqlite import init_db; init_db()"` in Bash console |
| **Page shows error 500** | Check **"Error log"** in Web tab for details |
| **CORS errors** | Frontend and backend are on same domain, so CORS is not needed; errors should not occur |
| **Blank/white page** | Reload the web app and wait 30 seconds; clear browser cache |

### View Error Logs

1. Go to **"Web"** → Your web app
2. Scroll to **"Log files"**
3. Click **"error log"** to see Flask errors
4. Click **"access log"** to see HTTP requests

---

## 📁 Final File Structure on PythonAnywhere

```
/home/yourusername/mysite/
├── app_sqlite.py              # Main Flask app
├── flask_app.py               # WSGI config for PythonAnywhere
├── gin.html                   # Frontend UI
├── campaigns.db               # SQLite database (auto-created)
├── requirements.txt           # Dependencies
├── migrate_json_to_sqlite.py  # Migration script
├── MIGRATION.md               # Migration guide
├── README.md                  # Setup guide
├── PROJECT_OVERVIEW.md        # Project overview
└── .gitignore                 # Git ignore
```

---

## 🎉 Your App is Live!

Once deployed, your Campaign Tracker is accessible at:
```
https://yourusername.pythonanywhere.com/
```

---

## 🔄 Updating Your App on PythonAnywhere

### If you update code locally:

1. **Using Git:**
```bash
cd ~/mysite
git pull origin main
```

2. **Manual update:**
   - Go to **"Files"** in PythonAnywhere
   - Edit/upload updated files

3. **Reload the web app:**
   - Go to **"Web"** → Click **"Reload yourusername.pythonanywhere.com"**

---

## 📊 Monitoring Your App

1. **Visit "Web" tab** to see:
   - CPU usage
   - Memory usage
   - Request count
   - Last reload time

2. **Check error logs** if users report issues

3. **Scale up** if needed (paid plan required for multiple web workers with SQLite)

---

## 🚀 Next Steps

1. ✅ Deploy to PythonAnywhere
2. ✅ Test all features (login, CRUD, persistence)
3. ⬜ Share link with team/users
4. ⬜ Monitor logs and usage
5. ⬜ (Optional) Switch to PostgreSQL if user base grows

---

## 📞 Need Help?

- **PythonAnywhere Docs:** https://help.pythonanywhere.com/
- **Flask Docs:** https://flask.palletsprojects.com/
- **SQLAlchemy Docs:** https://docs.sqlalchemy.org/

---

**Deployment Date:** November 11, 2025  
**Platform:** PythonAnywhere  
**App Type:** Flask + SQLite  
**Status:** Ready to Deploy
