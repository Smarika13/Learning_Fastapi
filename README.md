# Learning FastAPI

A REST API built with FastAPI to manage student records, with full user authentication using JWT tokens.

---

## What This Project Does

This project is a backend API that allows authenticated users to perform CRUD operations on student data. Users must register and login before accessing any student endpoints.

---

## Features

- User registration with hashed passwords
- User login with JWT token generation
- Protected student routes — requires valid token to access
- Create, read, update, delete student records
- SQLite database with SQLAlchemy ORM
- Auto-generated API docs via Swagger UI

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation |
| passlib + bcrypt | Password hashing |
| python-jose | JWT token creation and verification |

---

## Project Structure

```
Learning_Fastapi/
├── main.py          # API endpoints
├── models.py        # Database table definitions
├── database.py      # Database connection setup
├── auth.py          # Password hashing and JWT logic
├── requirements.txt # Project dependencies
└── student.db       # SQLite database file
```

---

## Installation

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/Learning_Fastapi.git
cd Learning_Fastapi
```

**2. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the server**
```bash
uvicorn main:app --reload
```

**5. Open Swagger UI**
```
http://127.0.0.1:8000/docs
```

---

## API Endpoints

### Authentication (Public)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT token |

### Students (Protected — requires token)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/students` | Get all students |
| GET | `/students/{id}` | Get a single student |
| POST | `/students` | Create a new student |
| PUT | `/students/{id}` | Update a student |
| DELETE | `/students/{id}` | Delete a student |

---

## How to Test Authentication

**Step 1 — Register**
```json
POST /register
{
  "name": "Your Name",
  "email": "youremail@gmail.com",
  "password": "yourpassword"
}
```

**Step 2 — Login**
```json
POST /login
{
  "email": "youremail@gmail.com",
  "password": "yourpassword"
}
```
Copy the `access_token` from the response.

**Step 3 — Authorize in Swagger**

Click the **Authorize** button in Swagger UI. Paste your token in the Value field and click Authorize. All protected endpoints are now accessible.

---

## How Authentication Works

1. User registers — password is hashed using bcrypt and stored. Plain text password is never saved.
2. User logs in — server verifies password against stored hash. If correct, a JWT token is returned.
3. User sends token — every protected request must include the token in the Authorization header.
4. Server verifies token — if valid, request proceeds. If missing or expired, request is rejected with 401.

---

## HTTP Status Codes Used

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request (e.g. email already registered) |
| 401 | Unauthorized (wrong password or invalid token) |
| 403 | Forbidden (no token provided) |
| 404 | Not found |

---

## Notes

- JWT tokens expire after 30 minutes
- Never commit your real `SECRET_KEY` to GitHub — use environment variables in production
- The `student.db` file is your local database and can be deleted to reset all data