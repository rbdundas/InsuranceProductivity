from django.contrib import admin
from .models import BillingEvent, EventType

# Register your models here.
admin.site.register(BillingEvent)
admin.site.register(EventType)
