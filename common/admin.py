from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import NonAdminUser, InstallerUser, User, Team, Address, CustomerUser
from django.contrib.auth.models import Group
import random
from django.db.models import Q
from django.contrib.auth.hashers import make_password
admin.site.unregister(Group)

# admin.site.register(User)
# admin.site.register(CustomerUser)

# admin.site.register(Team)

class UserAdmin(admin.ModelAdmin):

    list_display = ["id", "user_type", "email", "created_by", "username", 'pin', "phone", 'is_superuser']
    list_filter = ( "user_type", 'email')
    search_fields = ('username', 'email', 'phone')
    exclude = ['last_login','username', 'password','pin', 'date_joined', 'is_superuser', 'groups',  'user_permissions', 'created_by', 'created_at', 'updated_by', 'updated_at']

    def save_model(self, request, obj, form, change):
        if not change:
            # while True:
            #     uid  = str(random.randint(10000000, 99999999))
            #     username = 'SR' + uid
            #     try:
            #         user = User.objects.filter(username=username)
            #         if user.exists() == False:
            #             username = username
            #             break
            #     except Exception as e:
            #         continue
            # _pass = str(random.randint(100000, 999999))
            obj.created_by = request.user
            
            # obj.username = username
            # obj.password = make_password(_pass)
            # obj.make_password(_pass)
            # obj.pin = _pass
        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class CustomerUserAdmin(admin.ModelAdmin):
    list_display = ["id", "project_capacity","buying_options", "utility_bill", "quote_sent", "supply", "roof_type", "floor",]
    # list_filter = ( , "admin__phone")
    # search_fields = ( , 'admin__phone')
    # def formfield_for_manytomany(self, db_field, request=None, **kwargs):
    #     if db_field.name == "user":
    #             exclude_ids=User.objects.all().values_list("user__id",flat=True)
    #             # kwargs["queryset"] = User.objects.filter(is_superuser=False, user_type='customer').exclude(id__in=exclude_ids)
    #             kwargs["queryset"] = User.objects.filter(user_type="ADMIN").exclude(id__in=exclude_ids)
    #     return super(CustomerUserAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)
        
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'other' database.
        if db_field.name == "assign_to":
            exclude_ids=User.objects.filter(is_superuser=False, user_type__in=['NON_ADMIN', 'CUSTOMER']).values_list("id",flat=True)
            # print("exclude_ids" *10, exclude_ids)
            # print(User.objects.filter(is_superuser=False, user_type__in=['TEAM', 'INSTALLER']).only())
            kwargs["queryset"] = User.objects.filter(is_superuser=False).exclude(id__in=exclude_ids)
        return super(CustomerUserAdmin, self).formfield_for_manytomany(
            db_field, request, **kwargs
        )
    
class TeamAdmin(admin.ModelAdmin):
    # list_display = ["id", "admin", "alternate_phone", "department", "is_online", ]
    list_display = ["admin", "alternate_phone", "department", "is_online", ]
    # list_filter = ( )
    # search_fields = (, )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user.id

        elif change:
            obj.updated_by = request.user.id
        super().save_model(request, obj, form, change)

class NonAdminUserAdmin(admin.ModelAdmin):
    list_display = ["admin", "company_name", "alternate_phone", ]
    # list_display = ["id","admin",]
    # list_filter = ( )
    # search_fields = (, )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class InstallerUserAdmin(admin.ModelAdmin):
    list_display = ["id", "admin", "alternate_phone", "department", "ec_number", "el_number", "abm_number", "tfn_number" , "acn_number"]
    # list_filter = ( )
    # search_fields = (, )

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

class AddressAdmin(admin.ModelAdmin):
    list_display = ["user","address_line","street","city", "state", "postcode", "country"]
    list_filter = ('user', 'address_line', "city")
    search_fields = ('user__username', 'address_line', "city")
    exclude = ['created_by', 'created_at', 'updated_by', 'updated_at', ]

    def save_model(self, request, obj, form, change):

        if not change:
            obj.created_by = request.user

        elif change:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(CustomerUser, CustomerUserAdmin)
admin.site.register(NonAdminUser, NonAdminUserAdmin)
admin.site.register(InstallerUser, InstallerUserAdmin)