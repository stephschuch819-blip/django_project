from .models import BeneficiaryCase


def unread_messages_count(request):
    """
    Context processor to add unread messages count to all templates.
    """
    if request.session.get('beneficiary_case_id'):
        try:
            case = BeneficiaryCase.objects.get(
                id=request.session['beneficiary_case_id'],
                is_active=True
            )
            unread_count = case.messages.filter(
                sender_is_beneficiary=False,
                is_read=False
            ).count()
            return {'unread_messages_count': unread_count}
        except BeneficiaryCase.DoesNotExist:
            pass
    return {'unread_messages_count': 0}
