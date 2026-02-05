# Art Gallery RAD - PowerShell "make" (no make.exe required)
# Usage: .\make.ps1 <target>   e.g.  .\make.ps1 run

param([Parameter(Position=0)] [string] $Target = "help")

$Py = "venv\Scripts\python.exe"
$Pip = "venv\Scripts\pip.exe"

function Ensure-Venv {
    if (-not (Test-Path $Py)) {
        Write-Host "Creating virtual environment..."
        python -m venv venv
    }
}

switch ($Target.ToLower()) {
    "venv"  {
        if (Test-Path "venv") { Write-Host "venv already exists." } else { python -m venv venv; Write-Host "Done." }
    }
    "init"  {
        Ensure-Venv
        & $Pip install -r requirements.txt
        Write-Host "Done. Run: .\make.ps1 run"
    }
    "install" {
        Ensure-Venv
        & $Pip install -r requirements.txt
        Write-Host "Done."
    }
    "run"   {
        if (-not (Test-Path $Py)) { Ensure-Venv; & $Pip install -r requirements.txt }
        & $Py manage.py runserver
    }
    "migrate" {
        & $Py manage.py migrate
    }
    "makemigrations" {
        & $Py manage.py makemigrations
    }
    "shell" {
        & $Py manage.py shell
    }
    "superuser" {
        & $Py manage.py createsuperuser
    }
    "up"    {
        Ensure-Venv
        & $Pip install -r requirements.txt
        & $Py manage.py migrate
        & $Py manage.py runserver
    }
    "clean" {
        if (Test-Path "venv") { Remove-Item -Recurse -Force venv; Write-Host "Removed venv." }
        Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host "Done."
    }
    "help"  {
        Write-Host "Art Gallery RAD - available targets:"
        Write-Host "  .\make.ps1 venv         - Create virtual environment"
        Write-Host "  .\make.ps1 init         - First-time: create venv + install deps"
        Write-Host "  .\make.ps1 install      - Create venv and install dependencies"
        Write-Host "  .\make.ps1 run          - Run Django dev server"
        Write-Host "  .\make.ps1 migrate      - Apply database migrations"
        Write-Host "  .\make.ps1 makemigrations - Create migrations"
        Write-Host "  .\make.ps1 shell        - Django shell"
        Write-Host "  .\make.ps1 superuser    - Create superuser"
        Write-Host "  .\make.ps1 up           - install + migrate + run"
        Write-Host "  .\make.ps1 clean        - Remove venv and __pycache__"
        Write-Host "  .\make.ps1 help         - Show this help"
    }
    default {
        Write-Host "Unknown target: $Target. Use .\make.ps1 help"
        exit 1
    }
}
