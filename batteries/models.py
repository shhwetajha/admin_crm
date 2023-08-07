from django.db import models
from common.models import User
from common.utils import COMPONENT_TYPE

class BatteryModule(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    battery_logo = models.FileField(
        max_length=1000, upload_to="battery_logo/", null=True, blank=True
    )
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    total_energy = models.DecimalField(max_digits=12, null=True, blank=True, decimal_places=2)
    product_warranty = models.CharField(max_length=255, null=True, blank=True)
    my_list = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_battery_module')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_battery_module')

    class Meta:
        verbose_name = "Battery"
        verbose_name_plural = "Batteries"