# 🧿 Anker Tattoo Studio — Backend API (Flask)

This is the backend API for the Anker Tattoo & Piercing Studio platform. Built with **Flask**, it powers all authentication, database management, and artist CRUD operations.

---

## 🚀 Features

- JWT Authentication (access + refresh tokens)
- Artist management (bio, profile image, social links, etc.)
- Admin-safe CRUD endpoints
- SQLite3 + SQLAlchemy
- Marshmallow schema validation
- Alembic (Flask-Migrate) for DB migrations

---

## 🛠️ Tech Stack

- Python 3.12+
- Flask
- Flask-JWT-Extended
- Flask-Migrate / Alembic
- SQLAlchemy ORM
- Marshmallow
- CORS enabled for React frontend

---

## 📁 Structure

```
backend/
├── app.py
├── config.py
├── extensions.py
├── models.py
├── routes.py
├── auth/
│   ├── views.py
│   ├── helpers.py
├── instance/
│   └── anker_freiburg.db
├── migrations/
├── .env
├── .flaskenv
```

---

## 🧪 Setup & Run

```bash
cd src
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# First time
flask db init
flask db migrate -m "initial"
flask db upgrade

# Run
flask run
```

---

## 🔐 Example Endpoints

```
POST   /auth/register
POST   /auth/login
GET    /artists
POST   /artists
PUT    /artists/:id
DELETE /artists/:id
```

> All secured routes require Bearer token in Authorization header.

---

## 🔐 .env

```
SQLALCHEMY_DATABASE_URI=sqlite:///instance/anker_freiburg.db
JWT_SECRET_KEY=your_secret_here
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5001
```

