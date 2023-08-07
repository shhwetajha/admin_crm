from django.contrib import admin
from django.utils import timezone
from order.models import Order, InstallerAvailibility, TakeAppointment, DateString, DocumentUpload, DocumentOrderUpload,InstallerHoliday
from common.models import CustomerUser


class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer_name", "company_Name", "project",  "system_Size","nmi_no", "order_status", "quotation"]
    list_filter = ('project', "nmi_no")
    search_fields = ('project', "customer_name", "nmi_no")
    exclude = ['last_login','from_address', "customer_name", "project", 'to_address', 'order_id', 'is_delete', 'is_limit', 'is_extended',  'created_at', 'updated_by', 'updated_at', ]

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        if db_field.name == "user":
                exclude_ids=Order.objects.all().values_list("user__id",flat=True)
                # kwargs["queryset"] = User.objects.filter(is_superuser=False, user_type='customer').exclude(id__in=exclude_ids)
                kwargs["queryset"] = CustomerUser.objects.filter(quote_sent=False).exclude(id__in=exclude_ids)
        return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
            cust = CustomerUser.objects.get(id=obj.user.id)
            cust.quote_sent = True
            cust.save()
            # CustomerUser.objects.filter(id=obj.user.id).update(quote_sent=True)
        elif change:
            obj.updated_by = request.user
            # obj.last_status_changed =  timezone.now()

        super().save_model(request, obj, form, change)
        

# class OrderAdmin(admin.ModelAdmin):
#     list_display = ["id","order_time", "customer_name", "project", "created_by", "system_Size","nmi_no", "order_status", "quotation"]
#     list_filter = ('project', "nmi_no")
#     search_fields = ('project', "customer_name", "nmi_no")
#     exclude = ['last_login', "customer_name", "project", 'order_id', 'is_delete', 'is_limit', 'is_extended',  'created_at', 'updated_by', 'updated_at', ]

#     # def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
#     #     if db_field.name == "user":
#     #             exclude_ids=Order.objects.all().values_list("user__id",flat=True)
#     #             # kwargs["queryset"] = User.objects.filter(is_superuser=False, user_type='customer').exclude(id__in=exclude_ids)
#     #             kwargs["queryset"] = CustomerUser.objects.filter(quote_sent=False).exclude(id__in=exclude_ids)
#     #     return super(OrderAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

#     def save_model(self, request, obj, form, change):
#         if not change:
#             obj.created_by = request.user
#             # cust = CustomerUser.objects.get(id=obj.user.id)
#             # cust.quote_sent = True
#             # cust.save()
#             # CustomerUser.objects.filter(id=obj.user.id).update(quote_sent=True)
#         elif change:
#             obj.updated_by = request.user
#             # obj.last_status_changed =  timezone.now()

#         super().save_model(request, obj, form, change)
        


class InstallerAvailibilityAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = [ "id","installer","available_start_time", "available_end_time", "created_by", ]
    # list_filter = ( )
    # search_fields = (, )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)



class HolidayAvailibilityAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = [ "id","installer","is_unavailable","reason", "created_by", ]
    # list_filter = ( )
    # search_fields = (, )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class TakeAppointmentAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = ["id",  "customer", "appointment_date", "appointment_time", "appointment_appove","approval_send",  ]
    # list_filter = ( )
    # search_fields = (, )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)



admin.site.register(DocumentOrderUpload)

class DocumentUploadAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = ["upload_type", "title", "file", "taken_from", ]
    # list_filter = ( )
    # search_fields = (, )


    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)


class DateStringAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = ["id", "date",]
    # list_filter = ( )
    # search_fields = (, )


    # def save_model(self, request, obj, form, change):
    #     if not change:
    #         obj.created_by = request.user.id

    #     elif change:
    #         obj.updated_by = request.user
    #     super().save_model(request, obj, form, change)

admin.site.register(DateString, DateStringAdmin)
admin.site.register(TakeAppointment, TakeAppointmentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(InstallerAvailibility, InstallerAvailibilityAdmin)
admin.site.register(DocumentUpload, DocumentUploadAdmin)
admin.site.register(InstallerHoliday, HolidayAvailibilityAdmin)