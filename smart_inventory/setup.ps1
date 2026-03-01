#!/bin/bash
# Smart Inventory — Quick Start Setup Script (Windows PowerShell)

# Colors for output
$INFO = "ℹ️  "
$SUCCESS = "✓ "
$ERROR = "✗ "

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Smart Inventory — Setup Script" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "$INFO Activating virtual environment..." -ForegroundColor Blue
.\venv\Scripts\Activate.ps1

# Check if MySQL is available
Write-Host "$INFO Checking MySQL connection..."
try {
    mysql -u root -e "SELECT 1" 2>$null
    Write-Host "$SUCCESS MySQL is available" -ForegroundColor Green
} catch {
    Write-Host "$ERROR MySQL not found. Please ensure MySQL is installed and running." -ForegroundColor Red
    Write-Host "  → Install from: https://dev.mysql.com/downloads/mysql/" -ForegroundColor Yellow
    exit 1
}

# Run Django migrations
Write-Host "$INFO Running Django migrations..." -ForegroundColor Blue
cd web
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "$SUCCESS Django migrations completed" -ForegroundColor Green
} else {
    Write-Host "$ERROR Django migrations failed" -ForegroundColor Red
    exit 1
}

# Start development server
Write-Host ""
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "$SUCCESS Setup Complete! Starting Django server..." -ForegroundColor Green
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Django development server running at: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Django admin panel at:                  http://127.0.0.1:8000/admin/" -ForegroundColor Green
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver
