# Commerce — Auctions Web App

A simple Django-based e-commerce / auctions application (project root: `commerce`). This project contains a Django project (`commerce`) and an app `auctions` which implements listings, bidding, comments, categories, watchlists, authentication, and templates.

This README explains how to set up and run the project, where to find the main parts of the code, and basic usage.

## What this is

- A Django project with a single app `auctions` (templates in `templates/auctions`, static files in `static/auctions`).
- Includes models for listings, bids, comments, categories and user watchlists.
- Provides views and templates for listing index, create listing, view listing, category pages, watchlist, registration and login.

## Project layout (important files)

- `manage.py` — Django management script (run server, migrations, tests).
- `db.sqlite3` — SQLite database (committed here for convenience in some branches; be careful with production use).
- `auctions/` — Django app with models, views, templates and static files:
  - `auctions/models.py` — main data models.
  - `auctions/views.py` — request handlers.
  - `auctions/urls.py` — app URL routes.
  - `auctions/templates/auctions/` — HTML templates (index, create_listing, view_listing, watchlist, etc.).
  - `auctions/static/auctions/style.css` — styles.
- `commerce/` — Django project settings and WSGI/ASGI entrypoints.

## Setup (PowerShell)

1. Create a virtual environment and activate it (recommended):

```powershell
# from project root (where manage.py is)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install django
```

3. Apply migrations and prepare the database:

```powershell
python manage.py migrate
```
**Note:** The database file (`db.sqlite3`) is **not included** in this repository. It will be created when you run the `migrate` command above. If you need to create migrations for model changes, use:

```powershell
python manage.py makemigrations
```

4. (Optional) Create a superuser to access the admin site:

```powershell
python manage.py createsuperuser
```

5. Run the development server:

```powershell
python manage.py runserver
# then open http://127.0.0.1:8000/ in your browser
```

## Typical development workflow

- To create and apply migrations for model changes:

```powershell
python manage.py makemigrations
python manage.py migrate
```

- To collect static files (if you configure and use this step):

```powershell
python manage.py collectstatic
```

## App features and routes (common)

The `auctions` app typically exposes routes such as (check `auctions/urls.py` for exact URL names):

- `/` — index page listing active auctions
- `/create` — create a new listing
- `/listing/<id>` — view a single listing and bid/comment on it
- `/categories` or `/category/<name>` — category listing pages
- `/watchlist` — the current user's watchlist
- `/login`, `/logout`, `/register` — authentication

Templates live in `templates/auctions/` and include:
- `index.html`, `create_listing.html`, `view_listing.html`, `watchlist.html`, `category.html`, `login.html`, `register.html`, `layout.html` (base layout)

Static CSS is in `static/auctions/style.css`.

## Admin

- The Django admin is available (by default) at `/admin/` once you create a superuser.
- Register any models you want to view/edit from `auctions/admin.py`.

## Contributing

Feel free to fork this repository and submit pull requests to contribute to this project.

## License

This project is part of CS50's Web Programming with Python and JavaScript course.

