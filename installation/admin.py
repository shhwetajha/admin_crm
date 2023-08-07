from django.contrib import admin
from  installation.models import InstallationDocument, Installation, WarrantyDocument, UserReferral, ReferralSuccess

# from grid_approval.models import GridApproval

class InstallationAdmin(admin.ModelAdmin):
    list_display = ["order", "ins_booking_date","ins_completed_date", "payment_due","nmi_no","installation_status", "net_meter_status"]
    list_filter = ('order', )
    # search_fields = ('invoice__username', 'order__customer_name', )

    exclude = ['order', 'created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            if obj.ins_completed_date:
                obj.installation_status = 'Completed'
                obj.ins_status = 'Completed'
            else:
                obj.installation_status = 'Pending'
                obj.ins_status = 'Pending'
            # try:
            #     # docs = InstallationDocument.objects.get(invoice=obj, order=obj.order)
            #     docs = InstallationDocument.objects.get(invoice=obj)
            #     if docs:
            #         pass
            # except Exception as e:
            #     print(e)
            #     grid = GridApproval.objects.get(order=obj.order)
            #     print(grid)
            #     InstallationDocument.objects.create(grid_approval=grid, user=obj.user, order=obj.order, created_by=request.user)
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class InstallationDocumentAdmin(admin.ModelAdmin):
    list_display = ["order", "contract_docs","grid_approval_docs","compliance_docs", "pv_site_info_docs", 
        "energy_yield_report_docs", "safety_certificate_docs", "noc_docs"]
    # list_filter = ('order')
    # search_fields = ('order__customer_name', 'user__email',)
    exclude = ['grid_approval', 'order', 'created_by', 'created_on', 'updated_by', 'updated_at', "contract_status", 
            "grid_approval_status", "compliance_status", "noc_status",  "safety_certificate_status", 
            "energy_yield_report_status", "pv_site_info_status"]

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        elif change:
            if (obj.contract_docs):
                obj.contract_status = "Received"
            else:
                obj.contract_status = "Pending"
            if (obj.grid_approval_docs):
                obj.grid_approval_status = "Received"
            else:
                obj.grid_approval_status = "Pending"
            if (obj.compliance_docs):
                obj.compliance_status = "Received"
            else:
                obj.compliance_status = "Pending"
            if (obj.pv_site_info_docs):
                obj.pv_site_info_status = "Received"
            else:
                obj.pv_site_info_status = "Pending"
            if (obj.energy_yield_report_docs):
                obj.energy_yield_report_status = "Received"
            else:
                obj.energy_yield_report_status = "Pending"
            if (obj.safety_certificate_docs):
                obj.safety_certificate_status = "Received"
            else:
                obj.safety_certificate_status = "Pending"
            if (obj.noc_docs):
                obj.noc_status = "Received"
            else:
                obj.noc_status = "Pending"
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class WarrantyDocumentAdmin(admin.ModelAdmin):
    list_display = ["order", "panels_brands",  "panels_docs", "inverter_brands", "inverter_docs", "battery_brands", "battery_docs"]
    list_filter = ('order',)
    # search_fields = ('order__customer_name',)
    exclude = ['order', 'created_by', 'created_on', 'updated_by', 'updated_at',]

    def save_model(self, request, obj, form, change):

        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# class UserReferralAdmin(admin.ModelAdmin):
#     list_display = ["referred_by",  "first_name", "last_name", "mobile_no"]
#     list_filter = ('referred_by',)
#     search_fields = ('referred_by__email',)
#     # exclude = ['referred_by', 'created_by', 'created_on', 'updated_by', 'updated_at',]

# class ReferralSuccessAdmin(admin.ModelAdmin):
#     list_display = ["referral_by",  "referrals_made", "referrals_paid", "approval_pending"]
#     list_filter = ('referral_by',)
#     search_fields = ('referral_by__email',)


# admin.site.register(ReferralSuccess, ReferralSuccessAdmin)
# admin.site.register(UserReferral, UserReferralAdmin)
admin.site.register(Installation, InstallationAdmin)
admin.site.register(WarrantyDocument, WarrantyDocumentAdmin)
admin.site.register(InstallationDocument, InstallationDocumentAdmin)