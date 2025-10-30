from django.contrib import admin
from django.utils.html import format_html
from .models import BeneficiaryCase, Asset, Document, Message, SiteSettings, FAQ, MessageTemplate, CaseDescriptionTemplate


class AssetInline(admin.TabularInline):
    """Inline admin for assets within BeneficiaryCase."""
    model = Asset
    extra = 1
    fields = ['asset_type', 'description', 'estimated_value', 'status']
    classes = ['collapse']


class DocumentInline(admin.TabularInline):
    """Inline admin for documents within BeneficiaryCase."""
    model = Document
    extra = 0
    fields = ['title', 'file', 'is_visible_to_beneficiary']
    readonly_fields = ['uploaded_at']
    classes = ['collapse']


class MessageInline(admin.TabularInline):
    """Inline admin for messages within BeneficiaryCase."""
    model = Message
    extra = 0
    fields = ['subject', 'content', 'sender_is_beneficiary', 'is_read']
    readonly_fields = ['created_at']
    classes = ['collapse']


@admin.register(BeneficiaryCase)
class BeneficiaryCaseAdmin(admin.ModelAdmin):
    """
    Custom admin interface for BeneficiaryCase model.
    """
    list_display = [
        'case_number',
        'beneficiary_name',
        'beneficiary_email',
        'deceased_name',
        'asset_count',
        'is_active',
        'created_at'
    ]
    list_filter = ['is_active', 'created_at']
    search_fields = [
        'case_number',
        'beneficiary_name',
        'beneficiary_email',
        'deceased_name'
    ]
    readonly_fields = ['case_number', 'created_at', 'updated_at']
    inlines = [AssetInline, DocumentInline, MessageInline]
    
    fieldsets = (
        ('Case Information', {
            'fields': ('case_number', 'deceased_name', 'case_description', 'is_active')
        }),
        ('Beneficiary Details', {
            'fields': ('beneficiary_name', 'beneficiary_email', 'beneficiary_phone')
        }),
        ('Authentication', {
            'fields': ('password',),
            'description': 'Set a secure password for beneficiary portal access (min 8 characters)'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def asset_count(self, obj):
        count = obj.assets.count()
        return format_html('<strong>{}</strong>', count)
    asset_count.short_description = 'Assets'
    
    def save_model(self, request, obj, form, change):
        """Override to handle password properly"""
        super().save_model(request, obj, form, change)


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Asset model.
    """
    list_display = [
        'case',
        'asset_type',
        'description_short',
        'estimated_value',
        'status_badge',
        'updated_at'
    ]
    list_filter = ['asset_type', 'status', 'created_at']
    search_fields = ['case__case_number', 'case__beneficiary_name', 'description']
    
    fieldsets = (
        ('Case Association', {
            'fields': ('case',)
        }),
        ('Asset Details', {
            'fields': ('asset_type', 'description', 'estimated_value')
        }),
        ('Status Management', {
            'fields': ('status',),
            'description': 'Workflow: Unclaimed → Processing → Ready → Completed. Note: DGLegacy verifies beneficiaries and provides legal assistance to help them claim their inheritance.'
        }),
        ('Internal Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def status_badge(self, obj):
        colors = {
            'UNCLAIMED': '#6c757d',
            'PROCESSING': '#0d6efd',
            'READY_FOR_TRANSFER': '#ffc107',
            'COMPLETED': '#198754',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Document model.
    """
    list_display = [
        'title',
        'case',
        'uploader_display',
        'is_visible_to_beneficiary',
        'uploaded_at'
    ]
    list_filter = ['uploaded_by_beneficiary', 'is_visible_to_beneficiary', 'uploaded_at']
    search_fields = ['title', 'case__case_number', 'case__beneficiary_name']
    readonly_fields = ['uploaded_at', 'uploaded_by_beneficiary']
    
    fieldsets = (
        ('Document Information', {
            'fields': ('case', 'title', 'description', 'file')
        }),
        ('Visibility', {
            'fields': ('is_visible_to_beneficiary',),
            'description': 'Control whether beneficiaries can see this document'
        }),
        ('Metadata', {
            'fields': ('uploaded_by', 'uploaded_by_beneficiary', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def uploader_display(self, obj):
        """Show who uploaded the document with color coding"""
        if obj.uploaded_by_beneficiary:
            return format_html(
                '<span style="color: #0d6efd; font-weight: 600;"><i class="bi bi-person"></i> Beneficiary</span>'
            )
        elif obj.uploaded_by:
            return format_html(
                '<span style="color: #198754;"><i class="bi bi-shield-check"></i> Admin ({})</span>',
                obj.uploaded_by.username
            )
        else:
            return format_html('<span style="color: #6c757d;">Unknown</span>')
    uploader_display.short_description = 'Uploaded By'
    
    def save_model(self, request, obj, form, change):
        """Auto-set uploaded_by to current user if admin uploads"""
        if not change and not obj.uploaded_by_beneficiary:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Custom admin interface for Message model.
    """
    list_display = [
        'subject',
        'case',
        'sender_display',
        'is_read',
        'created_at'
    ]
    list_filter = ['sender_is_beneficiary', 'is_read', 'created_at']
    search_fields = ['subject', 'content', 'case__case_number', 'case__beneficiary_name']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Message Details', {
            'fields': ('case', 'subject', 'content')
        }),
        ('Sender Information', {
            'fields': ('sender_is_beneficiary', 'sender_admin'),
            'description': 'If sender is beneficiary, leave sender_admin blank'
        }),
        ('Status', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def sender_display(self, obj):
        if obj.sender_is_beneficiary:
            return format_html('<span style="color: #0d6efd;">Beneficiary</span>')
        else:
            admin_name = obj.sender_admin.username if obj.sender_admin else 'Unknown'
            return format_html('<span style="color: #198754;">Admin ({})</span>', admin_name)
    sender_display.short_description = 'Sender'
    
    def save_model(self, request, obj, form, change):
        """Auto-set sender_admin if not beneficiary"""
        if not obj.sender_is_beneficiary and not obj.sender_admin:
            obj.sender_admin = request.user
        super().save_model(request, obj, form, change)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin interface for site-wide settings.
    Only one instance should exist.
    """
    fieldsets = (
        ('Contact Information', {
            'fields': ('support_phone', 'support_email', 'company_address', 'business_hours'),
            'description': 'Contact details displayed throughout the site'
        }),
        ('Timeline Estimates', {
            'fields': (
                'estimated_completion_time',
                'identity_verification_time',
                'document_preparation_time',
                'legal_review_time'
            ),
            'description': 'Time estimates shown to beneficiaries'
        }),
        ('Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'linkedin_url', 'instagram_url'),
            'classes': ('collapse',),
            'description': 'Social media profile URLs (leave blank to hide)'
        }),
        ('Support Messages', {
            'fields': ('login_help_text', 'response_time_message'),
            'description': 'Help text and messages shown to users'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    """
    Admin interface for FAQs.
    """
    list_display = ['question', 'icon', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Question & Answer', {
            'fields': ('question', 'answer'),
            'description': 'HTML is allowed in the answer field'
        }),
        ('Display Settings', {
            'fields': ('icon', 'order', 'is_active'),
            'description': 'Icon: Bootstrap icon class (e.g., bi-info-circle). Order: Lower numbers appear first.'
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for message templates.
    """
    list_display = ['name', 'subject', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'subject', 'content']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'subject', 'content'),
            'description': 'Use {{beneficiary_name}} and {{case_number}} as placeholders in the content.'
        }),
        ('Settings', {
            'fields': ('is_active',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CaseDescriptionTemplate)
class CaseDescriptionTemplateAdmin(admin.ModelAdmin):
    """
    Admin interface for case description templates.
    """
    list_display = ['name', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Template Information', {
            'fields': ('name', 'description'),
            'description': 'Use {{deceased_name}} and {{beneficiary_name}} as placeholders in the description.'
        }),
        ('Settings', {
            'fields': ('is_active',),
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']


# Customize admin site header and title
admin.site.site_header = "DGLegacy Administration"
admin.site.site_title = "DGLegacy Admin"
admin.site.index_title = "Welcome to DGLegacy Admin"
