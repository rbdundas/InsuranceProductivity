from django.contrib import admin
from amsforms.models import *
from django.contrib.admin.filters import SimpleListFilter


admin.site.register(AMSType)
admin.site.register(FormDefinition)
admin.site.register(AMSObjectType)
admin.site.register(AMSObjectValueDefault)
admin.site.register(FormToAMSValueMapping)
admin.site.register(JotformParameters)
admin.site.register(CognitoParameters)


class AMSObjectValueAdmin(admin.ModelAdmin):
    list_display = ['AMSObjectType', 'AMSField', 'Required']
    ordering = ['AMSObjectType']
    #list_filter = (('AMSObjectType', SimpleListFilter),)
    search_fields = ('AMSObjectType', 'AMSField')


admin.site.register(AMSObjectValue, AMSObjectValueAdmin)
