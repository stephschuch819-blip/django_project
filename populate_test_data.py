import os
import sys
import django
from decimal import Decimal

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'delegacy_portal.settings')
django.setup()

from portal.models import (
    BeneficiaryCase, Asset, Document, Message, 
    SiteSettings, FAQ, MessageTemplate, CaseDescriptionTemplate
)
from django.contrib.auth.models import User

print("Creating test data...")

# Create Site Settings
site_settings = SiteSettings.load()
print(f"✓ Site Settings created/loaded")

# Create FAQs
faqs_data = [
    {
        "question": "How long does the inheritance process take?",
        "answer": "The typical inheritance process takes 4-12 weeks, depending on the complexity of the estate and required documentation.",
        "icon": "bi-clock",
        "order": 1
    },
    {
        "question": "What documents do I need to provide?",
        "answer": "You'll typically need: valid government ID, death certificate, proof of relationship to the deceased, and any will or trust documents.",
        "icon": "bi-file-text",
        "order": 2
    },
    {
        "question": "How do I track my case status?",
        "answer": "Log in to your beneficiary portal using your case number and password. Your dashboard shows real-time updates on your case status.",
        "icon": "bi-search",
        "order": 3
    },
    {
        "question": "Is my information secure?",
        "answer": "Yes, we use industry-standard encryption and security measures to protect your personal and financial information.",
        "icon": "bi-shield-check",
        "order": 4
    },
]

for faq_data in faqs_data:
    FAQ.objects.get_or_create(
        question=faq_data["question"],
        defaults=faq_data
    )
print(f"✓ Created {len(faqs_data)} FAQs")

# Create Message Templates
message_templates = [
    {
        "name": "Welcome Message",
        "subject": "Welcome to DG Legacy Portal",
        "content": "Dear {{beneficiary_name}},\n\nWelcome to the DG Legacy Portal. Your case number is {{case_number}}.\n\nWe're here to help you through this process. Please don't hesitate to reach out if you have any questions.\n\nBest regards,\nDG Legacy Team"
    },
    {
        "name": "Document Request",
        "subject": "Additional Documents Required",
        "content": "Dear {{beneficiary_name}},\n\nTo proceed with case {{case_number}}, we need additional documentation from you. Please upload the requested documents through your portal.\n\nThank you for your cooperation.\n\nBest regards,\nDG Legacy Team"
    },
    {
        "name": "Status Update",
        "subject": "Case Status Update",
        "content": "Dear {{beneficiary_name}},\n\nThis is an update regarding case {{case_number}}. We've made progress on your case and wanted to keep you informed.\n\nBest regards,\nDG Legacy Team"
    },
]

for template_data in message_templates:
    MessageTemplate.objects.get_or_create(
        name=template_data["name"],
        defaults=template_data
    )
print(f"✓ Created {len(message_templates)} Message Templates")

# Create Case Description Templates
case_templates = [
    {
        "name": "Standard Inheritance",
        "description": "{{beneficiary_name}} is the designated beneficiary for the estate of {{deceased_name}}. This case involves standard asset transfer procedures."
    },
    {
        "name": "Complex Estate",
        "description": "{{beneficiary_name}} is one of multiple beneficiaries for the estate of {{deceased_name}}. This case requires coordination with other parties and legal review."
    },
]

for template_data in case_templates:
    CaseDescriptionTemplate.objects.get_or_create(
        name=template_data["name"],
        defaults=template_data
    )
print(f"✓ Created {len(case_templates)} Case Description Templates")

# Create test beneficiary cases
cases_data = [
    {
        "beneficiary_name": "John Smith",
        "beneficiary_email": "john.smith@example.com",
        "beneficiary_phone": "+1-555-0101",
        "password": "testpass123",
        "deceased_name": "Robert Smith",
        "case_description": "Standard inheritance case involving bank accounts and real estate."
    },
    {
        "beneficiary_name": "Sarah Johnson",
        "beneficiary_email": "sarah.j@example.com",
        "beneficiary_phone": "+1-555-0102",
        "password": "testpass123",
        "deceased_name": "Mary Johnson",
        "case_description": "Complex estate with multiple asset types including investments and cryptocurrency."
    },
    {
        "beneficiary_name": "Michael Chen",
        "beneficiary_email": "m.chen@example.com",
        "beneficiary_phone": "+1-555-0103",
        "password": "testpass123",
        "deceased_name": "David Chen",
        "case_description": "Digital inheritance case focusing on online accounts and digital assets."
    },
]

created_cases = []
for case_data in cases_data:
    case, created = BeneficiaryCase.objects.get_or_create(
        beneficiary_email=case_data["beneficiary_email"],
        defaults=case_data
    )
    created_cases.append(case)
    if created:
        print(f"✓ Created case: {case.case_number} - {case.beneficiary_name}")
    else:
        print(f"  Case already exists: {case.case_number} - {case.beneficiary_name}")

