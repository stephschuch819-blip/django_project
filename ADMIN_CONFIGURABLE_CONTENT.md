# Admin-Configurable Content Guide

## Overview
Admins can now modify key portal content without touching code. This makes it easy to update contact information, FAQs, timelines, and support messages.

---

## 🎛️ What Admins Can Configure

### 1. **Site Settings** (Single Instance)
**Location:** Admin Panel → Site Settings

#### **Contact Information**
- ✅ **Support Phone** - Displayed throughout site
  - Default: `+1 (800) 555-0199`
  - Used in: Footer, Help page, Login page, Dashboard
  
- ✅ **Support Email** - Main contact email
  - Default: `support@dglegacy.com`
  - Used in: Footer, Help page, Login page, Messages
  
- ✅ **Company Address** - Physical address
  - Default: `123 Legacy Street, Suite 100\nNew York, NY 10001`
  - Used in: Footer
  
- ✅ **Business Hours** - Operating hours
  - Default: `Mon-Fri: 9AM - 6PM EST`
  - Used in: Footer, Help page

#### **Timeline Estimates**
- ✅ **Estimated Completion Time** - Overall case timeline
  - Default: `4-12 weeks`
  - Used in: Dashboard progress timeline
  
- ✅ **Identity Verification Time** - Verification duration
  - Default: `3-5 business days`
  - Used in: Help page FAQ
  
- ✅ **Document Preparation Time** - Doc prep duration
  - Default: `5-7 business days`
  - Used in: Help page FAQ
  
- ✅ **Legal Review Time** - Review duration
  - Default: `2-3 business days`
  - Used in: Help page FAQ

#### **Social Media Links** (Optional)
- ✅ **Facebook URL** - Leave blank to hide
- ✅ **Twitter URL** - Leave blank to hide
- ✅ **LinkedIn URL** - Leave blank to hide
- ✅ **Instagram URL** - Leave blank to hide
- Used in: Footer (only shows if URL provided)

#### **Support Messages**
- ✅ **Login Help Text** - Message on login page
  - Default: `Your case number and password were provided by our agency.`
  - Used in: Login page
  
- ✅ **Response Time Message** - Expected response time
  - Default: `We typically respond within 24 hours`
  - Used in: Help page, Messages page

---

### 2. **FAQs** (Multiple Entries)
**Location:** Admin Panel → FAQs

Each FAQ has:
- ✅ **Question** - The FAQ question (max 500 chars)
- ✅ **Answer** - The answer (HTML allowed for formatting)
- ✅ **Icon** - Bootstrap icon class (e.g., `bi-info-circle`)
- ✅ **Order** - Display order (lower numbers first)
- ✅ **Is Active** - Show/hide this FAQ

**Default FAQs Created:**
1. What is DGLegacy and how does it work?
2. How long does the process take?
3. What documents do I need to provide?
4. What do the asset statuses mean?
5. Is my information secure?
6. How do I contact support?

**Admin Can:**
- ✏️ Edit existing FAQs
- ➕ Add new FAQs
- 🗑️ Delete FAQs
- 👁️ Show/hide FAQs (toggle Is Active)
- 🔢 Reorder FAQs (change Order number)
- 🎨 Change icons (any Bootstrap icon)

---

## 🚀 How to Use

### **Initial Setup**
```bash
python manage.py setup_site_settings
```
This creates:
- Site Settings with default values
- 6 default FAQs

### **Accessing Admin Panel**
1. Go to: `http://localhost:8000/admin/`
2. Login with admin credentials
3. Look for:
   - **Site Settings** - Click to edit
   - **FAQs** - List of all FAQs

### **Editing Site Settings**
1. Click **Site Settings** in admin
2. Modify any field
3. Click **Save**
4. Changes appear immediately on site

### **Managing FAQs**
1. Click **FAQs** in admin
2. To edit: Click a FAQ
3. To add: Click **Add FAQ** button
4. To reorder: Change Order numbers
5. To hide: Uncheck **Is Active**
6. Click **Save**

---

## 📍 Where Content Appears

