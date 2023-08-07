from django.db import models
from django.utils.translation import gettext_lazy as _
from common.models import User
from common.utils import CURRENCY_CODES
from account.models import Account
from common.models import Address
from django.core.validators import RegexValidator
import time
from order.models import Order

INVOICE_STATUS = (
        ("Paid", "Paid"),
        ("Pending", "Pending"),
        ("Cancelled", "Cancel"),
    )

def invoice_url(self, filename):
    hash_ = int(time.time())
    return "%s/%s/%s" % ("invoice", hash_, filename)
phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Mobile incorrect.")
class Invoice(models.Model):
    """Model definition for Invoice."""

    order = models.OneToOneField(
        Order, 
        on_delete=models.CASCADE, 
        null=True, blank=True, related_name='order_invoice'
        )
    # account = models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='account_number')
    invoice_title = models.CharField(_("Invoice Title"), max_length=50,  null=True, blank=True, default='Billing')
    invoice_number = models.CharField(max_length=256, null=True, blank=True)
    from_address = models.ForeignKey(
        Address,
        related_name="invoice_from_address",
        on_delete=models.CASCADE,
        null=True,
    )
    to_address = models.OneToOneField(
        Address, related_name="invoice_to_address", on_delete=models.SET_NULL, null=True
    )
    name = models.CharField(_("Name"), max_length=100)
    email = models.EmailField(_("Email"))
    # assigned_to = models.OneToOneField(User, null=True, on_delete=models.SET_NULL, related_name="invoice_assigned_to")
    
    # quantity is the number of product
    quantity = models.PositiveIntegerField(default=0)
    
    # rate is the rate charged
    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    special_discount = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    other = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    # total amount is product of rate and quantity
    total_amount = models.DecimalField(default=0,
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    tax = models.DecimalField(default=0,blank=True, null=True, max_digits=12, decimal_places=2)
    currency = models.CharField(default=0,
        max_length=3, choices=CURRENCY_CODES, blank=True, null=True
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    payment_status =  models.CharField(_("Status"),null=True, blank=True, max_length=100)
    payment_method =  models.CharField(_("Method"), null=True, blank=True, max_length=100)
    surcharge =  models.CharField(_("Surcharge"), default=0, null=True, blank=True, max_length=100)
    payment_date = models.DateTimeField(auto_now=True)
    website = models.URLField(_("Website"), default='https://solar365.net.au/',  blank=True, null=True)
    summary = models.FileField(
        max_length=1000, upload_to=invoice_url, null=True, blank=True
    )
    invoice = models.FileField(
        max_length=1000, upload_to=invoice_url, null=True, blank=True
    )
    amount_due = models.DecimalField(default=0, 
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    amount_paid = models.DecimalField(default=0, 
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    pay = models.DecimalField(default=0,
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name="invoice_created_by", on_delete=models.SET_NULL, null=True
    )
    is_email_sent = models.BooleanField(default=False)
    status = models.CharField(choices=INVOICE_STATUS, max_length=15, default="Pending")
    details = models.TextField(_("Details"), null=True, blank=True)
    due_date = models.DateField(blank=True, null=True)
    full_pay_due_date = models.DateField(blank=True, null=True)
        
    class Meta:
        """Meta definition for Invoice."""

        verbose_name = "Invoice"
        verbose_name_plural = "Invoices"
        ordering = ["-created_on"]

    def formatted_total_amount(self):
        return self.currency + " " + str(self.total_amount)

    def formatted_rate(self):
        return str(self.rate) + " " + self.currency

    def formatted_total_quantity(self):
        return str(self.quantity) + " " + "items"

    def is_draft(self):
        if self.status == "Draft":
            return True
        else:
            return False

    def is_sent(self):
        if self.status == "Sent" and self.is_email_sent == False:
            return True
        else:
            return False

    def is_resent(self):
        if self.status == "Sent" and self.is_email_sent == True:
            return True
        else:
            return False

    def is_paid_or_cancelled(self):
        if self.status in ["Paid", "Cancelled"]:
            return True
        else:
            return False

    def __str__(self):
        """Unicode representation of Invoice."""
        return self.email

class InvoiceHistory(models.Model):
    """Model definition for InvoiceHistory.
    This model is used to track/keep a record of the updates made to original invoice object."""
    # order = models.ForeignKey(
    #     Order,
    #     related_name="order_invoice_history",
    #     on_delete=models.SET_NULL,
    #     null=True,
    # )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="invoice_history"
    )
    invoice_title = models.CharField(_("Invoice Title"), max_length=50)
    invoice_number = models.CharField(max_length=256, null=True, blank=True)
    # invoice_number = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='invoice_number_history')
    to_address = models.ForeignKey(
        Address,
        related_name="invoice_history_to_address",
        on_delete=models.SET_NULL,
        null=True,
    )
    from_address = models.ForeignKey(
        Address,
        related_name="invoice_history_from_address",
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(_("Name"), max_length=100, null=True, blank=True)
    email = models.EmailField(_("Email"), null=True, blank=True)
    # assigned_to = models.ManyToManyField(
    #     User, related_name="invoice_history_assigned_to"
    # )
    
    # quantity is the number of items
    quantity = models.PositiveIntegerField(default=0)
    
    # rate is the rate charged
    rate = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    
    # total amount is product of rate and quantity
    total_amount = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    payment_method =  models.CharField(_("Method"), null=True, blank=True, max_length=100)
    
    currency = models.CharField(
        max_length=3, choices=CURRENCY_CODES, blank=True, null=True
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True,null=True)
    receipt = models.FileField(
        max_length=1000, upload_to=invoice_url, null=True, blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, related_name='invoice_history_created_by',
        on_delete=models.SET_NULL, null=True)
    amount_due = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    amount_paid = models.DecimalField(
        blank=True, null=True, max_digits=12, decimal_places=2
    )
    is_email_sent = models.BooleanField(default=False)
    status = models.CharField(choices=INVOICE_STATUS, max_length=15, default="Pending")
    
    # details or description here stores the fields changed in the original invoice object
    details = models.TextField(_("Details"), null=True, blank=True)
    due_date = models.DateField(auto_now_add=True)
    payment_date = models.DateField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_on"]

    def formatted_total_amount(self):
        return self.currency + " " + str(self.total_amount)

    def formatted_rate(self):
        return str(self.rate) + " " + self.currency

    def formatted_total_quantity(self):
        return str(self.quantity) + " " + "Hours"

    def __str__(self):
        """Unicode representation of Invoice."""
        return self.email
        