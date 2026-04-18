# Art Gallery RAD

Django MTV project: **pages** (UI), **artists**, **gallery** (Artwork + Category), **blog** (Post).

## Developer setup (2 steps)

1. **Initialize** (create venv + install dependencies):
   ```bash
   .\make init
   ```

2. **Run the dev server** (port 9000):
   ```bash
   venv\Scripts\python.exe manage.py runserver 9000
   ```

**One-shot (install deps, migrate, then server on port 9000):** from the project folder run `.\dev.cmd` or `.\make.bat up` (same as `.\make.ps1 up`).

Open **http://127.0.0.1:9000/** in your browser.

### Static gallery HTML (under `/pages/`)

The former root `.html` files now live as Django templates in **`pages/templates/pages/gallery/`**. Examples: **`/pages/`** (main landing), **`/pages/fabiola-morcillo/`**, **`/pages/valentin-pavageau/`**, **`/pages/butcher-billy/`**, **`/pages/david-sosella/`**, **`/pages/kyle-lambert/`**.

Shared CSS: **`pages/static/pages/styles.css`**. Images stay in **`assets/`** and load via Django **`{% static %}`**.

### Staff dashboard (content management)

- Sign in at **`/dashboard/login/`**. Only **staff** accounts (`is_staff=True`) can use it; everyone else stays on the public site.
- Create a staff user: `python manage.py createsuperuser` (superusers are staff by default).
- From the dashboard, staff manage **artists**, **artworks** (uploads are saved as files under **`assets/`**), **posts**, and **categories**. The public “Add content” page was removed.

---

## Database: SQL Server (SSMS)

The project can use **Microsoft SQL Server** (e.g. with SQL Server Management Studio 21) or **SQLite** (default).

### Using SQL Server

1. **Create a database** in SSMS (e.g. `art_gallery`).

2. **Copy env template** and set your connection details:
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set at least:
   - `DB_NAME` – database name (e.g. `art_gallery`)
   - `DB_USER` – SQL Server login
   - `DB_PASSWORD` – password for that login
   - `DB_HOST` – server (e.g. `127.0.0.1` or `localhost`; for a named instance use `host\instance`)
   - `DB_PORT` – usually `1433` (leave empty for default)

3. **ODBC driver**: Ensure **ODBC Driver 17 for SQL Server** (or 18) is installed. It often comes with SSMS; otherwise install from [Microsoft ODBC Driver for SQL Server](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

4. **Install dependencies** (if not already):
   ```bash
   venv\Scripts\pip install -r requirements.txt
   ```

5. **Run migrations**:
   ```bash
   venv\Scripts\python.exe manage.py migrate
   ```

If `DB_NAME` is not set in `.env`, the app uses **SQLite** (no SQL Server required).

---

