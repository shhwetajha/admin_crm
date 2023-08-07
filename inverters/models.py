from django.db import models
from common.models import User

class InverterModule(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    inverter_logo = models.FileField(
        max_length=1000, upload_to="inverter_logo/", null=True, blank=True
    )
    inverter_type = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    rated_output_power = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    product_warranty = models.PositiveSmallIntegerField(null=True, blank=True)
    additional_part_warranty = models.PositiveSmallIntegerField(null=True, blank=True)
    my_list = models.BooleanField(default=False)
    default_inverter_range = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_inverter_module')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_inverter_module')
        
    class Meta:
        verbose_name = "Inverter"
        verbose_name_plural = "Inverters"