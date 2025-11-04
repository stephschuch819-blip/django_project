from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import MinLengthValidator
from django.utils.crypto import get_random_string
import uuid


class BeneficiaryCase(models.Model):
    """
    Represents a beneficiary case in the digital inheritance system.
    """
    case_number = models.CharField(
        max_length=20,
        unique=True,
        editable=False,
        help_text="Unique case identifier"
    )
    beneficiary_name = models.CharField(max_length=200)
    beneficiary_email = models.EmailField()
    beneficiary_phone = models.CharField(max_length=20, blank=True)
    
    # Authentication
    password = models.CharField(
        max_length=128,
        validators=[MinLengthValidator(8)],
        help_text="Password for beneficiary portal access"
    )
    
    # Case details
    deceased_name = models.CharField(max_length=200)
    case_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Beneficiary Case"
        verbose_name_plural = "Beneficiary Cases"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.case_number} - {self.beneficiary_name}"
    
    def save(self, *args, **kwargs):
        if not self.case_number:
            # Generate unique case number
            self.case_number = self.generate_case_number()
        
        # Hash password if it's not already hashed
        # Django hashed passwords start with algorithm identifier (e.g., 'pbkdf2_sha256$')
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        
        super().save(*args, **kwargs)
    
    def set_password(self, raw_password):
        """
        Set the password using Django's password hashing.
        Use this method when updating passwords.
        """
        self.password = make_password(raw_password)
    
    @staticmethod
    def generate_case_number():
        """Generate a unique case number in format: DG-XXXXXX"""
        while True:
            case_num = f"DG-{get_random_string(6, allowed_chars='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"
            if not BeneficiaryCase.objects.filter(case_number=case_num).exists():
                return case_num


class Asset(models.Model):
    """
    Represents an asset associated with a beneficiary case.
    """
    ASSET_TYPES = [
        ('BANK_ACCOUNT', 'Bank Account'),
        ('REAL_ESTATE', 'Real Estate'),
        ('VEHICLE', 'Vehicle'),
        ('INVESTMENT', 'Investment'),
        ('CRYPTOCURRENCY', 'Cryptocurrency'),
        ('DIGITAL_ASSET', 'Digital Asset'),
        ('PERSONAL_PROPERTY', 'Personal Property'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('UNCLAIMED', 'Unclaimed'),
        ('PROCESSING', 'Processing'),
        ('READY_FOR_TRANSFER', 'Ready'),
        ('COMPLETED', 'Completed'),
    ]
    
    case = models.ForeignKey(
        BeneficiaryCase,
        on_delete=models.CASCADE,
        related_name='assets'
    )
    asset_type = models.CharField(max_length=50, choices=ASSET_TYPES)
    description = models.TextField()
    estimated_value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Estimated value in USD"
    )
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='UNCLAIMED'
    )
    notes = models.TextField(blank=True, help_text="Internal notes (not visible to beneficiary)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Asset"
        verbose_name_plural = "Assets"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_asset_type_display()} - {self.case.case_number}"


class Document(models.Model):
    """
    Represents a document associated with a beneficiary case.
    """
    case = models.ForeignKey(
        BeneficiaryCase,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        help_text="Admin user who uploaded this (null if uploaded by beneficiary)"
    )
    uploaded_by_beneficiary = models.BooleanField(
        default=False,
        help_text="True if uploaded by beneficiary, False if uploaded by admin"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_visible_to_beneficiary = models.BooleanField(
        default=True,
        help_text="Whether this document is visible in the beneficiary portal"
    )
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.title} - {self.case.case_number}"


class Message(models.Model):
    """
    Represents a message in the internal messaging system.
    """
    case = models.ForeignKey(
        BeneficiaryCase,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender_is_beneficiary = models.BooleanField(
        default=True,
        help_text="True if sent by beneficiary, False if sent by admin"
    )
    sender_admin = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sent_messages'
    )
    subject = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']
    
    def __str__(self):
        sender = "Beneficiary" if self.sender_is_beneficiary else f"Admin ({self.sender_admin})"
        return f"{self.subject} - {sender} - {self.case.case_number}"


class SiteSettings(models.Model):
    """
    Site-wide settings that can be configured by admins.
    Only one instance should exist.
    """
    # Contact Information
    support_phone = models.CharField(
        max_length=20,
        default="+1 (800) 555-0199",
        help_text="Support phone number displayed throughout the site"
    )
    support_email = models.EmailField(
        default="support@dglegacy.com",
        help_text="Support email address"
    )
    company_address = models.TextField(
        default="123 Legacy Street, Suite 100\nNew York, NY 10001",
        help_text="Company physical address"
    )
    
    # Business Hours
    business_hours = models.CharField(
        max_length=100,
        default="Mon-Fri: 9AM - 6PM EST",
        help_text="Business operating hours"
    )
    
    # Timeline Estimates
    estimated_completion_time = models.CharField(
        max_length=50,
        default="4-12 weeks",
        help_text="Estimated time for case completion"
    )
    identity_verification_time = models.CharField(
        max_length=50,
        default="3-5 business days",
        help_text="Time for identity verification"
    )
    document_preparation_time = models.CharField(
        max_length=50,
        default="5-7 business days",
        help_text="Time for document preparation"
    )
    legal_review_time = models.CharField(
        max_length=50,
        default="2-3 business days",
        help_text="Time for legal review"
    )
    
    # Social Media Links
    facebook_url = models.URLField(blank=True, help_text="Facebook page URL")
    twitter_url = models.URLField(blank=True, help_text="Twitter profile URL")
    linkedin_url = models.URLField(blank=True, help_text="LinkedIn page URL")
    instagram_url = models.URLField(blank=True, help_text="Instagram profile URL")
    
    # Support Messages
    login_help_text = models.TextField(
        default="Your case number and password were provided by our agency.",
        help_text="Help text shown on login page"
    )
    response_time_message = models.CharField(
        max_length=200,
        default="We typically respond within 24 hours",
        help_text="Message about support response time"
    )
    
    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
    
    def __str__(self):
        return "Site Settings"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        """Get or create the single settings instance"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class FAQ(models.Model):
    """
    Frequently Asked Questions for the Help page.
    """
    question = models.CharField(max_length=500, help_text="The question")
    answer = models.TextField(help_text="The answer (HTML allowed)")
    icon = models.CharField(
        max_length=50,
        default="bi-info-circle",
        help_text="Bootstrap icon class (e.g., bi-info-circle)"
    )
    order = models.IntegerField(
        default=0,
        help_text="Display order (lower numbers appear first)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this FAQ is visible"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return self.question


class MessageTemplate(models.Model):
    """
    Pre-defined message templates for admins to use when messaging beneficiaries.
    """
    name = models.CharField(
        max_length=200,
        help_text="Template name (e.g., 'Welcome Message', 'Document Request')"
    )
    subject = models.CharField(
        max_length=200,
        help_text="Default subject line"
    )
    content = models.TextField(
        help_text="Message content. Use {{beneficiary_name}} and {{case_number}} as placeholders."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is available for use"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CaseDescriptionTemplate(models.Model):
    """
    Pre-defined case description templates for common inheritance scenarios.
    """
    name = models.CharField(
        max_length=200,
        help_text="Template name (e.g., 'Standard Inheritance', 'Complex Estate')"
    )
    description = models.TextField(
        help_text="Case description template. Use {{deceased_name}} and {{beneficiary_name}} as placeholders."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is available for use"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Case Description Template"
        verbose_name_plural = "Case Description Templates"
        ordering = ['name']
    
    def __str__(self):
        return self.name
