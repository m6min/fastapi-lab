# URL Shortener

A lightweight URL shortening service built with **FastAPI** and **SQLAlchemy**. Supports both auto-generated and custom slugs, with built-in link expiration after 3 days.

[Try the live demo](https://shorter.onrender.com). The demo may take some time to wake up or be unavailable due to free-tier limits.

## Tech Stack

- **FastAPI** — async-ready web framework
- **SQLAlchemy** — ORM for database interactions
- **Jinja2** — server-side HTML templating
- **SQLite** (local default) / **PostgreSQL** (configured via `DATABASE_URL`)

## Features

- Auto-generates a random 6-character alphanumeric slug
- Optional custom slugs (3–15 chars, no spaces)
-  Duplicate URL detection — returns existing short link instead of creating a new one
-  Links expire after **3 days** and return `410 Gone`
-  `/admin/cleanup` endpoint to manually purge stale links from the DB
-  Custom error pages for `4xx`/`5xx` responses

## Project Structure

```
url-shortener/
├── main.py         # Route handlers & app logic
├── models.py       # SQLAlchemy Link model
├── database.py     # Engine & session configuration
├── templates/      # Jinja2 HTML templates
└── static/         # Static assets
```

## Getting Started

```bash
# Clone the repo
git clone https://github.com/m6min/fastapi-lab.git
cd fastapi-lab/url-shortener

# Install dependencies
python -m pip install -r requirements.txt

# Run the app
python -m uvicorn main:app --reload
```

App will be available at `http://localhost:8000`.

Use a virtual environment for local development. The existing development environment uses Python 3.13.
## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./url_shortener.db` | Database connection string |

No environment variables are required for local SQLite usage. For PostgreSQL, set `DATABASE_URL` in your shell or in Render's Environment settings. PowerShell example:
```powershell
$env:DATABASE_URL = "postgresql://user:password@localhost/urlshortener"
```

The app reads process environment variables; it does not automatically load `.env` files. `.env.example` only documents the connection string format. Never commit real database credentials.

The app handles the `postgres://` → `postgresql://` prefix automatically and creates missing tables on startup. The database must already exist and be reachable.

## Render Deployment

| Setting | Value |
|---|---|
| Language | Python 3 |
| Branch | `main` |
| Root Directory | `url-shortener` (within the `fastapi-lab` repository) |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| Health Check Path | `/ping` |
| `PYTHON_VERSION` environment variable | `3.13.2` |
| `DATABASE_URL` environment variable | Your Render Postgres Internal Database URL |

Keep the web service and database in the same region. Local SQLite data on Render's default filesystem is lost on restarts or redeploys. Free Render Postgres databases expire after 30 days; see [Render's free-tier limits](https://render.com/docs/free).

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Home page |
| `POST` | `/` | Create a short URL |
| `GET` | `/{slug}` | Redirect to original URL |
| `GET` | `/admin/cleanup` | Delete links older than 3 days |
| `GET` | `/ping` | Application health check (does not check the database) |

## Notes

- Slug uniqueness is enforced at the database level (`unique=True`)
- Expired links are lazily deleted on access, or bulk-removed via `/admin/cleanup`
- This is a learning/demo project with no authentication or rate limiting; `/admin/cleanup` is publicly accessible.
- The background self-ping targets `https://shorter.onrender.com/ping`. It does not guarantee that a free service stays awake.
