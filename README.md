# Delegacy Portal

A secure, Django-based digital inheritance agency platform featuring a public-facing beneficiary portal and a comprehensive Super Admin panel.

## Features

### Beneficiary Portal
- **Secure Authentication**: Login using unique case number and password
- **Dashboard**: Overview of all assets with estimated values and status tracking
- **Asset Management**: View detailed information about inherited assets
- **Document Access**: Download case-related documents securely
- **Messaging System**: Communicate directly with the agency team

### Super Admin Panel
- **Complete CRUD Operations**: Manage beneficiary cases, assets, and documents
- **User Management**: Create and manage admin accounts
- **Message Management**: View and respond to beneficiary messages
- **Status Workflow Control**: Manually update asset statuses through the workflow:
  - Unclaimed → Processing → Ready for Transfer → Completed
- **Rich Admin Interface**: Enhanced Django admin with custom displays and filters

## Technology Stack

- **Backend**: Python 3.x with Django 4.2
- **Database**: PostgreSQL (configurable for MySQL)
- **Frontend**: Bootstrap 5, Bootstrap Icons
- **Forms**: Django Crispy Forms with Bootstrap 5
- **Security**: Built-in Django security features, CSRF protection, XSS prevention

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**
   ```bash
   cd delegacy
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update the following variables:
     ```
     SECRET_KEY=your-secret-key-here
     DEBUG=True
     DATABASE_NAME=delegacy_db
     DATABASE_USER=postgres
     DATABASE_PASSWORD=your-password
     DATABASE_HOST=localhost
     DATABASE_PORT=5432
     ```

6. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE delegacy_db;
   ```

7. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create a superuser (admin account)**
   ```bash
   python manage.py createsuperuser
   ```

9. **Collect static files**
   ```bash
   python manage.py collectstatic --noinput
   ```

10. **Run the development server**
    ```bash
    python manage.py runserver
    ```

11. **Access the application**
    - Beneficiary Portal: http://localhost:8000/
    - Admin Panel: http://localhost:8000/admin/

## Usage

### For Super Admins

1. **Login to Admin Panel**
   - Navigate to http://localhost:8000/admin/
   - Use your superuser credentials

2. **Create a Beneficiary Case**
   - Go to "Beneficiary Cases" → "Add Beneficiary Case"
   - Fill in beneficiary details
   - Set a secure password (min 8 characters)
   - A unique case number will be auto-generated (format: DG-XXXXXX)

3. **Add Assets**
   - Go to "Assets" → "Add Asset"
   - Select the beneficiary case
   - Choose asset type and enter details
   - Set initial status (default: Unclaimed)

4. **Upload Documents**
   - Go to "Documents" → "Add Document"
   - Select the case and upload file
   - Toggle visibility for beneficiary access

5. **Manage Messages**
   - View all messages in "Messages"
   - Reply to beneficiary inquiries
   - Messages are automatically linked to cases

### For Beneficiaries

1. **Login**
   - Navigate to http://localhost:8000/
   - Enter your case number (e.g., DG-ABC123)
   - Enter the password provided by the agency

2. **View Dashboard**
   - See overview of all assets
   - Check total estimated value
   - View unread messages count

3. **Browse Assets**
   - Click "Assets" to view detailed asset information
   - Check status of each asset
   - Track progress through workflow stages

4. **Download Documents**
   - Click "Documents" to access available files
   - Download documents related to your case

5. **Send Messages**
   - Click "Messages" to communicate with the agency
   - View message history
   - Send new inquiries

## Security Features

- **CSRF Protection**: All forms are protected against Cross-Site Request Forgery
- **XSS Prevention**: Django's template system auto-escapes content
- **SQL Injection Protection**: Django ORM prevents SQL injection attacks
- **Secure Sessions**: HTTP-only cookies and secure session management
- **Password Validation**: Minimum length requirements and validation
- **Content Security**: X-Frame-Options and Content-Type-Nosniff headers

## Asset Status Workflow

Assets follow a defined workflow that Super Admins control:

1. **Unclaimed**: Asset identified but not yet claimed
2. **Processing**: DGLegacy is verifying beneficiary identity and preparing legal documentation
3. **Ready**: Verification complete. Legal assistance will be provided to help beneficiary claim the asset
4. **Completed**: Beneficiary has successfully claimed the asset with DGLegacy's assistance

**Note**: DGLegacy does not have direct access to inherited assets. Our role is to verify beneficiaries, prepare legal documentation, and provide lawyers to assist in claiming inheritance from the respective institutions.

## Design Inspiration

The UI design draws inspiration from DGLegacy.com with:
- Professional blue color scheme (#1e3a5f primary, #4a90e2 accent)
- Clean, modern card-based layouts
- Intuitive navigation and user experience
- Responsive design for all devices
- Clear status indicators and progress tracking

## Project Structure

```
delegacy/
├── delegacy_portal/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── portal/                   # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View logic
│   ├── forms.py             # Form definitions
│   ├── admin.py             # Admin customization
│   └── urls.py              # URL routing
├── templates/               # HTML templates
│   ├── base.html
│   └── portal/
│       ├── login.html
│       ├── dashboard.html
│       ├── assets.html
│       ├── documents.html
│       └── messages.html
├── static/                  # Static files (CSS, JS)
├── media/                   # Uploaded files
├── requirements.txt         # Python dependencies
└── manage.py               # Django management script
```

## Database Models

- **BeneficiaryCase**: Stores beneficiary information and case details
- **Asset**: Represents inherited assets with type, value, and status
- **Document**: File storage for case-related documents
- **Message**: Internal messaging between beneficiaries and admins

## Development Notes

- The current implementation uses plain text password storage for simplicity. In production, implement proper password hashing using Django's built-in authentication system.
- Ensure DEBUG=False in production environments
- Configure proper email backend for notifications
- Set up proper file storage (e.g., AWS S3) for production document handling
- Implement SSL/TLS for secure connections in production

## Support

For issues or questions about the Delegacy Portal, please contact your system administrator.

## License

Proprietary - All rights reserved

---

**Built with Django** | **Secure Digital Inheritance Management**
