# Campaign Tracker – Project Overview

## 📋 Project Description

**Campaign Tracker** is a web-based application for managing marketing campaigns. It allows users to create, view, update, and delete campaigns with real-time status tracking and filtering. The app includes user authentication, a dashboard summary, and persistent storage using SQLite.

---

## 🎯 Key Features

✅ **User Authentication**
- Login/logout with session management
- Demo credentials: `admin` / `1234`
- Server-side session storage

✅ **Campaign Management (CRUD)**
- Add new campaigns with name, client, start date, and status
- View all campaigns in a clean table format
- Update campaign status (Active / Paused / Completed)
- Delete campaigns

✅ **Search & Filter**
- Search campaigns by name or client
- Filter by status (All, Active, Paused, Completed)

✅ **Dashboard Summary**
- Real-time count of total, active, paused, and completed campaigns
- Yellow-highlighted summary boxes for visibility

✅ **Responsive UI**
- Modern, gradient-based design
- Mobile-friendly layout
- Smooth animations and transitions

✅ **Persistent Storage**
- SQLite database for reliable data persistence
- Auto-initialization on first run
- Scalable to PostgreSQL/MySQL for production

---

## 🏗️ Architecture

### Technology Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla) |
| **Backend** | Python 3 + Flask |
| **Database** | SQLite (with Flask-SQLAlchemy ORM) |
| **Server** | Flask dev server (gunicorn for production) |
| **CORS** | flask-cors for cross-origin requests |

### Project Structure

```
Ginder_media/
├── app.py                      # Original JSON-based app (for reference)
├── app_sqlite.py               # Current SQLite-based app (USE THIS)
├── gin.html                    # Frontend UI (HTML/CSS/JS)
├── campaigns.db                # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── README.md                   # Setup and usage guide
├── MIGRATION.md                # SQLite migration guide
├── migrate_json_to_sqlite.py   # Script to import JSON data
├── .gitignore                  # Git ignore rules
├── campaigns.json              # Old JSON data (backup)
├── users.json                  # Old user data (backup)
└── TODO.md                     # Project tasks
```

---

## 📦 Dependencies

```
Flask>=2.0              # Web framework
flask-cors>=3.0         # CORS support for frontend
flask-sqlalchemy>=3.0   # SQLite ORM
```

Optional (for production):
```
gunicorn>=20.0         # Production WSGI server
python-dotenv          # Environment variable management
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Local Setup (Windows CMD)

**Step 1: Navigate to project directory**
```cmd
cd /d "c:\Users\harshith.k\Downloads\Work\Ginder_media"
```

**Step 2: Create virtual environment (optional but recommended)**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Step 3: Install dependencies**
```cmd
pip install -r requirements.txt
```

**Step 4: Run the app**
```cmd
python app_sqlite.py
```

You'll see:
```
✓ Default user 'admin' created.
✓ Database initialized.
 * Running on http://127.0.0.1:5000
