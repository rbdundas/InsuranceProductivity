from .models import BillingEvent, EventType
from core.models import Account, User, AccountUser


def get_billing_event(billing_type):
    return EventType.objects.get(Type=billing_type)


def create_billing_event(account, event_type, description, user=None):
    event_type = EventType.objects.get(Type=event_type)
    if user:
        BillingEvent.objects.create(Account=account, Event=event_type, Description=description, User=user)
    else:
        BillingEvent.objects.create(Account=account, Event=event_type, Description=description)
