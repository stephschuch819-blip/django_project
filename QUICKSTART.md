# Quick Start Guide

## Fast Setup (Windows)

1. **Run the setup script**
   ```bash
   setup.bat
   ```

2. **Configure environment**
   - Copy `.env.example` to `.env`
   - Edit `.env` with your database credentials

3. **Setup database**
   ```bash
   # Activate virtual environment first
   venv\Scripts\activate
   
   # Run migrations
   python manage.py makemigrations
   python manage.py migrate
   
   # Create admin user
   python manage.py createsuperuser
   ```

4. **Start the server**
   ```bash
   python manage.py runserver
   ```

5. **Access the application**
   - Admin Panel: http://localhost:8000/admin/
   - Beneficiary Portal: http://localhost:8000/

## Creating Your First Case

1. Login to admin panel at http://localhost:8000/admin/
2. Click "Beneficiary Cases" → "Add Beneficiary Case"
3. Fill in the form:
   - Beneficiary Name: John Doe
   - Email: john@example.com
   - Password: TestPass123 (min 8 characters)
   - Deceased Name: Jane Doe
   - Description: Estate of Jane Doe
4. Click "Save"
5. Note the auto-generated Case Number (e.g., DG-ABC123)

## Adding Assets

1. Click "Assets" → "Add Asset"
2. Select the case you just created
3. Choose asset type (e.g., Bank Account)
4. Enter description and estimated value
5. Set status to "Unclaimed"
6. Click "Save"

## Testing Beneficiary Login

1. Go to http://localhost:8000/
2. Enter the case number (e.g., DG-ABC123)
3. Enter the password you set (e.g., TestPass123)
4. Click "Login to Portal"
5. Explore the dashboard, assets, documents, and messages

## Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running
- Check `.env` file has correct database credentials
- Verify database exists: `CREATE DATABASE delegacy_db;`

### Module Not Found Error
- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`

### Static Files Not Loading
- Run: `python manage.py collectstatic`
- Ensure DEBUG=True in development

### Port Already in Use
- Use different port: `python manage.py runserver 8080`
- Or stop the process using port 8000

## Default Credentials

After running `createsuperuser`, use those credentials for admin access.

For beneficiaries, credentials are set when creating a case in the admin panel.

---

**Need Help?** Check the full README.md for detailed documentation.