```

**Step 5: Open in browser**
```
http://127.0.0.1:5000
```

**Step 6: Login**
- Username: `admin`
- Password: `1234`

---

## 📊 Database Schema

### User Table
```sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
```

### Campaign Table
```sql
CREATE TABLE campaign (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    client VARCHAR(255) NOT NULL,
    startDate VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'Active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔌 REST API Endpoints

All endpoints return JSON. Authentication required for POST/PUT/DELETE operations.

### Authentication
- `POST /api/login` — Login (credentials in JSON body)
- `POST /api/logout` — Logout
- `GET /api/check-login` — Check session status

### Campaigns
- `GET /api/campaigns` — Get all campaigns (supports `?status=` and `?search=` params)
- `POST /api/campaigns` — Create campaign (requires login)
- `PUT /api/campaigns/<id>` — Update campaign (requires login)
- `DELETE /api/campaigns/<id>` — Delete campaign (requires login)

### Dashboard
- `GET /api/summary` — Get campaign counts (total, active, paused, completed)

---

## 🎨 Frontend Features

### Pages
1. **Login Page** — Authentication with demo credentials display
2. **Dashboard** — Main app with summary, search, campaigns table

### UI Components
- **Header** — App title and logout button
- **Dashboard Summary** — Yellow boxes showing counts
- **Search Bar** — Text input with status filter dropdown
- **Add Campaign Form** — Inline form with 4 input fields
- **Campaigns Table** — Sortable columns with inline status editor and delete button

### Styling
- Modern gradient background (indigo → cyan)
- Frosted glass login card
- Responsive flexbox layout
- Smooth fade-in animations

---

## 🔄 Data Flow

```
User Input (Frontend)
    ↓
JavaScript Event Handler
    ↓
Fetch API (HTTP Request)
    ↓
Flask Route (@app.route)
    ↓
Database Query (SQLAlchemy)
    ↓
SQLite Database
    ↓
JSON Response
    ↓
Frontend Updates DOM
    ↓
User sees updated data
```

---

## 🛠️ Common Tasks

### Reset Database
```cmd
del campaigns.db
python app_sqlite.py
```

### Migrate Data from JSON to SQLite
```cmd
python migrate_json_to_sqlite.py
```

### Generate Strong Secret Key (for production)
```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Run with Production Settings
```cmd
set FLASK_ENV=production
set SECRET_KEY=your-generated-key-here
python app_sqlite.py
```

---

## 📈 Deployment

### Option 1: Render.com (Recommended for beginners)
1. Push to GitHub
2. Connect GitHub repo to Render
3. Set environment variables: `SECRET_KEY`, `DATABASE_URL`
4. Deploy

### Option 2: Heroku
1. Add `Procfile`: `web: gunicorn app_sqlite:app`
2. Push to GitHub
3. Connect and deploy with env vars

### Option 3: Docker + VPS
See `Dockerfile` (if created) or use standard Flask deployment guides.

---

## 🔐 Security Considerations

⚠️ **Current Implementation (Development)**
- Hardcoded secret key
- Plain-text password storage
- No HTTPS enforcement
- Open CORS (allows all origins)

✅ **For Production**
- Use environment variables for `SECRET_KEY` and `DATABASE_URL`
- Implement password hashing (bcrypt, werkzeug.security)
- Enable HTTPS/TLS
- Restrict CORS to your frontend domain
- Use strong, randomly generated secrets
- Add rate limiting for login attempts
- Consider OAuth2 or JWT for better auth

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Port 5000 already in use** | Change port in `app_sqlite.py`: `app.run(port=8000)` |
| **Database locked** | Stop other instances; delete `campaigns.db` and restart |
| **ModuleNotFoundError: flask** | Run `pip install -r requirements.txt` in activated venv |
| **CORS errors in browser** | Ensure frontend fetch calls include `credentials: 'include'` |
| **Login fails** | Check that `users` table exists; run init_db manually if needed |

---

## 📚 Next Steps

1. ✅ Test the app locally with SQLite
2. ⬜ Migrate existing JSON campaigns (if any)
3. ⬜ Prepare for production (env vars, gunicorn, Procfile)
4. ⬜ Deploy to Render/Heroku/VPS
5. ⬜ Add password hashing and stronger security
6. ⬜ (Optional) Switch to PostgreSQL for larger datasets

---

## 📝 File Descriptions

| File | Purpose |
|------|---------|
| `app_sqlite.py` | **Main app** — Flask backend with SQLite |
| `gin.html` | Frontend UI with login and dashboard |
| `requirements.txt` | Python package dependencies |
| `campaigns.db` | SQLite database (created on first run) |
| `MIGRATION.md` | SQLite setup and migration guide |
| `migrate_json_to_sqlite.py` | Script to import old JSON data |
| `README.md` | User-facing setup and usage guide |
| `.gitignore` | Git ignore rules |

---

## 👤 Demo User

- **Username:** `admin`
- **Password:** `1234`

(Auto-created on first app run)

---

## 📞 Support

For issues or questions:
1. Check `MIGRATION.md` for SQLite-specific help
2. Review `README.md` for general setup
3. Verify dependencies: `pip list`
4. Check Flask logs for error messages
5. Review API responses in browser DevTools (Network tab)

---

## 📄 License

This project is provided as-is for demo/learning purposes.

---

**Last Updated:** November 11, 2025  
**Current Version:** SQLite (v2.0)  
**Status:** Ready for local testing and deployment
