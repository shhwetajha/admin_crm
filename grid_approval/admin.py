from django.contrib import admin
from grid_approval.models import  GridApproval, Document, PreSiteRisk
# from import_export.admin import ImportExportModelAdmin
from account.models import Account


class GridApprovalAdmin(admin.ModelAdmin):
    list_display = [ "order", "nmi_no", "meter_date","meter_Approved_date", "grid_status","energy_provider"]
    list_filter = ("order","nmi_no","grid_status", )
    search_fields = ("order__customer_name", "nmi_no","grid_status", )
    exclude = ['grid_status', 'order',  'created_by', 'created_at', 'updated_by', 'updated_at', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            if obj.meter_Approved_date:
                obj.grid_status = 'Completed'
            else:
                obj.grid_status = 'Pending'
            # try:
            #     # docs = Account.objects.get(assigned_to=obj.user, assigned_by=request.user, billing_address=obj.order.address)
            #     docs = Account.objects.get(order=obj.order)
            #     if docs:
            #         pass
            # except Exception as e:
            #     print(e)
            #     Account.objects.create(assigned_to=obj.user, assigned_by=request.user, billing_address=obj.order.address, order=obj.order, created_by=request.user)
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class DocumentAdmin(admin.ModelAdmin):
    list_display = [ "order", "contract_file","meter_box","electricity_bill","council_rate","miscellaneous_file"]
    list_filter = ("order", )
    search_fields = ("order__customer_name", )
    exclude = [ 'order', 'address', 'contract_status',  'meter_status', 'electricity_status', 'council_status', 
                    'miscellaneous_status', 'created_by', 'created_at', 'updated_by', 'updated_at', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            if (obj.contract_file):
                obj.contract_status = 'Completed'
            else:
                obj.contract_status = 'Pending'
                # obj.save()
            if (obj.meter_box):
                print(obj.meter_box)
                obj.meter_status = 'Completed'
            else:
                obj.meter_status = 'Pending'
                # obj.save()
            if (obj.electricity_bill):
                obj.electricity_status = 'Completed'
            else:
                obj.electricity_status = 'Pending'
                # obj.save()
            if (obj.council_rate):
                obj.council_status = 'Completed'
            else:
                obj.council_status = 'Pending'
                # obj.save()
            if (obj.miscellaneous_file):
                obj.miscellaneous_status = 'Completed'
            else:
                obj.miscellaneous_status = 'Pending'
            obj.save()
            # try:
            #     # grid = GridApproval.objects.get(document=obj, presite=obj.presite, user=obj.user, order=obj.order)
            #     grid = GridApproval.objects.get(document=obj)
            #     if grid:
            #         pass
            # except Exception as e:
            #     GridApproval.objects.create(document=obj, presite=obj.presite, user=obj.user, order=obj.order, created_by=request.user)
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class PreSiteRiskAdmin(admin.ModelAdmin):
    list_display = ["order", "moss","high_tension","damaged_severley"]
    list_filter = ("order", )
    # search_fields = ( "order__customer_name", )
    exclude = ['last_login', 'order', 'created_by', 'created_at', 'updated_by', 'updated_at', ]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            # try:
            #     # docs = Document.objects.get(presite=obj, user=obj.project, order=obj.order)
            #     docs = Document.objects.get(presite=obj)
            #     if docs:
            #         pass
            # except Exception as e:
            #     print(e)
            #     Document.objects.create(presite=obj, user=obj.project, order=obj.order, created_by=request.user)

            obj.updated_by = request.user

        super().save_model(request, obj, form, change)
admin.site.register(GridApproval, GridApprovalAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(PreSiteRisk, PreSiteRiskAdmin)