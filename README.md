# FastAPI Projects
Small FastAPI projects im coding for learning purposes.

## 1- URL Shortener

A lightweight URL shortening service built with **FastAPI** and **SQLAlchemy**. Supports both auto-generated and custom slugs, with built-in link expiration after 3 days.

[See and test the live demo](https://smaller.onrender.com)

### Tech Stack

- **FastAPI** — async-ready web framework with automatic OpenAPI docs
- **SQLAlchemy** — ORM for database interactions
- **Jinja2** — server-side HTML templating
- **SQLite** (default) / **PostgreSQL** (production-ready via `DATABASE_URL`)
