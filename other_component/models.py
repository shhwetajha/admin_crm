from django.db import models
from common.models import User
from common.utils import COMPONENT_TYPE

# Create your models here.
class OtherComponent(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    code = models.CharField(max_length=255, null=True, blank=True, unique=True)
    component_logo = models.FileField(
        max_length=1000, upload_to="component_logo/", null=True, blank=True
    )   
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    smart_meter = models.CharField(max_length=255, null=True, blank=True)
    optimisor = models.CharField(max_length=255, null=True, blank=True)
    product_warranty = models.PositiveSmallIntegerField(null=True, blank=True) 
    smart_meter_heading = models.CharField(max_length=255, null=True, blank=True)
    optimisor_heading = models.CharField(max_length=255, null=True, blank=True)
    my_list = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='create_other_module')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_other_module')
    
    class Meta:
        verbose_name = "Other Component"
        verbose_name_plural = "Other Components"