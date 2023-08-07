

from django.contrib import admin
from  batteries.models import BatteryModule
import random

class BatteryModuleAdmin(admin.ModelAdmin):
    list_display = ["code", "battery_logo","manufacturer", "my_list"]
    list_filter = ('manufacturer',)
    search_fields = ('code', 'manufacturer', )
    exclude = ['created_by', 'created_on', 'updated_by', 'updated_at']

    # exclude = ['user', 'invoice','order', 'account', 'grid_approval', 'created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(BatteryModule, BatteryModuleAdmin)