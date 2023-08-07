from django.db import models

# Create your models here.
from django.db import models
from common.models import User
from order.models import Order, STATUS_CHOICES
import time

def document_path(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("docs", hash_, filename)

class Document(models.Model):

    contract_file = models.FileField(
        upload_to=document_path, 
        max_length=500, 
        null=True,
        blank=True,
        )
    contract_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    meter_box = models.FileField(
        upload_to=document_path, 
        max_length=500, 
        null=True,
        blank=True,
        )
    meter_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    electricity_bill = models.FileField(
        upload_to=document_path, 
        max_length=500, 
        null=True,
        blank=True,
        )
    electricity_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    council_rate = models.FileField(
        upload_to=document_path, 
        max_length=500, 
        null=True,
        blank=True,
        )
    council_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    miscellaneous_file = models.FileField(
        upload_to=document_path, 
        max_length=500, 
        null=True,
        blank=True,
        )
    miscellaneous_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    doc_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    order = models.OneToOneField(
        Order,
        related_name="order_document",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_by = models.ForeignKey(
        User,
        related_name="document_uploaded",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(
        auto_now_add=True
        )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='presite_risk_update'
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        null=True, 
        blank=True
    )
    class Meta:
        ordering = ("-created_on",)


class GridApproval(models.Model):
    order = models.OneToOneField(
        Order, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="grid_order"
        )
    meter_date = models.DateField(null=True, blank=True)
    meter_Approved_date = models.DateField(null=True, blank=True)    
    nmi_no = models.CharField(max_length=500, null=True, blank=True)
    energy_provider = models.CharField(max_length=500, null=True, blank=True)
    grid_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')

    created_by = models.ForeignKey(
        User,
        related_name="create_grid",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='update_grid'
        )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return str(self.order)
        
    class Meta:
        verbose_name = "GridApproval"
        verbose_name_plural = "GridApprovals"

RANGE_STATUS_CHOICE = (
		('0 to 5', '0 to 5'),
		('5 to 10', '5 to 10'),
		('10 to 20', '10 to 20'),
		('30+', '30+'),
	)
class PreSiteRisk(models.Model):
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        null=True, blank=True, related_name='order'
        )
    # project = models.OneToOneField(
    #     User, on_delete=models.CASCADE, 
    #     null=True, blank=True, 
    #     related_name='project_id'
    #     )
    approximate_age = models.CharField(
        max_length=30, choices=RANGE_STATUS_CHOICE, default='0 to 5'
        )
    hazards = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
        
    select_hazards = models.CharField(
        max_length=254, default='', null=True, blank=True
        )
    roof_structure = models.CharField(
        max_length=254, default='', null=True, blank=True
        )
    document_attachment = models.FileField(
        upload_to=document_path, max_length=500, null=True, blank=True, 
        )
    moss = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    moss_comment = models.CharField(
        max_length=255, null=True, blank=True
        )
    high_tension = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    high_tension_attachment = models.FileField(
        upload_to=document_path, max_length=500, null=True, blank=True, 
        )
    damaged_severley = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    roof_damage = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    any_damage = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    vehicle_activities = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    asbestos_presence  = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    safety_concerns = models.CharField(
        max_length=255, null=True, blank=True, default='No'
        )
    safety_concerns_comment = models.CharField(
        max_length=255, null=True, blank=True, 
        )
    presite_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, blank=True, related_name='create_presite'
        )
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True
        )
    updated_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='update_presite'
        )

    # def __str__(self):
    #     return self.order.user.email
        
    class Meta:
        verbose_name = "PreSite Risk"
        verbose_name_plural = "PreSite Risks"