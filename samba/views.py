from django.shortcuts import render
from . import samba_safety
from core.models import AccountTokens


def epic_to_samba_report(request):
    client_id = request.GET.get('EntityID')
    policy_id = request.GET.get('PolicyID')
    token = request.GET.get('a')
    account = AccountTokens.objects.get(Token=token).Account
    samba_safety.epic_to_samba(account, data={'PolicyID': policy_id, 'ClientID': client_id})
    context = {

    }
    return render(request, template_name='close_tab.html')
