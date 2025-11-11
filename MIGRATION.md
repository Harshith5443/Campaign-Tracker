# SQLite Database Migration Guide

## Overview
The app has been converted from JSON file storage to SQLite database using Flask-SQLAlchemy.

## Files

- **`app_sqlite.py`** - New SQLite-based Flask app (replaces `app.py`)
- **`campaigns.db`** - SQLite database file (auto-created on first run)
- **`requirements.txt`** - Updated with `flask-sqlalchemy>=3.0`

## Quick Start (SQLite Version)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the App
```bash
python app_sqlite.py
```

On first run, the app will:
- Create the SQLite database (`campaigns.db`)
- Initialize the schema (User and Campaign tables)
- Create the default user: `admin` / `1234`

### 3. Access the App
Open your browser and visit:
```
http://127.0.0.1:5000
```

Login with:
- Username: `admin`
- Password: `1234`

## Database Features

- **User Table**: Stores login credentials
- **Campaign Table**: Stores all campaign data with fields:
  - `id` (auto-increment primary key)
  - `name` (string, required)
  - `client` (string, required)
  - `startDate` (string, required)
  - `status` (string: Active/Paused/Completed)
  - `created_at` (timestamp, auto-filled)

## Migration from JSON

If you have existing campaigns in `campaigns.json`, you can migrate them to the database:

```python
import json
from app_sqlite import app, db, Campaign

with app.app_context():
    with open('campaigns.json', 'r') as f:
        campaigns = json.load(f)
    
    for c in campaigns:
        campaign = Campaign(
            name=c['name'],
            client=c['client'],
            startDate=c['startDate'],
            status=c['status']
        )
        db.session.add(campaign)
    
    db.session.commit()
    print(f"✓ Migrated {len(campaigns)} campaigns to SQLite")
```

Run this script (after installing dependencies):
```bash
python migrate_json_to_sqlite.py
```

## Environment Variables (Production)

For production deployment, set these environment variables:

```bash
export DATABASE_URL="sqlite:///campaigns.db"  # or use PostgreSQL, MySQL, etc.
export SECRET_KEY="your-strong-random-secret-here"
export FLASK_ENV="production"
```

Example for Render.com, Heroku, or other platforms—set these in the dashboard environment variables section.

## Switching Between Versions

- **Local development with JSON**: Use original `app.py`
- **With SQLite (recommended)**: Use `app_sqlite.py`

To use SQLite permanently:
```bash
mv app.py app_json_backup.py
mv app_sqlite.py app.py
```

## Troubleshooting

**Q: Database locked error?**
- Ensure only one instance of the app is running.
- Delete `campaigns.db` if corrupted and restart (recreates fresh schema).

**Q: Default user not created?**
- Run: `python -c "from app_sqlite import init_db; init_db()"`

**Q: Want to reset the database?**
```bash
rm campaigns.db
python app_sqlite.py
```

## Next Steps

1. Test the app with SQLite locally
2. Migrate existing campaigns (if any) from `campaigns.json`
3. Deploy to Render/Heroku/VPS (set `DATABASE_URL` and `SECRET_KEY` env vars)
4. For larger deployments, consider PostgreSQL or MySQL
