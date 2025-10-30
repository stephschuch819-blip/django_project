# DGLegacy Beneficiary Portal - Complete Guide

## 📋 Table of Contents
1. [Quick Start](#quick-start)
2. [Features Overview](#features-overview)
3. [Admin Configuration](#admin-configuration)
4. [Mobile Responsiveness](#mobile-responsiveness)
5. [Testing Guide](#testing-guide)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Installation
```bash
# 1. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Setup site settings and FAQs
python manage.py setup_site_settings

# 6. Create sample data (optional)
python manage.py create_sample_data

# 7. Run server
python manage.py runserver
```

### Access Points
- **Beneficiary Portal:** http://localhost:8000/
- **Admin Panel:** http://localhost:8000/admin/
- **Help Page:** http://localhost:8000/help/

### Sample Login
- **Case Number:** DG-IQ14U6
- **Password:** password123

---

## ✨ Features Overview

### Beneficiary Portal Features

#### 1. **Dashboard**
- Welcome message with case number
- 3 stat cards (Total Assets, Estimated Value, Unread Messages)
- **Next Steps card** - Shows current progress and action items
- **Progress Timeline** - Visual 4-stage progress tracker
- Recent assets table
- Asset status chart

#### 2. **Assets Page**
- **Search bar** - Search by type or description
- **Status filter** - Filter by Unclaimed, Processing, Ready, Completed
- **Sort options** - By value (high/low), type, or date
- **Asset cards** - Click to view detailed modal
- **Asset modal** - Full details with next steps

#### 3. **Documents Page**
- View all documents (admin + beneficiary uploaded)
- **Upload documents** - Drag & drop or click to upload
- Download documents
- Document descriptions

#### 4. **Messages Page**
- View message history
- Send messages to admin
- Unread message indicators
- Bidirectional communication

#### 5. **Help/FAQ Page**
- 6+ comprehensive FAQs
- Quick action buttons
- Contact information
- Accordion interface

### Admin Panel Features

#### 1. **Beneficiary Cases**
- Full CRUD operations
- Auto-generated case numbers (DG-XXXXXX)
- Inline editing (assets, documents, messages)
- Search and filters

#### 2. **Assets**
- 8 asset types
- 4-stage workflow (Unclaimed → Processing → Ready → Completed)
- Status badges with colors
- Bulk actions

#### 3. **Documents**
- **Upload source tracking** - See if admin or beneficiary uploaded
- Visibility controls
- File management
- Filter by uploader

#### 4. **Messages**
- Bidirectional messaging
- Read/unread status
- Sender identification
- **Message templates** - Reusable messages with placeholders

#### 5. **Site Settings** (Configurable)
- Contact information (phone, email, address)
- Business hours
- Timeline estimates
- Social media links
- Support messages

#### 6. **FAQs** (Configurable)
- Add/edit/delete FAQs
- Reorder by priority
- Show/hide toggle
- Custom icons

#### 7. **Message Templates**
- Pre-written message templates
- Use placeholders: {{beneficiary_name}}, {{case_number}}
- Quick messaging

#### 8. **Case Description Templates**
- Pre-written case descriptions
- Use placeholders: {{deceased_name}}, {{beneficiary_name}}
- Standardize case creation

---

## 🎛️ Admin Configuration

### What Admins Can Configure (No Code Required)

#### Site Settings
1. Go to **Admin → Site Settings**
2. Edit:
   - Support phone/email
   - Company address
   - Business hours
   - Timeline estimates (4-12 weeks, etc.)
   - Social media URLs
   - Help text messages

#### FAQs
1. Go to **Admin → FAQs**
2. Add/Edit FAQs:
   - Question
   - Answer (HTML allowed)
   - Icon (Bootstrap icon class)
   - Order (display priority)
   - Active status

#### Message Templates
1. Go to **Admin → Message Templates**
2. Create templates:
   - Name: "Welcome Message"
   - Subject: "Welcome to DGLegacy"
   - Content: Use {{beneficiary_name}} and {{case_number}}

#### Case Description Templates
1. Go to **Admin → Case Description Templates**
2. Create templates:
   - Name: "Standard Inheritance"
   - Description: Use {{deceased_name}} and {{beneficiary_name}}

---

## 📱 Mobile Responsiveness

### Responsive Features

#### Breakpoints
- **Mobile:** < 768px
- **Tablet:** 768px - 1024px
- **Desktop:** > 1024px

#### Mobile Optimizations
✅ **Dashboard:**
- Stat cards stack vertically
- Next Steps card fully responsive
- Progress timeline adapts
- Touch-friendly buttons

✅ **Assets:**
- Filter bar stacks
- Cards display in single column
- Modal works on mobile
- Touch-friendly interactions

✅ **Documents:**
- Cards stack vertically
- Upload button full-width
- File list scrollable

✅ **Messages:**
- Form full-width
- Message history scrollable
- Touch-friendly send button

✅ **Help:**
- Accordion works perfectly
- Sidebar stacks below content
- Quick actions stack

✅ **Navigation:**
- Hamburger menu on mobile
- Touch-friendly nav items
- Proper spacing

✅ **Login:**
- Card centered
- Security badges stack
- Password toggle works

### Mobile Testing Checklist
- [ ] Dashboard loads correctly
- [ ] Assets page filter works
- [ ] Asset modal opens
- [ ] Documents upload works
- [ ] Messages send successfully
- [ ] Help accordion expands
- [ ] Navbar hamburger menu works
- [ ] All buttons are touch-friendly (min 44px)
- [ ] Text is readable
- [ ] No horizontal scrolling

---

## 🧪 Testing Guide

### Functional Testing

#### 1. Login Flow
```
1. Go to http://localhost:8000/
2. Enter: DG-IQ14U6 / password123
3. Click eye icon to show/hide password
4. Click "Login to Portal"
5. Should redirect to dashboard
```

#### 2. Dashboard
```
1. Check stat cards display correctly
2. Verify Next Steps card shows progress
3. Check Progress Timeline displays
4. Click on asset in table
5. Verify chart displays
```

#### 3. Assets
```
1. Go to Assets page
2. Type in search bar
3. Select status filter
4. Change sort option
5. Click asset card → modal opens
6. Verify modal shows all details
7. Click "Clear" to reset filters
```

#### 4. Documents
```
1. Go to Documents page
2. Click "Choose File"
3. Select a PDF/image
4. Enter title and description
5. Click "Upload Document"
6. Verify success message
7. Check document appears in list
8. Download a document
```

#### 5. Messages
```
1. Go to Messages page
2. Enter subject and message
3. Click "Send Message"
4. Verify message appears in history
5. Check unread count updates
```

#### 6. Help
```
1. Go to Help page
2. Click FAQ to expand
3. Verify content displays
4. Click quick action buttons
5. Test contact links
```

### Admin Testing

#### 1. Site Settings
```
1. Login to /admin/
2. Click "Site Settings"
3. Change support phone
4. Save
5. Verify change on frontend
```

#### 2. FAQs
```
1. Go to Admin → FAQs
2. Click "Add FAQ"
3. Fill in question/answer
4. Set order and icon
5. Save
6. Check Help page
```

#### 3. Document Tracking
```
1. Login as beneficiary
2. Upload a document
3. Login to admin
4. Go to Documents
5. Verify "👤 Beneficiary" shows
6. Filter by "Uploaded by beneficiary: Yes"
```

#### 4. Templates
```
1. Go to Admin → Message Templates
2. Create template with {{beneficiary_name}}
3. Go to Admin → Case Description Templates
4. Create template with {{deceased_name}}
5. Use templates when creating cases/messages
```

### Mobile Testing

#### Using Browser DevTools
```
1. Press F12 (open DevTools)
2. Press Ctrl+Shift+M (toggle device toolbar)
3. Select device (iPhone, Android, iPad)
4. Test all pages
5. Check touch interactions
6. Verify no horizontal scroll
7. Test hamburger menu
```

#### Real Device Testing
```
1. Get your phone
2. Connect to same network as dev server
3. Find your computer's IP: ipconfig (Windows) / ifconfig (Mac)
4. On phone, go to: http://[YOUR-IP]:8000/
5. Test all features
6. Check touch responsiveness
7. Test form inputs
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. **Admin models not showing**
**Problem:** New models (Site Settings, FAQs) not in admin
**Solution:**
```bash
# Hard refresh browser
Ctrl + F5 (Windows)
Cmd + Shift + R (Mac)

# Or use incognito window
# Or clear browser cache
```

#### 2. **Migrations not applied**
**Problem:** Database errors
**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 3. **Static files not loading**
**Problem:** CSS/JS not working
**Solution:**
```bash
python manage.py collectstatic
# Or set DEBUG = True in settings
```

#### 4. **Password toggle not working**
**Problem:** Eye icon doesn't toggle password
**Solution:**
- Check browser console for errors
- Verify JavaScript is enabled
- Hard refresh page (Ctrl + F5)

#### 5. **Mobile view not responsive**
**Problem:** Site doesn't adapt to mobile
**Solution:**
- Check viewport meta tag exists
- Clear browser cache
- Test in incognito mode
- Verify CSS media queries loaded

#### 6. **Document uploads fail**
**Problem:** Files don't upload
**Solution:**
- Check `MEDIA_ROOT` and `MEDIA_URL` in settings
- Verify `media/` folder exists
- Check file permissions
- Verify file size limits

---

## 📊 Database Models

### Core Models
1. **BeneficiaryCase** - Case information
2. **Asset** - Inherited assets
3. **Document** - File uploads
4. **Message** - Communication

### Configuration Models
5. **SiteSettings** - Site-wide settings (singleton)
6. **FAQ** - Help page questions
7. **MessageTemplate** - Reusable messages
8. **CaseDescriptionTemplate** - Reusable descriptions

---

## 🎨 Branding

### Colors
- **Primary:** #6B46C1 (Purple)
- **Secondary:** #4299E1 (Blue)
- **Accent:** #38B2AC (Teal)
- **Success:** #48BB78 (Green)
- **Warning:** #ED8936 (Orange)

### Typography
- **Font:** System fonts (Bootstrap 5 default)
- **Icons:** Bootstrap Icons

### Logo
- Shield check icon (bi-shield-check)
- Text: "DGLegacy" (not "DGLegacy Portal")

---

## 📞 Support

### For Beneficiaries
- **Phone:** +1 (800) 555-0199
- **Email:** support@dglegacy.com
- **Hours:** Mon-Fri, 9AM-6PM EST

### For Developers
- Check documentation files
- Review code comments
- Test with sample data
- Use Django debug toolbar

---

## 🔐 Security Notes

### Current Implementation
- ⚠️ **Passwords in plain text** (demo only)
- ✅ CSRF protection enabled
- ✅ XSS prevention
- ✅ Session-based auth
- ✅ Secure headers (WhiteNoise)

### Production Recommendations
- [ ] Hash passwords (use Django's auth system)
- [ ] Enable HTTPS
- [ ] Set secure session cookies
- [ ] Add rate limiting
- [ ] Implement 2FA
- [ ] Add email verification
- [ ] Set up proper logging
- [ ] Configure CORS properly

---

## 📝 Summary

### What's Working
✅ Beneficiary portal with dashboard, assets, documents, messages, help
✅ Admin panel with full CRUD operations
✅ Admin-configurable content (settings, FAQs, templates)
✅ Document upload tracking (admin vs beneficiary)
✅ Mobile responsive design
✅ Password visibility toggle
✅ Asset filtering and search
✅ Progress tracking and timeline
✅ Branding updated to "DGLegacy"

### Key Features
- 👥 Dual interface (beneficiary + admin)
- 📱 Fully mobile responsive
- 🎛️ Admin-configurable content
- 📄 Document management with source tracking
- 💬 Bidirectional messaging
- 📊 Progress visualization
- 🔍 Search and filter capabilities
- 🎨 Professional, trustworthy design

---

**Last Updated:** October 21, 2025
**Version:** 1.0
**Status:** Production Ready (with security improvements needed for live deployment)
