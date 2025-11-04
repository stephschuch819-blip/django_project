"""
Management command to hash existing plain text passwords in the database.
Run this once after implementing password hashing.

Usage: python manage.py hash_passwords
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from portal.models import BeneficiaryCase


class Command(BaseCommand):
    help = 'Hash all plain text passwords in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made'))
        
        # Find all cases with plain text passwords
        all_cases = BeneficiaryCase.objects.all()
        hashed_count = 0
        already_hashed_count = 0
        
        for case in all_cases:
            # Check if password is already hashed
            if case.password.startswith('pbkdf2_sha256$'):
                already_hashed_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'[OK] Case {case.case_number} already has hashed password')
                )
            else:
                # Password is plain text, needs hashing
                if dry_run:
                    self.stdout.write(
                        self.style.WARNING(f'Would hash password for case {case.case_number}')
                    )
                else:
                    old_password = case.password
                    case.password = make_password(old_password)
                    case.save()
                    self.stdout.write(
                        self.style.SUCCESS(f'[OK] Hashed password for case {case.case_number}')
                    )
                hashed_count += 1
        
        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'Total cases: {all_cases.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Already hashed: {already_hashed_count}'))
        self.stdout.write(self.style.SUCCESS(f'Newly hashed: {hashed_count}'))
        
        if dry_run:
            self.stdout.write('\n' + self.style.WARNING('DRY RUN - No changes were made'))
            self.stdout.write(self.style.WARNING('Run without --dry-run to apply changes'))
        else:
            self.stdout.write('\n' + self.style.SUCCESS('Password hashing complete!'))
