from django.core.management.base import BaseCommand
from portal.models import SiteSettings, FAQ


class Command(BaseCommand):
    help = 'Initialize site settings and default FAQs'

    def handle(self, *args, **options):
        # Create or get site settings
        settings, created = SiteSettings.objects.get_or_create(pk=1)
        if created:
            self.stdout.write(self.style.SUCCESS('[OK] Site settings created with default values'))
        else:
            self.stdout.write(self.style.WARNING('Site settings already exist'))
        
        # Create default FAQs if none exist
        if not FAQ.objects.exists():
            faqs = [
                {
                    'question': 'What is DGLegacy and how does it work?',
                    'answer': '''<p>DGLegacy is a digital inheritance platform that helps beneficiaries claim their rightful inheritance. Here's how it works:</p>
<ol>
    <li><strong>Asset Owner Setup:</strong> The deceased used DGLegacy to catalog their assets and designate beneficiaries</li>
    <li><strong>HeartBeat Detection:</strong> DGLegacy's system detected an unforeseen event</li>
    <li><strong>Beneficiary Notification:</strong> You were notified and given access to this portal</li>
    <li><strong>Verification Process:</strong> We verify your identity and prepare legal documentation</li>
    <li><strong>Legal Assistance:</strong> We provide lawyers to help you claim your inheritance</li>
</ol>
<p class="mb-0"><strong>Important:</strong> DGLegacy does NOT have direct access to your assets. We help you claim them from the institutions that hold them.</p>''',
                    'icon': 'bi-info-circle',
                    'order': 1
                },
                {
                    'question': 'How long does the process take?',
                    'answer': '''<p>The timeline varies depending on several factors, but here's a typical breakdown:</p>
<ul>
    <li><strong>Identity Verification:</strong> 3-5 business days</li>
    <li><strong>Document Preparation:</strong> 5-7 business days</li>
    <li><strong>Legal Review:</strong> 2-3 business days</li>
    <li><strong>Asset Claiming:</strong> Varies by institution (2-8 weeks)</li>
</ul>
<p class="mb-0"><strong>Total estimated time:</strong> 4-12 weeks depending on complexity and institution response times.</p>''',
                    'icon': 'bi-clock',
                    'order': 2
                },
                {
                    'question': 'What documents do I need to provide?',
                    'answer': '''<p>To verify your identity and process your claim, you'll typically need:</p>
<ul>
    <li><strong>Government-issued ID:</strong> Driver's license, passport, or state ID</li>
    <li><strong>Proof of Relationship:</strong> Birth certificate, marriage certificate, or legal documents</li>
    <li><strong>Death Certificate:</strong> Official death certificate of the deceased (if available)</li>
    <li><strong>Proof of Address:</strong> Utility bill or bank statement (within last 3 months)</li>
    <li><strong>Additional Documents:</strong> May vary by asset type and institution</li>
</ul>
<p class="mb-0">Upload documents securely through the Documents page.</p>''',
                    'icon': 'bi-file-earmark-text',
                    'order': 3
                },
                {
                    'question': 'What do the asset statuses mean?',
                    'answer': '''<div class="mb-3">
    <span class="badge bg-secondary">Unclaimed</span>
    <p class="mt-2 mb-0">Asset has been identified but the claiming process hasn't started yet.</p>
</div>
<div class="mb-3">
    <span class="badge bg-primary">Processing</span>
    <p class="mt-2 mb-0">We're verifying your identity and preparing legal documentation for this asset.</p>
</div>
<div class="mb-3">
    <span class="badge bg-warning text-dark">Ready</span>
    <p class="mt-2 mb-0">Verification complete! Legal assistance will be provided to help you claim this asset.</p>
</div>
<div class="mb-0">
    <span class="badge bg-success">Completed</span>
    <p class="mt-2 mb-0">You have successfully claimed this asset with our assistance!</p>
</div>''',
                    'icon': 'bi-bar-chart',
                    'order': 4
                },
                {
                    'question': 'Is my information secure?',
                    'answer': '''<p>Yes! We take security very seriously:</p>
<ul>
    <li><strong>Encryption:</strong> All data is encrypted in transit and at rest</li>
    <li><strong>Secure Storage:</strong> Documents are stored in secure, encrypted servers</li>
    <li><strong>Access Control:</strong> Only authorized personnel can access your case</li>
    <li><strong>Compliance:</strong> We comply with all relevant data protection regulations</li>
    <li><strong>Regular Audits:</strong> Our security measures are regularly audited</li>
</ul>
<p class="mb-0">Your privacy and security are our top priorities.</p>''',
                    'icon': 'bi-shield-check',
                    'order': 5
                },
                {
                    'question': 'How do I contact support?',
                    'answer': '''<p>We're here to help! You can reach us through multiple channels:</p>
<ul>
    <li><strong>Portal Messages:</strong> Send us a secure message (response within 24 hours)</li>
    <li><strong>Phone:</strong> +1 (800) 555-0199 (Mon-Fri, 9AM-6PM EST)</li>
    <li><strong>Email:</strong> support@dglegacy.com</li>
    <li><strong>Emergency:</strong> For urgent matters, call and select option 1</li>
</ul>
<p class="mb-0">Our support team typically responds within 24 hours on business days.</p>''',
                    'icon': 'bi-headset',
                    'order': 6
                },
            ]
            
            for faq_data in faqs:
                FAQ.objects.create(**faq_data)
            
            self.stdout.write(self.style.SUCCESS(f'[OK] Created {len(faqs)} default FAQs'))
        else:
            self.stdout.write(self.style.WARNING(f'FAQs already exist ({FAQ.objects.count()} total)'))
        
        self.stdout.write(self.style.SUCCESS('\n[OK] Setup complete!'))
        self.stdout.write(self.style.SUCCESS('  - Site Settings: Ready for admin configuration'))
        self.stdout.write(self.style.SUCCESS('  - FAQs: Ready for admin editing'))
        self.stdout.write(self.style.SUCCESS('\nGo to /admin/ to customize these settings.'))
