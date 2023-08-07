

from django.contrib import admin
from  module.models import Module

class ModuleAdmin(admin.ModelAdmin):
    list_display = ["code", "title", 'technology', "manufacturer", "my_list"]
    list_filter = ('manufacturer',)
    search_fields = ('code', 'manufacturer', )
    exclude = ['created_by', 'created_on', 'updated_by', 'updated_at']
    # exclude = ['user', 'grid_approval', 'order', 'created_by', 'created_on', 'updated_by', 'updated_at', "contract_status", 
    #         "grid_approval_status", "compliance_status", "noc_status",  "safety_certificate_status", 
    #         "energy_yield_report_status", "pv_site_info_status"]
    
    def save_model(self, request, obj, form, change):

        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_at = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Module, ModuleAdmin)