# FastAPI Template

A production-ready FastAPI template with authentication, user management, role support, database integration, and best practices for modern Python web APIs.

---

## Features

- **FastAPI**: High-performance, easy-to-use Python web framework
- **SQLAlchemy**: ORM for database models and migrations (with Alembic)
- **Pydantic**: Data validation and serialization
- **Authentication**: JWT-based login and registration
- **Role Management**: Enum-based roles for users
- **CORS**: Configurable origins
- **Environment-based config**: `.env` support
- **Custom Middleware**: Consistent API response format
- **Auto-generated OpenAPI docs**: Swagger UI and ReDoc

---

## Getting Started

### 1. Clone the repository

```sh
git clone <your-repo-url>
cd template-fast-api
```

### 2. Create and activate a virtual environment

```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Generate `requirements.txt`

If you haven't created `requirements.txt` yet, generate it from your current environment:

```sh
pip freeze > requirements.txt
```

---

### 5. Generate and run database migrations

**A. Generate a new migration (autogenerate from models):**

```sh
alembic revision --autogenerate -m "Initial migration"
```

**B. Apply the migration (upgrade the database):**

```sh
alembic upgrade head
```

### 6. Start the application

```sh
uvicorn app.main:app --reload
```

---

## Project Structure

```
app/
  ├── api/                # API routers and endpoints
  ├── core/               # Core settings and security
  ├── db/                 # Database utilities
  ├── models/             # SQLAlchemy models
  ├── schemas/            # Pydantic schemas
  ├── enum/               # Enum definitions (e.g., roles)
  ├── main.py             # FastAPI app entrypoint
alembic/                  # Alembic migrations
.env                      # Environment variables
requirements.txt
README.md
```

---

## API Docs

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## Custom Response Format

All JSON responses are wrapped as:

```json
{
  "statusCode": 200,
  "message": "Success",
  "data": { ... }
}
```

For errors:

```json
{
  "statusCode": 400,
  "message": "Error message here"
}
```

---

## License
