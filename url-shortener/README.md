# 🔗 URL Shortener

A lightweight URL shortening service built with **FastAPI** and **SQLAlchemy**. Supports both auto-generated and custom slugs, with built-in link expiration after 3 days.

[See and test the live demo](https://smaller.onrender.com)

## Tech Stack

- **FastAPI** — async-ready web framework with automatic OpenAPI docs
- **SQLAlchemy** — ORM for database interactions
- **Jinja2** — server-side HTML templating
- **SQLite** (default) / **PostgreSQL** (production-ready via `DATABASE_URL`)

## Features

- 🔀 Auto-generates a random 6-character alphanumeric slug
- ✏️ Optional custom slugs (3–15 chars, no spaces)
- ♻️ Duplicate URL detection — returns existing short link instead of creating a new one
- ⏳ Links expire after **3 days** and return `410 Gone`
- 🧹 `/admin/cleanup` endpoint to manually purge stale links from the DB
- 🛑 Custom error pages for `4xx`/`5xx` responses

## Project Structure

```
url-shortener/
├── app.py          # Route handlers & app logic
├── models.py       # SQLAlchemy Link model
├── database.py     # Engine & session configuration
├── templates/      # Jinja2 HTML templates
└── static/         # Static assets
```

## Getting Started

```bash
# Clone the repo
git clone https://github.com/m6min/fastapi-lab/url-shortener
cd url-shortener

# Install dependencies
pip install fastapi sqlalchemy uvicorn jinja2 python-multipart

# Run the app
uvicorn app:app --reload
```

App will be available at `http://localhost:8000`.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./url_shortener.db` | Database connection string |

For PostgreSQL, set something like:
```
DATABASE_URL=postgresql://user:password@localhost/urlshortener
```

> The app handles the `postgres://` → `postgresql://` prefix fix automatically (e.g. for Heroku).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Home page |
| `POST` | `/` | Create a short URL |
| `GET` | `/{slug}` | Redirect to original URL |
| `GET` | `/admin/cleanup` | Delete links older than 3 days |

## Notes

- Slug uniqueness is enforced at the database level (`unique=True`)
- Expired links are lazily deleted on access, or bulk-removed via `/admin/cleanup`
- The app is structured for simplicity — no auth, no rate limiting (yet)