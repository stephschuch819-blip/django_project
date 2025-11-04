from .models import BeneficiaryCase
import logging

# Security logger
logger = logging.getLogger('portal.security')


def unread_messages_count(request):
    """
    Context processor to add unread messages count to all templates.
    
    Includes IDOR protection by:
    1. Validating session case_id exists
    2. Verifying case is active
    3. Logging suspicious access attempts
    """
    case_id = request.session.get('beneficiary_case_id')
    
    if case_id:
        try:
            case = BeneficiaryCase.objects.get(
                id=case_id,
                is_active=True
            )
            unread_count = case.messages.filter(
                sender_is_beneficiary=False,
                is_read=False
            ).count()
            return {'unread_messages_count': unread_count}
        except BeneficiaryCase.DoesNotExist:
            # Log suspicious access attempt
            logger.warning(
                f"Context processor detected invalid case_id={case_id} "
                f"from IP {request.META.get('REMOTE_ADDR')}"
            )
            # Clear invalid session
            request.session.flush()
    
    return {'unread_messages_count': 0}