# Create assets for each case
admin_user = User.objects.get(username='admin')

assets_data = [
    # Case 1 - John Smith
    [
        {"asset_type": "BANK_ACCOUNT", "description": "Chase Savings Account #1234", "estimated_value": Decimal("45000.00"), "status": "PROCESSING"},
        {"asset_type": "REAL_ESTATE", "description": "Family home at 123 Main St", "estimated_value": Decimal("350000.00"), "status": "UNCLAIMED"},
        {"asset_type": "VEHICLE", "description": "2018 Honda Accord", "estimated_value": Decimal("18000.00"), "status": "READY_FOR_TRANSFER"},
    ],
    # Case 2 - Sarah Johnson
    [
        {"asset_type": "INVESTMENT", "description": "Fidelity Investment Account", "estimated_value": Decimal("125000.00"), "status": "PROCESSING"},
        {"asset_type": "CRYPTOCURRENCY", "description": "Bitcoin Wallet", "estimated_value": Decimal("75000.00"), "status": "UNCLAIMED"},
        {"asset_type": "BANK_ACCOUNT", "description": "Bank of America Checking", "estimated_value": Decimal("12000.00"), "status": "COMPLETED"},
        {"asset_type": "PERSONAL_PROPERTY", "description": "Jewelry Collection", "estimated_value": Decimal("25000.00"), "status": "READY_FOR_TRANSFER"},
    ],
    # Case 3 - Michael Chen
    [
        {"asset_type": "DIGITAL_ASSET", "description": "Domain Portfolio (15 domains)", "estimated_value": Decimal("8500.00"), "status": "PROCESSING"},
        {"asset_type": "CRYPTOCURRENCY", "description": "Ethereum Wallet", "estimated_value": Decimal("32000.00"), "status": "UNCLAIMED"},
        {"asset_type": "BANK_ACCOUNT", "description": "Wells Fargo Savings", "estimated_value": Decimal("28000.00"), "status": "READY_FOR_TRANSFER"},
    ],
]

for i, case in enumerate(created_cases):
    for asset_data in assets_data[i]:
        asset_data['case'] = case
        Asset.objects.get_or_create(
            case=case,
            description=asset_data['description'],
            defaults=asset_data
        )
    print(f"✓ Created {len(assets_data[i])} assets for {case.beneficiary_name}")

# Create messages for each case
messages_data = [
    # Case 1 - John Smith
    [
        {
            "sender_is_beneficiary": False,
            "sender_admin": admin_user,
            "subject": "Welcome to DG Legacy",
            "content": "Welcome to the DG Legacy Portal. We're here to assist you with your inheritance case.",
            "is_read": True
        },
        {
            "sender_is_beneficiary": True,
            "subject": "Question about documents",
            "content": "Hi, I have a question about the documents I need to provide. Can you clarify?",
            "is_read": False
        },
    ],
    # Case 2 - Sarah Johnson
    [
        {
            "sender_is_beneficiary": False,
            "sender_admin": admin_user,
            "subject": "Case Status Update",
            "content": "Your case is progressing well. We've completed the verification of your bank account.",
            "is_read": True
        },
    ],
    # Case 3 - Michael Chen
    [
        {
            "sender_is_beneficiary": False,
            "sender_admin": admin_user,
            "subject": "Digital Asset Transfer",
            "content": "We're working on transferring your digital assets. This process may take 5-7 business days.",
            "is_read": False
        },
    ],
]

for i, case in enumerate(created_cases):
    for msg_data in messages_data[i]:
        msg_data['case'] = case
        Message.objects.get_or_create(
            case=case,
            subject=msg_data['subject'],
            defaults=msg_data
        )
    print(f"✓ Created {len(messages_data[i])} messages for {case.beneficiary_name}")

print("\n" + "="*60)
print("TEST DATA SUMMARY")
print("="*60)
print(f"\nSuperuser Credentials:")
print(f"  Username: admin")
print(f"  Password: admin123")
print(f"\nBeneficiary Cases Created:")
for case in created_cases:
    print(f"\n  Case Number: {case.case_number}")
    print(f"  Beneficiary: {case.beneficiary_name}")
    print(f"  Email: {case.beneficiary_email}")
    print(f"  Password: testpass123")
    print(f"  Assets: {case.assets.count()}")
    print(f"  Messages: {case.messages.count()}")

print(f"\n✓ All test data created successfully!")
print(f"\nYou can now:")
print(f"  1. Login to admin at: http://localhost:8000/admin/")
print(f"  2. Login as beneficiary at: http://localhost:8000/login/")
print("="*60)