### **Support Phone**
- Footer (clickable link)
- Help page sidebar
- Login page
- Dashboard Next Steps card
- Help page FAQs

### **Support Email**
- Footer (clickable link)
- Help page sidebar
- Login page
- Help page FAQs

### **Company Address**
- Footer only

### **Business Hours**
- Footer
- Help page sidebar

### **Timeline Estimates**
- Dashboard progress timeline
- Help page "How long does the process take?" FAQ

### **Social Media Links**
- Footer (only if URLs provided)

### **Login Help Text**
- Login page below password field

### **Response Time Message**
- Help page sidebar
- Help page "How do I contact support?" FAQ

### **FAQs**
- Help page accordion
- Ordered by Order field
- Only active FAQs shown

---

## ❌ What's NOT Admin-Configurable

These require code changes:
- **Color scheme** - Requires CSS knowledge
- **Page layouts** - Requires HTML knowledge
- **Asset statuses** - Tied to business logic
- **Workflow stages** - Part of core functionality
- **Security badges** - Static trust indicators
- **Navigation structure** - Requires URL configuration

---

## 💡 Best Practices

### **Contact Information**
- ✅ Keep phone/email consistent across all platforms
- ✅ Test phone links work (click to call)
- ✅ Test email links work (opens email client)
- ✅ Update business hours for holidays

### **Timeline Estimates**
- ✅ Be realistic with estimates
- ✅ Update based on actual performance
- ✅ Consider adding ranges (e.g., "3-5 days")
- ✅ Explain factors that affect timing

### **FAQs**
- ✅ Keep answers concise but complete
- ✅ Use HTML for formatting (lists, bold, links)
- ✅ Order by importance (most asked first)
- ✅ Review and update regularly
- ✅ Use clear, simple language
- ✅ Choose appropriate icons

### **Social Media**
- ✅ Only add links to active accounts
- ✅ Test links before saving
- ✅ Leave blank if not using social media

---

## 🔧 Technical Details

### **Models**
```python
# Only ONE instance allowed
SiteSettings.objects.get(pk=1)

# Multiple FAQs
FAQ.objects.filter(is_active=True).order_by('order')
```

### **In Templates**
```django
{% load static %}
{{ settings.support_phone }}
{{ settings.support_email }}
{{ settings.estimated_completion_time }}

{% for faq in faqs %}
    {{ faq.question }}
    {{ faq.answer|safe }}
{% endfor %}
```

### **Database Tables**
- `portal_sitesettings` - Single row (pk=1)
- `portal_faq` - Multiple rows

---

## 📝 Example Workflow

### **Scenario: Update Phone Number**
1. Go to Admin → Site Settings
2. Change `support_phone` to new number
3. Click Save
4. New number appears in:
   - Footer
   - Help page
   - Login page
   - Dashboard

### **Scenario: Add New FAQ**
1. Go to Admin → FAQs
2. Click "Add FAQ"
3. Fill in:
   - Question: "Can I track my case progress?"
   - Answer: "Yes! Check your dashboard..."
   - Icon: `bi-graph-up`
   - Order: `7`
   - Is Active: ✓
4. Click Save
5. New FAQ appears on Help page

### **Scenario: Temporarily Hide FAQ**
1. Go to Admin → FAQs
2. Find the FAQ
3. Uncheck "Is Active"
4. Click Save
5. FAQ hidden from Help page (but not deleted)

---

## 🎯 Summary

**What Admins Control:**
- ✅ All contact information
- ✅ All timeline estimates
- ✅ All support messages
- ✅ All FAQs (add/edit/delete/reorder)
- ✅ Social media links

**Benefits:**
- 🚀 No code changes needed
- ⚡ Instant updates
- 👥 Non-technical admins can manage
- 📝 Easy to maintain
- 🔄 Reversible changes

**Next Steps:**
1. Run `python manage.py setup_site_settings` (if not done)
2. Login to admin panel
3. Customize Site Settings
4. Review and edit FAQs
5. Test changes on site

---

**Need to add more configurable content?** Contact the development team to add new fields to SiteSettings or create new models.
