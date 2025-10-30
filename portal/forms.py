from django import forms
from django.core.exceptions import ValidationError
from .models import Message, Document


class BeneficiaryLoginForm(forms.Form):
    """
    Form for beneficiary login using case number and password.
    """
    case_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your case number (e.g., DG-ABC123)',
            'autocomplete': 'off'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your password'
        })
    )
    
    def clean_case_number(self):
        case_number = self.cleaned_data.get('case_number')
        return case_number.upper().strip()


class MessageForm(forms.ModelForm):
    """
    Form for beneficiaries to send messages to the agency.
    """
    class Meta:
        model = Message
        fields = ['subject', 'content']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Message subject'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Type your message here...',
                'rows': 5
            })
        }
    
    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise ValidationError('Message content must be at least 10 characters long.')
        return content


class DocumentUploadForm(forms.ModelForm):
    """
    Form for beneficiaries to upload documents.
    """
    class Meta:
        model = Document
        fields = ['title', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description (optional)',
                'rows': 3
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Limit file size to 10MB
            if file.size > 10 * 1024 * 1024:
                raise ValidationError('File size must not exceed 10MB.')
            # Check file extension
            allowed_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.jpeg', '.png', '.txt']
            file_ext = file.name[file.name.rfind('.'):].lower()
            if file_ext not in allowed_extensions:
                raise ValidationError(f'File type not allowed. Allowed types: {", ".join(allowed_extensions)}')
        return file
