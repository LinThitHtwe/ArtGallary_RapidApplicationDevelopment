# Art Gallery RAD - Makefile (Windows-friendly)
# Use: make <target>. Requires make (e.g. from Git for Windows, Chocolatey, or WSL).

# Use forward slashes (works on Windows and Unix with make)
PYTHON = venv/Scripts/python.exe
PIP = venv/Scripts/pip.exe

.PHONY: venv init install run migrate shell clean help

# Create virtual environment
venv:
	python -m venv venv

# First-time setup: create venv and install dependencies
init: venv
	$(PIP) install -r requirements.txt

# Install dependencies (run after venv)
install: venv
	$(PIP) install -r requirements.txt

# Run Django development server (port 9000)
run:
	$(PYTHON) manage.py runserver 9000

# Apply migrations
migrate:
	$(PYTHON) manage.py migrate

# Create new migrations
makemigrations:
	$(PYTHON) manage.py makemigrations

# Django shell
shell:
	$(PYTHON) manage.py shell

# Create superuser (interactive)
superuser:
	$(PYTHON) manage.py createsuperuser

# Install deps and run (full init + run)
up: install migrate run

# Remove venv and cache
clean:
	rmdir /s /q venv 2>nul || true
	del /s /q __pycache__ 2>nul || true

# Show help
help:
	@echo Art Gallery RAD - available targets:
	@echo   make venv         - Create virtual environment
	@echo   make init        - First-time: create venv + install deps
	@echo   make install     - Create venv and install dependencies
	@echo   make run          - Run Django dev server
	@echo   make migrate      - Apply database migrations
	@echo   make makemigrations - Create migrations
	@echo   make shell        - Django shell
	@echo   make superuser    - Create superuser
	@echo   make up           - install + migrate + run
	@echo   make clean        - Remove venv and pycache
	@echo   make help         - Show this help
