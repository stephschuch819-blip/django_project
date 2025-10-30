from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from portal.models import BeneficiaryCase, Asset, Document, Message
from decimal import Decimal


class Command(BaseCommand):
    help = 'Creates sample data for testing the Delegacy Portal'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Creating sample data...'))
        
        # Create admin user if doesn't exist
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@delegacy.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f'Created admin user: admin / admin123'))
        
        # Create sample beneficiary cases
        cases_data = [
            {
                'beneficiary_name': 'John Smith',
                'beneficiary_email': 'john.smith@example.com',
                'beneficiary_phone': '+1-555-0101',
                'password': 'password123',
                'deceased_name': 'Mary Smith',
                'case_description': 'Estate of Mary Smith including real estate and financial assets.',
            },
            {
                'beneficiary_name': 'Sarah Johnson',
                'beneficiary_email': 'sarah.j@example.com',
                'beneficiary_phone': '+1-555-0102',
                'password': 'password123',
                'deceased_name': 'Robert Johnson',
                'case_description': 'Digital and physical assets from Robert Johnson estate.',
            },
            {
                'beneficiary_name': 'Michael Brown',
                'beneficiary_email': 'mbrown@example.com',
                'beneficiary_phone': '+1-555-0103',
                'password': 'password123',
                'deceased_name': 'Elizabeth Brown',
                'case_description': 'Investment portfolio and personal property.',
            },
        ]
        
        for case_data in cases_data:
            case, created = BeneficiaryCase.objects.get_or_create(
                beneficiary_email=case_data['beneficiary_email'],
                defaults=case_data
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created case: {case.case_number} - {case.beneficiary_name}'))
                
                # Create sample assets for each case
                assets_data = [
                    {
                        'asset_type': 'BANK_ACCOUNT',
                        'description': 'Chase Bank Savings Account #****1234',
                        'estimated_value': Decimal('45000.00'),
                        'status': 'PROCESSING',
                    },
                    {
                        'asset_type': 'REAL_ESTATE',
                        'description': '123 Main Street, Springfield - 3 bedroom house',
                        'estimated_value': Decimal('350000.00'),
                        'status': 'UNCLAIMED',
                    },
                    {
                        'asset_type': 'INVESTMENT',
                        'description': 'Vanguard Investment Portfolio',
                        'estimated_value': Decimal('125000.00'),
                        'status': 'READY_FOR_TRANSFER',
                    },
                    {
                        'asset_type': 'VEHICLE',
                        'description': '2020 Toyota Camry - VIN: 1234567890',
                        'estimated_value': Decimal('22000.00'),
                        'status': 'COMPLETED',
                    },
                ]
                
                for asset_data in assets_data:
                    asset = Asset.objects.create(case=case, **asset_data)
                    self.stdout.write(f'  - Created asset: {asset.get_asset_type_display()}')
                
                # Create sample messages
                Message.objects.create(
                    case=case,
                    sender_is_beneficiary=True,
                    subject='Question about asset transfer',
                    content='Hello, I would like to know more about the timeline for transferring the bank account. Thank you.',
                    is_read=True,
                )
                
                Message.objects.create(
                    case=case,
                    sender_is_beneficiary=False,
                    sender_admin=admin_user,
                    subject='RE: Question about asset transfer',
                    content='Thank you for your inquiry. The bank account transfer is currently in processing and should be completed within 2-3 weeks. We will notify you once it moves to the next stage.',
                    is_read=False,
                )
                
                self.stdout.write(f'  - Created sample messages')
        
        self.stdout.write(self.style.SUCCESS('\n=== Sample Data Created Successfully ==='))
        self.stdout.write(self.style.SUCCESS('\nBeneficiary Login Credentials:'))
        self.stdout.write('All beneficiaries use password: password123')
        self.stdout.write('\nCase Numbers:')
        for case in BeneficiaryCase.objects.all():
            self.stdout.write(f'  - {case.case_number}: {case.beneficiary_name} ({case.beneficiary_email})')
        
        self.stdout.write(self.style.SUCCESS('\nAdmin Login:'))
        self.stdout.write('  Username: admin')
        self.stdout.write('  Password: admin123')
        self.stdout.write(self.style.SUCCESS('\nAccess the portal at: http://localhost:8000/'))
        self.stdout.write(self.style.SUCCESS('Access the admin at: http://localhost:8000/admin/'))
