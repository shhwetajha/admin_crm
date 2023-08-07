from django.db import models
from common.models import User
from account.models import Account
# from grid_approval.models import STATUS_CHOICES, GridApproval
import time
from invoice.models import Invoice
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from order.models import Order
# upload_to=document_path, 
def document_path(self, filename):
    # hash_ = int(time.time())
    return "%s/%s/%s" % ("installation", filename)


STATUS_CHOICES = (
		('Pending', 'Pending'),
		('Completed', 'Completed'),
	)
class Installation(models.Model):
    ins_booking_date = models.DateTimeField(_("Installation Booking Date"), blank=True, null=True)
    ins_completed_date = models.DateTimeField(_("Installation Complete Date"), null=True, blank=True)
    payment_due = models.CharField(max_length=500, null=True, blank=True)
    nmi_no = models.CharField(max_length=500, null=True, blank=True)
    installation_status = models.CharField(
        choices=STATUS_CHOICES, max_length=64, default="Pending"
    )
    net_meter_status = models.CharField(
        choices=STATUS_CHOICES, max_length=64, default="Pending"
    )
    important_info = models.FileField(max_length=1001, upload_to="attachments/%Y/%m/", null=True, blank=True)
    ins_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    # invoice = models.OneToOneField(
    #     Invoice, 
    #     null=True,
    #     blank=True, 
    #     on_delete=models.CASCADE, 
    #     related_name="installation_account"
    # )
    order = models.OneToOneField(
        Order, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="installation_order"
        )
    # account = models.OneToOneField(
    #     Account, 
    #     null=True, 
    #     blank=True, 
    #     on_delete=models.CASCADE, 
    #     related_name="installation_account"
    # )
    # grid_approval = models.OneToOneField(
    #     GridApproval, 
    #     null=True, 
    #     blank=True, 
    #     on_delete=models.CASCADE, 
    #     related_name="installation_grid"
    # )
    created_by = models.ForeignKey(
        User,
        related_name="create_installation",
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
        related_name='update_installation'
        )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.order.project
        
    class Meta:
        verbose_name = "Installation"
        verbose_name_plural = "Installations"


class InstallationDocument(models.Model):

    DOCUMENT_STATUS_CHOICE = (("Pending", "Pending"), ("Received", "Received"))
    contract_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    contract_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    grid_approval_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    grid_approval_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    compliance_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    compliance_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    pv_site_info_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    pv_site_info_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    energy_yield_report_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    energy_yield_report_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    safety_certificate_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    safety_certificate_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    noc_docs = models.FileField(max_length=1001, upload_to='inst_attachment/', null=True, blank=True)
    noc_status = models.CharField(
        choices=DOCUMENT_STATUS_CHOICE, max_length=64, default="Pending"
    )
    user_manual = models.FileField(max_length=1001, upload_to="attachments/%Y/%m/", null=True, blank=True)
    # user_manual = models.ForeignKey(
    #     UserManual,
    #     related_name="create_user_manual",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    order = models.OneToOneField(
        Order, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="installationdocument_order"
        )
    insdoc_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    created_by = models.ForeignKey(
        User,
        related_name="create_installationdocument",
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
        related_name='update_installationdocument'
        )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.order.project

    def __nonzero__(self):
        return bool(self.contract_docs)
        
    class Meta:
        verbose_name = "InstallationDocument"
        verbose_name_plural = "InstallationDocuments"

class WarrantyDocument(models.Model):
    panels_brands = models.TextField(blank=True, null=True)
    panels_docs = models.FileField(upload_to='order_warranty/', null=True, blank=True)
    inverter_brands = models.TextField(blank=True, null=True)
    inverter_docs = models.FileField(upload_to='order_warranty/', null=True, blank=True)
    battery_brands = models.TextField(blank=True, null=True)
    battery_docs = models.FileField(upload_to='order_warranty/', null=True, blank=True)
    war_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    order = models.OneToOneField(
        Order, 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name="order_warranty"
        )

    created_by = models.ForeignKey(
        User,
        related_name="create_warranty",
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
        related_name='update_warranty'
        )
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.order.project

    class Meta:
        verbose_name = "WarrantyDocument"
        verbose_name_plural = "WarrantyDocuments"


class UserReferral(models.Model):
    referred_by = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE,related_name="user_referred_by_user")
    first_name = models.CharField(max_length=500, null=True, blank=True)
    last_name = models.CharField(max_length=500, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile incorrect.")
    mobile_no = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    referral_address_line = models.CharField(
        _("Address"), max_length=255, blank=True, null=True
    )
    referral_street = models.CharField(_("Street"), max_length=55, blank=True, null=True)
    referral_city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    referral_state = models.CharField(_("State"), max_length=255, blank=True, null=True)
    referral_postcode = models.CharField(
        _("Post/Zip-code"), max_length=64, blank=True, null=True
    )
    referral_country = models.CharField(
        max_length=255,  blank=True, null=True
    )
    joined_date = models.DateTimeField(null=True, blank=True)
    referral_date = models.DateTimeField(auto_now_add=True)
    referral_url = models.CharField(max_length=500, null=True, blank=True)

    def get_complete_address(self):
        address = ""
        if self.referral_address_line:
            address += self.referral_address_line
        if self.referral_street:
            if address:
                address += ", " + self.referral_street
            else:
                address += self.referral_street
        if self.referral_city:
            if address:
                address += ", " + self.referral_city
            else:
                address += self.referral_city
        if self.referral_state:
            if address:
                address += ", " + self.referral_state
            else:
                address += self.referral_state
        if self.referral_postcode:
            if address:
                address += ", " + self.referral_postcode
            else:
                address += self.referral_postcode
        if self.referral_country:
            if address:
                address += ", " + self.referral_country()
            else:
                address += self.referral_country()
        return address

    def __str__(self):
        return self.referred_by.admin.user.email
        
    class Meta:
        verbose_name = "UserReferral"
        verbose_name_plural = "UserReferrals"

class ReferralSuccess(models.Model):
    referrals_made = models.CharField(max_length=64, null=True, blank=True)
    referrals_paid = models.CharField(max_length=64, null=True, blank=True)
    approval_pending = models.CharField(max_length=64, null=True, blank=True)
    referral = models.ManyToManyField(UserReferral, blank=True, related_name="user_referred")
    referral_by = models.ForeignKey(Order, null=True, blank=True, on_delete=models.CASCADE,related_name="referred_by_user")

    class Meta:
        verbose_name = "ReferralSuccess"
        verbose_name_plural = "ReferralSuccesses"

    def __str__(self):
        return self.referral_by.admin.user.email