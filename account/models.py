from django.db import models
from django.utils.translation import pgettext_lazy
from django.utils.translation import gettext_lazy as _
from common.models import User, Address
from common.utils import INDCHOICES, COUNTRIES
from common import utils
from django.core.validators import RegexValidator
from order.models import Order

class Account(models.Model):

    ACCOUNT_STATUS_CHOICE = (("open", "Open"), ("close", "Close"))
    name = models.CharField(pgettext_lazy("Name of Account", "Name"), max_length=64)
    email = models.EmailField()
    # phone = PhoneNumberField(null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile incorrect.")
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    # industry = models.CharField(
    #     _("Industry Type"), max_length=255, choices=INDCHOICES, blank=True, null=True
    # )
    billing_address = models.OneToOneField(
        Address, related_name='account_billing_address', on_delete=models.CASCADE, blank=True, null=True)
    # assigned_to = models.OneToOneField(User,on_delete=models.CASCADE, related_name="account_assigned_users")
    status = models.CharField(
        choices=ACCOUNT_STATUS_CHOICE, max_length=64, default="open"
    )
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        User, related_name="account_created_by", on_delete=models.SET_NULL, null=True
    )
    created_on = models.DateTimeField(_("Created on"), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='update_account')
    assigned_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True, blank=True, related_name="account_assigned_by_admin")
    is_active = models.BooleanField(default=False)
    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        null=True, blank=True, related_name='order_account'
        )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.order.customer_name

class Email(models.Model):
    order = models.ForeignKey(
        Order, related_name="sent_email", on_delete=models.SET_NULL, null=True
    )
    from_account = models.ForeignKey(
        Account, related_name="sent_email", on_delete=models.SET_NULL, null=True
    )
    # user = models.ForeignKey(User, related_name="sent_email", on_delete=models.CASCADE, null=True
    # )
    message_subject = models.TextField(null=True)
    message_body = models.TextField(null=True)
    timezone = models.CharField(max_length=100, default="UTC")
    scheduled_date_time = models.DateTimeField(null=True)
    scheduled_later = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    from_email = models.EmailField()
    rendered_message_body = models.TextField(null=True)

    # def __str__(self):
    #     return self.user.email


class EmailLog(models.Model):
    """this model is used to track if the email is sent or not"""

    email = models.ForeignKey(
        Email, related_name="email_log", on_delete=models.SET_NULL, null=True
    )
    is_sent = models.BooleanField(default=False)


