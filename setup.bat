@echo off
echo ========================================
echo Delegacy Portal Setup Script
echo ========================================
echo.

echo Creating virtual environment...
py -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Installing dependencies...
pip install -r requirements.txt
echo.

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo Next steps:
echo 1. Copy .env.example to .env and configure your database settings
echo 2. Create your PostgreSQL database
echo 3. Run: py manage.py makemigrations
echo 4. Run: py manage.py migrate
echo 5. Run: py manage.py createsuperuser
echo 6. Run: py manage.py runserver
echo.
pause
