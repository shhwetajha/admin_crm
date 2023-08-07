from django.contrib import admin
from inverters.models import InverterModule

class InverterModuleAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "inverter_type", "manufacturer", 'product_warranty', 'rated_output_power', 'my_list']
    # list_filter = ('first_name', 'email', "phone")
    # search_fields = ('first_name', 'email', 'phone')
    exclude = ['created_by', 'created_at', 'updated_by', 'updated_at', ]
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(InverterModule, InverterModuleAdmin)