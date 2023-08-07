from django.contrib import admin
from account.models import Account, EmailLog, Email
from invoice.models import Invoice
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    list_display = ["order", "name", "email", "phone", "status"]
    list_filter = ('order',)
    search_fields = ('order__name',)
    exclude = ['billing_address','order', 'assigned_to','assigned_by', 'created_by', 'created_on', 'updated_by', 'updated_at',]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class EmailAdmin(admin.ModelAdmin):
    list_display = [ "from_email"]
    exclude = ["from_account"]

admin.site.register(Account, AccountAdmin)
admin.site.register(EmailLog)
admin.site.register(Email, EmailAdmin)