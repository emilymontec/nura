@echo off
echo ====================================
echo NURA - Iniciando proyecto completo
echo ====================================
echo.

echo [1/2] Iniciando servidor Django (backend)...
start "NURA Backend" cmd /k "cd /d "%~dp0" && python manage.py runserver"

timeout /t 3 /nobreak >nul

echo [2/2] Iniciando frontend (React + Vite)...
start "NURA Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

echo.
echo ====================================
echo Proyecto iniciado!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo ====================================
