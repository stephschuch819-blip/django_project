# Installation Guide - Delegacy Portal

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for application + database

### Recommended Requirements
- **Python**: 3.10 or higher
- **PostgreSQL**: 14 or higher
- **RAM**: 8GB
- **Disk Space**: 2GB

## Step-by-Step Installation

### Step 1: Install Python

#### Windows
1. Download Python from https://www.python.org/downloads/
2. Run the installer
3. **Important**: Check "Add Python to PATH"
4. Verify installation:
   ```bash
   python --version
   ```

#### macOS
```bash
# Using Homebrew
brew install python@3.10
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip
```

### Step 2: Install PostgreSQL

#### Windows
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Run the installer
3. Remember the password you set for the postgres user
4. Default port: 5432

#### macOS
```bash
# Using Homebrew
brew install postgresql@14
brew services start postgresql@14
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### Step 3: Create Database

#### Using psql (Command Line)
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE delegacy_db;

# Create user (optional)
CREATE USER delegacy_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE delegacy_db TO delegacy_user;

# Exit
\q
```

#### Using pgAdmin (GUI)
1. Open pgAdmin
2. Right-click "Databases" → "Create" → "Database"
3. Name: `delegacy_db`
4. Click "Save"

### Step 4: Clone/Download Project

```bash
# Navigate to your projects directory
cd C:\Users\User\CascadeProjects\delegacy

# Or if downloading, extract the ZIP file to this location
```

### Step 5: Create Virtual Environment

#### Windows
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# You should see (venv) in your command prompt
```

#### macOS/Linux
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your terminal
```

### Step 6: Install Dependencies

```bash
# Make sure virtual environment is activated
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages**:
- Django 4.2.7
- psycopg2-binary 2.9.9
- python-decouple 3.8
- Pillow 10.1.0
- django-crispy-forms 2.1
- crispy-bootstrap5 1.0.0
- whitenoise 6.6.0

### Step 7: Configure Environment Variables

1. **Copy the example file**:
   ```bash
   # Windows
   copy .env.example .env
   
   # macOS/Linux
   cp .env.example .env
   ```

2. **Edit .env file** with your settings:
   ```env
   SECRET_KEY=your-secret-key-here-make-it-long-and-random
   DEBUG=True
   DATABASE_NAME=delegacy_db
   DATABASE_USER=postgres
   DATABASE_PASSWORD=your_postgres_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   ```

3. **Generate a SECRET_KEY** (optional but recommended):
   ```python
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

### Step 8: Run Database Migrations

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Expected output**:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, portal, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  ...
  Applying portal.0001_initial... OK
```

### Step 9: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

**You will be prompted for**:
- Username: (e.g., admin)
- Email: (e.g., admin@delegacy.com)
- Password: (min 8 characters)
- Password confirmation

### Step 10: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 11: (Optional) Load Sample Data

```bash
python manage.py create_sample_data
```

This creates:
- 3 sample beneficiary cases
- Multiple assets per case
- Sample messages
- Admin user (username: admin, password: admin123)

### Step 12: Run Development Server

```bash
python manage.py runserver
```

**Expected output**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'delegacy_portal.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 13: Access the Application

Open your web browser and navigate to:

- **Beneficiary Portal**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/

## Verification Checklist

After installation, verify:

- [ ] Python version is 3.8+
- [ ] PostgreSQL is running
- [ ] Database `delegacy_db` exists
- [ ] Virtual environment is activated
- [ ] All dependencies installed successfully
- [ ] `.env` file is configured
- [ ] Migrations completed without errors
- [ ] Superuser created
- [ ] Static files collected
- [ ] Development server starts
- [ ] Can access login page
- [ ] Can access admin panel

## Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Activate virtual environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Issue: "FATAL: password authentication failed"
**Solution**: Check PostgreSQL credentials in `.env` file
- Verify DATABASE_USER
- Verify DATABASE_PASSWORD
- Verify DATABASE_NAME exists

### Issue: "Port 8000 is already in use"
**Solution**: Use a different port
```bash
python manage.py runserver 8080
```

### Issue: "psycopg2 installation failed"
**Solution**: Install PostgreSQL development files
```bash
# Windows: Use psycopg2-binary (already in requirements.txt)

# macOS
brew install postgresql

# Linux
sudo apt-get install libpq-dev python3-dev
```

### Issue: "Static files not loading"
**Solution**: 
1. Ensure DEBUG=True in development
2. Run `python manage.py collectstatic`
3. Check STATIC_URL and STATIC_ROOT in settings.py

### Issue: "Database connection refused"
**Solution**: 
1. Verify PostgreSQL is running
   ```bash
   # Windows
   services.msc (look for PostgreSQL)
   
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```
2. Check DATABASE_HOST and DATABASE_PORT in `.env`

### Issue: "Migration conflicts"
**Solution**: 
```bash
# Delete migration files (except __init__.py)
# Then recreate
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Permission denied on media folder"
**Solution**: 
```bash
# Windows
icacls media /grant Users:F /T

# macOS/Linux
chmod -R 755 media/
```

## Alternative Database Setup (SQLite for Testing)

If you want to quickly test without PostgreSQL:

1. **Edit `delegacy_portal/settings.py`**:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

**Note**: SQLite is for development/testing only. Use PostgreSQL for production.

## Next Steps

After successful installation:

1. **Read the documentation**:
   - README.md - Complete guide
   - QUICKSTART.md - Quick reference
   - FEATURES.md - Feature list

2. **Create your first case**:
   - Login to admin panel
   - Add a beneficiary case
   - Add assets to the case
   - Test beneficiary login

3. **Customize the application**:
   - Update color scheme in `templates/base.html`
   - Add your agency logo
   - Customize email templates
   - Configure production settings

4. **Prepare for production**:
   - Set DEBUG=False
   - Configure proper SECRET_KEY
   - Set up HTTPS
   - Configure email backend
   - Set up backups

## Support

If you encounter issues not covered here:

1. Check Django documentation: https://docs.djangoproject.com/
2. Check PostgreSQL documentation: https://www.postgresql.org/docs/
3. Review error logs in the terminal
4. Check Django debug page (if DEBUG=True)

## Quick Commands Reference

```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Run server
python manage.py runserver

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py create_sample_data

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell

# Run tests
python manage.py test
```

---

**Installation Complete!** 🎉

You're now ready to use Delegacy Portal.
