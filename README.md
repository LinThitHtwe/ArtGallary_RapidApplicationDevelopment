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

Open **http://127.0.0.1:9000/** in your browser.

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

