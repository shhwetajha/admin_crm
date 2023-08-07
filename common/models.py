
import datetime
import time
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

def img_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("profile_pics", hash_, filename)

# class UserManager(BaseUserManager):
    
#     def create_user(self, email, username=None, password=None):
        
#         if not email:
#             raise ValueError('Email Field is required.')

#         if not password or password is None:
#             raise ValueError("Password Field is required.")
            
#         user = self.model(
            
#             email=self.normalize_email(email)
            
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         user.username = username
#         user.save()
#         return user
        
#     def create_superuser(self, email,username=None, password=None):
        
#         if not email:
#             raise ValueError('Email Field is required.')
            
#         if not password or password is None:
#             raise ValueError("Password Field is required.")

#         if not username or username is None:
#             raise ValueError("Username Field is required.")
            
#         user = self.create_user(
#             email, username=username,
#             password=password
#         )
#         user.set_password(password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.is_active = True
#         user.is_admin = True
#         user.save(using=self._db)
#         print("user.is_staff", user.is_staff)
#         return user

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile incorrect.")


# ADMIN = '1'
#     TEAM = '2'
#     INSTALLER = '3'
#     NONE_ADMIN = '4'
#     CUSTOMER = '5'
#     USER_TYPE = (
#         (ADMIN, "Admin"), 
#         (TEAM, "Team"), 
#         (INSTALLER, "Installer"), 
#         (NONE_ADMIN, "None Admin"), 
#         (CUSTOMER, "Customer")
#         )
class  User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 'ADMIN'
    TEAM = 'TEAM'
    INSTALLER = 'INSTALLER'
    NON_ADMIN = 'NON_ADMIN'
    CUSTOMER = 'CUSTOMER'
    USER_TYPE = (
        (ADMIN, "Admin"), 
        (TEAM, "Team"), 
        (INSTALLER, "Installer"), 
        (NON_ADMIN, "Non Admin"), 
        (CUSTOMER, "Customer")
        )
    file_prepend = "users/profile_pics"
    user_type = models.CharField(max_length=50, null=True, blank=True, choices=USER_TYPE)
    username = models.CharField(max_length=100, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    password = models.CharField(_('password'), max_length=128, null=True, blank=True,)
    phone = models.CharField(validators=[phone_regex], max_length=17, null=True, unique=True)
    email = models.EmailField(null=True, blank=True, max_length=255, unique=True)
    profile_pic = models.FileField(
        max_length=1000, upload_to=img_url, null=True, blank=True
    )
    date_joined = models.DateTimeField(("date joined"), auto_now_add=True)
    pin = models.CharField(max_length=100, null=True, blank=True)
    # otp = models.CharField(max_length=100, null=True, blank=True)
    # address = models.TextField(blank=True, null=True)
    is_main = models.BooleanField(default=False)
    has_approve = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_user')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = UserManager()

    def __str__(self):
        return str(self.email)


    def get_short_name(self):
        return self.username

    def get_full_name(self):
        full_name = None
        if self.first_name or self.last_name:
            full_name = self.first_name + " " + self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-id']

class Address(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE, null=True, blank=True
    )
    address_line = models.CharField(
        _("Address"), max_length=255, blank=True, default=""
    )
    street = models.CharField(_("Street"), max_length=55, blank=True, default="")
    city = models.CharField(_("City"), max_length=255, blank=True, default="")
    state = models.CharField(_("State"), max_length=255, blank=True, default="")
    postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, default=""
    )
    country = models.CharField(max_length=255, blank=True, default="")
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_address')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_address')

    def __str__(self):
        return str(self.user)

    def get_complete_address(self):
        address = ""
        if self.address_line:
            address += self.address_line
        if self.street:
            if address:
                address += ", " + self.street
            else:
                address += self.street
        if self.city:
            if address:
                address += ", " + self.city
            else:
                address += self.city
        if self.state:
            if address:
                address += ", " + self.state
            else:
                address += self.state
        if self.postcode:
            if address:
                address += ", " + self.postcode
            else:
                address += self.postcode
        if self.country:
            if address:
                address += ", " + self.country
            else:
                address += self.country
        return address

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
    alternate_phone =  models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    department = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_sales_Manager = models.BooleanField(default=False)
    is_invoice_Manager = models.BooleanField(default=False)
    is_invoice_Executive = models.BooleanField(default=False)
    is_marketing_Manager = models.BooleanField(default=False)
    is_installation_Manager = models.BooleanField(default=False)

    is_sales_Executive = models.BooleanField(default=False)
    is_invoice_Executive = models.BooleanField(default=False)
    is_online = models.BooleanField(default=True)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_team_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_team_user')

    # objects = UserManager()

    class Meta:
        verbose_name = "Team"
        verbose_name_plural = "Teams"
        ordering = ['-id']

class InstallerUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
    alternate_phone =  models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    department = models.CharField(max_length=255, null=True, blank=True)
    ec_file = models.FileField(upload_to='job_attachment/', null=True, blank=True)
    ec_number = models.CharField(max_length=50, blank=True, null=True)
    el_file = models.FileField(upload_to='job_attachment/', null=True, blank=True)
    el_number = models.CharField(max_length=50, blank=True, null=True)
    abm_number = models.CharField(max_length=50, blank=True, null=True)
    acn_number = models.CharField(max_length=50, blank=True, null=True)
    tfn_number = models.CharField(max_length=50, blank=True, null=True)
    is_online = models.BooleanField(default=True)
    has_installer = models.BooleanField(default=False)
    has_electrician = models.BooleanField(default=False)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_installer_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_installer_user')

    # objects = UserManager()

    class Meta:
        verbose_name = "Installer User"
        verbose_name_plural = "Installer Users"
        ordering = ['-id']

    # def __str__(self):
    #     return self.ec_number


class NonAdminUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
    alternate_phone =  models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    abn_number = models.CharField(max_length=50, blank=True, null=True)
    acn_number = models.CharField(max_length=50, blank=True, null=True)
    has_customer_access = models.BooleanField(default=False)
    has_installer_access = models.BooleanField(default=False)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_non_admin_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_non_admin_user')

    # objects = UserManager()

    class Meta:
        verbose_name = "Non Admin User"
        verbose_name_plural = "Non Admin Users"
        ordering = ['-id']

class CustomerUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
    alternate_phone =  models.CharField(validators=[phone_regex], max_length=17, null=True, blank=True)
    looking_for = models.TextField(blank=True, null=True)
    project_capacity = models.CharField(max_length=255, null=True, blank=True)
    utility_bill = models.CharField(max_length=255, null=True, blank=True)
    # assign_to = models.ManyToManyField(User, blank=True, related_name='assign_to')
    supply = models.TextField(blank=True, null=True)
    roof_type = models.CharField(max_length=255, null=True, blank=True)
    floor = models.CharField(max_length=255, null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    buying_options = models.CharField(max_length=254, null=True, blank=True)
    follows_up_1 = models.TextField(blank=True, null=True)
    follows_up_2 = models.TextField(blank=True, null=True)
    quote_sent = models.BooleanField(default=False)
    created_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='create_customer_user')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey("User", on_delete=models.CASCADE, null=True, blank=True, related_name='update_customer_user')

    # objects = UserManager()

    class Meta:
        verbose_name = "Customer User"
        verbose_name_plural = "Customer Users"
        ordering = ['-id']

    def __str__(self):
        return self.admin.user.email

# class Order(models.Model):
#     company_Name = models.CharField(max_length=255, null=True, blank=True)
#     user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, null=True, blank=True, related_name='order_user')
#     admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
#     project = models.CharField(max_length=255, null=True, blank=True)
#     project_capacity = models.CharField(max_length=255, null=True, blank=True)
#     CONTRACT_STATUS = (
#         ('Signed', 'Signed'),
#         ('Unsigned', 'Unsigned')
#     )
#     from_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='from_order_address')
#     to_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='to_order_address')
#     customer_name = models.CharField(max_length=255, null=True, blank=True)
#     quotation = models.CharField(max_length=30, choices=CONTRACT_STATUS, default='Unsigned')
#     system_Size = models.CharField(max_length=255, null=True, blank=True)
#     building_Type = models.CharField(max_length=255, null=True, blank=True)
#     nmi_no = models.CharField(max_length=20, null=True, blank=True, validators=[validate_nmi_number])
#     panels_quantity = models.PositiveIntegerField(null=True, blank=True)
#     # panels = models.TextField(max_length=255, null=True, blank=True)
#     panels = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True, related_name='order_panels')
#     inverter_quantity = models.PositiveIntegerField(null=True, blank=True)
#     # inverter = models.TextField(max_length=255, null=True, blank=True)  
#     inverter = models.ForeignKey(InverterModule, on_delete=models.CASCADE, null=True, blank=True, related_name='order_inverter')
#     batteries = models.ForeignKey(BatteryModule, on_delete=models.CASCADE, null=True, blank=True, related_name='order_battery')
#     other_component = models.ManyToManyField(OtherComponent, blank=True, related_name='order_other_component')
#     monitoring_quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
#     monitoring = models.CharField(max_length=255, null=True, blank=True, default='Inbuilt Wi-Fi')
#     meter_Phase = models.CharField(max_length=20, null=True, blank=True)
#     meter_Number = models.CharField(max_length=20, null=True, blank=True)
#     order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
#     installation_Type = models.CharField(max_length=255, null=True, blank=True)
#     assign_to = models.ManyToManyField(User, blank=True, related_name='assign_to')
#     # packing_slip = models.FileField(upload_to=document_path, null=True, blank=True, max_length=5000)
#     # western_power = models.FileField(upload_to=document_path, null=True, blank=True, max_length=5000)
#     # switch_board = models.FileField(upload_to=document_path, null=True, blank=True, max_length=5000)
#     # panel_layout = models.FileField(upload_to=document_path, null=True, blank=True, max_length=5000)
#     # extras = models.ManyToManyField("DocumentUpload", upload_to=document_path, null=True, blank=True, max_length=5000)
#     order_time = models.TimeField(auto_now_add=True)
#     description = models.TextField(null=True, blank=True)
#     # is_delete = models.BooleanField(default=False)
#     is_delivered = models.BooleanField(default=False)
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_order')
#     created_at = models.DateTimeField(auto_now_add=True)
#     # is_extended = models.BooleanField(default=False)
#     # is_limit = models.BooleanField(default=False)
#     updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_order')
