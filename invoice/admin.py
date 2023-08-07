from django.contrib import admin
from .models import Invoice, InvoiceHistory
# from grid_approval.models import GridApproval
from installation.models import Installation, InstallationDocument
from decimal import Decimal


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "name", "phone", "amount_due",'rate', 'quantity']
    list_filter = ('invoice_number', 'order')
    search_fields = ('invoice_number__username', "invoice_number__first_name", "invoice_number__last_name")
    exclude = ['invoice_number','account', 'from_address','order', 'to_address','assigned_to', 'created_by', 'created_on', 'updated_by', 'updated_at',]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            # qs.total_amount + round(Decimal((amount - ((1 / 10) * amount))), 2)
            # obj.total_amount = round(Decimal)
            obj.amount_paid=(obj.amount_paid + obj.pay) 
            obj.total_amount = obj.rate
            # obj.total_amount = (obj.rate + obj.other + obj.tax) - (obj.special_discount)
            obj.amount_due = (obj.total_amount - obj.amount_paid)
            obj.save()
            Installation.objects.filter(order=obj.order).update(payment_due=obj.amount_due)
            if (obj.pay) > 0:
                InvoiceHistory.objects.create(invoice=obj,invoice_title=obj.invoice_title, invoice_number=obj.invoice_number, 
                                        to_address=obj.to_address, from_address=obj.from_address, name=obj.name, email=obj.email, 
                                        quantity=obj.quantity, phone=obj.phone,
                                        rate=obj.rate, total_amount=obj.total_amount, 
                                        currency=obj.currency,
                                        amount_due=obj.amount_due, 
                                        amount_paid=obj.pay,status=obj.status
                                        )
            if (obj.total_amount) == (obj.amount_paid):
                obj.status = 'Paid'
            else:
                obj.status = 'Pending'
            
            obj.updated_by = request.user
            obj.pay = 0
            obj.save()
        super().save_model(request, obj, form, change)

admin.site.register(Invoice, InvoiceAdmin)

class InvoiceHistoryAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "phone", "invoice_title","total_amount","amount_paid", "payment_date",  "amount_due", 'rate', 'quantity']
    list_filter = ('invoice_number',)
    search_fields = ('invoice_number__username', "invoice_number__first_name", "invoice_number__last_name")
    exclude = ['invoice_number', 'invoice', 'order', 'from_address', 'to_address','assigned_to', 'created_by', 'created_on', 'updated_by', 'updated_at',]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(InvoiceHistory, InvoiceHistoryAdmin)