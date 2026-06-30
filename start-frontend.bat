@echo off
echo Iniciando frontend...
cd /d "%~dp0frontend"
npm install
npm run dev
