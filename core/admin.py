from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, AccountUser, Account, Address, CorporateContact, EpicSDKConfiguration

admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Account)
admin.site.register(AccountUser)
admin.site.register(Address)
admin.site.register(CorporateContact)
admin.site.register(EpicSDKConfiguration)
