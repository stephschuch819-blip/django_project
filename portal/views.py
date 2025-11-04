from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.db.models import Sum, Count, Q
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.contrib.auth.hashers import check_password
from django_ratelimit.decorators import ratelimit
import logging
from .models import BeneficiaryCase, Asset, Document, Message
from .forms import BeneficiaryLoginForm, MessageForm, DocumentUploadForm

# Security logger for tracking suspicious access attempts
logger = logging.getLogger('portal.security')


@ratelimit(key='ip', rate='5/m', method='POST', block=True)
def beneficiary_login(request):
    """
    Login view for beneficiaries using case number and password.
    Rate limited to 5 login attempts per minute per IP address.
    """
    if request.session.get('beneficiary_case_id'):
        return redirect('beneficiary_dashboard')
    
    if request.method == 'POST':
        form = BeneficiaryLoginForm(request.POST)
        if form.is_valid():
            case_number = form.cleaned_data['case_number']
            password = form.cleaned_data['password']
            
            try:
                case = BeneficiaryCase.objects.get(
                    case_number=case_number,
                    is_active=True
                )
                
                # Secure password check using Django's password hashing
                if check_password(password, case.password):
                    # Regenerate session to prevent session fixation attacks
                    request.session.cycle_key()
                    
                    # Set session
                    request.session['beneficiary_case_id'] = case.id
                    request.session['beneficiary_name'] = case.beneficiary_name
                    
                    # Log successful login
                    logger.info(
                        f"Successful login for case {case.case_number} "
                        f"from IP {request.META.get('REMOTE_ADDR')}"
                    )
                    
                    messages.success(request, f'Welcome, {case.beneficiary_name}!')
                    return redirect('beneficiary_dashboard')
                else:
                    messages.error(request, 'Invalid case number or password.')
            except BeneficiaryCase.DoesNotExist:
                messages.error(request, 'Invalid case number or password.')
    else:
        form = BeneficiaryLoginForm()
    
    return render(request, 'portal/login.html', {'form': form})


def beneficiary_logout(request):
    """
    Logout view for beneficiaries.
    """
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('beneficiary_login')


def get_beneficiary_case(request):
    """
    Securely retrieve the beneficiary case for the current session.
    
    This function provides IDOR protection by:
    1. Validating the session contains a case_id
    2. Verifying the case exists and is active
    3. Logging suspicious access attempts
    
    Returns:
        BeneficiaryCase: The authenticated beneficiary's case
    
    Raises:
        PermissionDenied: If session is invalid or case is inactive
        Http404: If case doesn't exist
    """
    case_id = request.session.get('beneficiary_case_id')
    
    if not case_id:
        logger.warning(
            f"Unauthorized access attempt from IP {request.META.get('REMOTE_ADDR')}: "
            f"No case_id in session"
        )
        raise PermissionDenied("Invalid session. Please log in again.")
    
    try:
        case = BeneficiaryCase.objects.get(id=case_id, is_active=True)
        return case
    except BeneficiaryCase.DoesNotExist:
        logger.warning(
            f"Suspicious access attempt from IP {request.META.get('REMOTE_ADDR')}: "
            f"Session contains invalid case_id={case_id}"
        )
        # Clear the invalid session
        request.session.flush()
        raise Http404("Case not found or has been deactivated. Please log in again.")


def beneficiary_required(view_func):
    """
    Decorator to ensure beneficiary is logged in with proper authorization.
    
    This decorator provides IDOR protection by:
    1. Checking for valid session
    2. Validating case ownership through get_beneficiary_case()
    3. Handling security exceptions gracefully
    """
    def wrapper(request, *args, **kwargs):
        if not request.session.get('beneficiary_case_id'):
            messages.warning(request, 'Please log in to access this page.')
            return redirect('beneficiary_login')
        
        try:
            # Validate case ownership - this will raise exceptions if invalid
            get_beneficiary_case(request)
        except (PermissionDenied, Http404) as e:
            messages.error(request, str(e))
            return redirect('beneficiary_login')
        
        return view_func(request, *args, **kwargs)
    return wrapper


@beneficiary_required
def beneficiary_dashboard(request):
    """
    Dashboard view for beneficiaries showing assets overview.
    """
    # Use secure case retrieval with IDOR protection
    case = get_beneficiary_case(request)
    
    # Get assets with statistics
    assets = case.assets.all()
    total_value = assets.aggregate(Sum('estimated_value'))['estimated_value__sum'] or 0
    
    # Count by status
    status_counts = assets.values('status').annotate(count=Count('id'))
    
    # Get unread messages from admin
    unread_admin_messages = case.messages.filter(
        sender_is_beneficiary=False,
        is_read=False
    )
    
    # Store unread message IDs in session for notification display
    if unread_admin_messages.exists():
        # Convert datetime to string for JSON serialization
        notifications = []
        for msg in unread_admin_messages.values('id', 'subject', 'created_at'):
            notifications.append({
                'id': msg['id'],
                'subject': msg['subject'],
                'created_at': msg['created_at'].isoformat() if msg['created_at'] else None
            })
        request.session['show_message_notifications'] = notifications
    
    unread_messages = unread_admin_messages.count()
    
    # Get recent message conversations (last 3)
    recent_messages = case.messages.all()[:3]
    
    context = {
        'case': case,
        'assets': assets,
        'total_value': total_value,
        'status_counts': {item['status']: item['count'] for item in status_counts},
        'unread_messages': unread_messages,
        'recent_messages': recent_messages,
    }
    
    return render(request, 'portal/dashboard.html', context)


@beneficiary_required
def beneficiary_assets(request):
    """
    View to display all assets for the beneficiary.
    """
    # Use secure case retrieval with IDOR protection
    case = get_beneficiary_case(request)
    
    assets = case.assets.all()
    
    context = {
        'case': case,
        'assets': assets,
    }
    
    return render(request, 'portal/assets.html', context)


@beneficiary_required
def beneficiary_documents(request):
    """
    View to display and upload documents for the beneficiary.
    """
    # Use secure case retrieval with IDOR protection
    case = get_beneficiary_case(request)
    
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.case = case
            document.uploaded_by_beneficiary = True  # Mark as uploaded by beneficiary
            document.is_visible_to_beneficiary = True  # Beneficiary uploads are visible to them
            document.save()
            messages.success(request, 'Document uploaded successfully!')
            return redirect('beneficiary_documents')
    else:
        form = DocumentUploadForm()
    
    # Get all documents (both uploaded by admin and beneficiary)
    documents = case.documents.filter(is_visible_to_beneficiary=True)
    
    context = {
        'case': case,
        'documents': documents,
        'form': form,
    }
    
    return render(request, 'portal/documents.html', context)


@beneficiary_required
def beneficiary_messages(request):
    """
    View to display and send messages.
    """
    # Use secure case retrieval with IDOR protection
    case = get_beneficiary_case(request)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.case = case
            message.sender_is_beneficiary = True
            message.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('beneficiary_messages')
    else:
        form = MessageForm()
    
    # Get all messages for this case
    all_messages = case.messages.all()
    
    # Mark admin messages as read
    case.messages.filter(
        sender_is_beneficiary=False,
        is_read=False
    ).update(is_read=True)
    
    context = {
        'case': case,
        'messages': all_messages,
        'form': form,
    }
    
    return render(request, 'portal/messages.html', context)


def beneficiary_help(request):
    """
    Help and FAQ page for beneficiaries.
    """
    # No authentication required - help is available to all
    return render(request, 'portal/help.html')
