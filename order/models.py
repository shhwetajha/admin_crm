from django.db import models
from common.models import User, Address, InstallerUser, CustomerUser
import time
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from module.models import Module
from inverters.models import InverterModule
from batteries.models import BatteryModule
from other_component.models import OtherComponent
from django.urls import reverse

def validate_nmi_number(value):
    if ((len(value)) <= 8) or ((len(value)) >= 20):
        raise ValidationError(
            _('%(value)s is not a valid nmi_number number.'),
            params={'value': value},
        )

STATUS_CHOICES = (
		('Pending', 'Pending'),
		('Completed', 'Completed'),
	)
def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)

class DocumentOrderUpload(models.Model):
    # title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        max_length=1000, upload_to="installation_docs/", null=True, blank=True
    )

    def __str__(self):
        return f"{self.pk}"
    
    @property
    def filename(self):
        name = self.file.name.split("/")[1].replace('_',' ').replace('-',' ')
        return name
    def get_absolute_url(self):
        return reverse('myapp:document-detail', kwargs={'pk': self.pk})

class Order(models.Model):
    company_Name = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, null=True, blank=True, related_name='order_user')
    # admin = models.OneToOneField(Address, on_delete = models.CASCADE, null=True)
    project = models.CharField(max_length=255, null=True, blank=True)
    # project_capacity = models.CharField(max_length=255, null=True, blank=True)
    CONTRACT_STATUS = (
        ('Signed', 'Signed'),
        ('Unsigned', 'Unsigned')
    )
    from_address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='from_order_address')
    to_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True, related_name='to_order_address')
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    quotation = models.CharField(max_length=30, choices=CONTRACT_STATUS, default='Unsigned')
    system_Size = models.CharField(max_length=255, null=True, blank=True)
    building_Type = models.CharField(max_length=255, null=True, blank=True)
    nmi_no = models.CharField(max_length=20, null=True, blank=True, validators=[validate_nmi_number])
    panels_quantity = models.PositiveIntegerField(null=True, blank=True)
    # panels = models.TextField(max_length=255, null=True, blank=True)
    panels = models.ForeignKey(Module, on_delete=models.CASCADE, null=True, blank=True, related_name='order_panels')
    inverter_quantity = models.PositiveIntegerField(null=True, blank=True)
    # inverter = models.TextField(max_length=255, null=True, blank=True)  
    inverter = models.ForeignKey(InverterModule, on_delete=models.CASCADE, null=True, blank=True, related_name='order_inverter')
    batteries = models.ForeignKey(BatteryModule, on_delete=models.CASCADE, null=True, blank=True, related_name='order_battery')
    other_component = models.ManyToManyField(OtherComponent, blank=True, related_name='order_other_component')
    monitoring_quantity = models.PositiveIntegerField(default=1, null=True, blank=True)
    monitoring = models.CharField(max_length=255, null=True, blank=True, default='Inbuilt Wi-Fi')
    meter_Phase = models.CharField(max_length=20, null=True, blank=True)
    meter_Number = models.CharField(max_length=20, null=True, blank=True)
    order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    installation_Type = models.CharField(max_length=255, null=True, blank=True)
    assign_to = models.ManyToManyField(User, blank=True, related_name='assign_to')
    packing_slip = models.ManyToManyField(DocumentOrderUpload, blank=True, related_name='packing_slip')
    western_power = models.ManyToManyField(DocumentOrderUpload, blank=True, related_name='western_power')
    switch_board = models.ManyToManyField(DocumentOrderUpload, blank=True, related_name='switch_board')
    panel_layout = models.ManyToManyField(DocumentOrderUpload, blank=True, related_name='panel_layout')
    extras = models.ManyToManyField(DocumentOrderUpload, blank=True, related_name='extras')
    packing_slip_reason = models.TextField(null=True, blank=True)
    western_power_reason = models.TextField(null=True, blank=True)
    switch_board_reason = models.TextField(null=True, blank=True)
    panel_layout_reason = models.TextField(null=True, blank=True)
    order_start_date = models.DateTimeField(null=True, blank=True)
    order_end_date = models.DateTimeField(null=True, blank=True)
    order_time = models.TimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_order')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_order')

# class Order(models.Model):
#     user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE, null=True, blank=True, related_name='order_user')
#     project = models.CharField(max_length=255, null=True, blank=True)
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
#     order_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
#     installation_Type = models.CharField(max_length=255, null=True, blank=True)
#     document_file = models.FileField(upload_to=document_path, null=True, blank=True, max_length=5000)
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
#     # last_status_changed = models.DateTimeField(null=True, blank=True)
    
#     def __str__(self):
#         return str(self.customer_name)
        
#     class Meta:
#         verbose_name = "Order"
#         verbose_name_plural = "Orders"
#         ordering = ['-updated_at']

SHIFT_CHOICES = (
		('Morning', 'Morning'),
		('Evening', 'Evening'),
	)

class DateString(models.Model):
    date = models.DateField()

class InstallerAvailibility(models.Model):
    # available_shift = models.CharField(max_length=30, choices=SHIFT_CHOICES, default='Morning')
    installer = models.ForeignKey(InstallerUser, on_delete=models.CASCADE)
    # Add other doctor fields like name, specialization, etc.
    # day_1 = models.DateField(null=True, blank=True)
    # day_2 = models.DateField(null=True, blank=True)
    # day_3 = models.DateField(null=True, blank=True)
    # day_4 = models.DateField(null=True, blank=True)
    # day_5 = models.DateField(null=True, blank=True)
    # day_6 = models.DateField(null=True, blank=True)
    # day_7 = models.DateField(null=True, blank=True)
    available_days = models.ManyToManyField(DateString, blank=True, related_name="available_date")
    available_start_time = models.TimeField()
    available_end_time = models.TimeField()
    is_anvailable = models.BooleanField(default=True)
    reason = models.TextField(null=True, blank=True )
    cancelled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_installer_avail')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_installer_avail')

    def __str__(self):
        return str(self.installer.admin.user.email)
    




class InstallerHoliday(models.Model):
    # available_shift = models.CharField(max_length=30, choices=SHIFT_CHOICES, default='Morning')
    installer = models.ForeignKey(InstallerUser, on_delete=models.CASCADE)
    # Add other doctor fields like name, specialization, etc.
    # day_1 = models.DateField(null=True, blank=True)
    # day_2 = models.DateField(null=True, blank=True)
    # day_3 = models.DateField(null=True, blank=True)
    # day_4 = models.DateField(null=True, blank=True)
    # day_5 = models.DateField(null=True, blank=True)
    # day_6 = models.DateField(null=True, blank=True)
    # day_7 = models.DateField(null=True, blank=True)
    holiday_days = models.ManyToManyField(DateString, blank=True, related_name="holiday_date")
    # available_start_time = models.TimeField()
    # available_end_time = models.TimeField()
    is_unavailable = models.BooleanField(default=True)
    reason = models.TextField(null=True, blank=True )
    cancelled = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_installer_holiday')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_installer_holiday')

    def __str__(self):
        return str(self.installer.admin.user.email)


class TakeAppointment(models.Model):
    # slots = models.PositiveIntegerField(default=0)
    # appointment = models.ManyToManyField(InstallerAvailibility, blank=True)
    customer = models.ForeignKey(Order, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField(null=True, blank=True, auto_now_add=True)
    # is_anvailable = models.BooleanField(default=True)
    appointment_appove = models.BooleanField(default=False)
    approval_send = models.BooleanField(default=False)
    # Add other appointment fields like reason, status, etc.
    reason = models.TextField(null=True, blank=True )
    cancelled = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_customer_Appointment')
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_customer_Appointment')

    def __str__(self):
        return f"{self.customer}"


class DocumentUpload(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    file = models.FileField(
        max_length=1000, upload_to="installation_docs/", null=True, blank=True
    )
    taken_from = models.CharField(max_length=255, default="App")
    upload_type = models.CharField(max_length=255, null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_customer_Document')
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.CharField(max_length=255, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_customer_Document')

    def __str__(self):
        return f"{self.upload_type} - {self.title}"
