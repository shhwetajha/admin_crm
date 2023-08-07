
from datetime import datetime

from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.conf import settings
from common.models import User, Address, InstallerUser, Team, NonAdminUser
import urllib.request
from invoice.models import Invoice, InvoiceHistory
from order.models import Order, TakeAppointment


class Mailer:
    """
    Mailer
    """
    def __init__(self, **kwargs):
        self.email_id = kwargs.get('email_id', None)
        self.email_status = False
        self.notification_category = "EMAIL"
        self.email_subject = kwargs.get('subject', None)
        self.filename = kwargs.get('filename', None)
        self.reason_for_failed = 'Error'
        self.subject = kwargs.get("subject", None)
        self.otp = kwargs.get('otp', None)
        self.type = kwargs.get("type", None)
        self.reset_hash = kwargs.get("reset_hash", None)
        self.invoice_hist = kwargs.get("invoice_hist", None)
        # self.reset_hash = kwargs.get("reset_hash", None)
        if self.type == "otp":
            self.template_name = "otp.html"
        elif self.type == "register":
            self.template_name = "create_customer_html.html"
        elif self.type == "receipt_template":
            self.template_name = "invoice_mail.html"
        elif self.type == "appointment_app_mail":
            self.template_name = "appointment_app_mail.html"
        elif self.type == "not_app_appointment_mail":
            self.template_name = "not_app_appointment_mail.html"
        elif self.type == 'installer_registration_mail':
            self.template_name = "installer_registration_mail.html"
        elif self.type == "team_registration_mail":
            self.template_name = "team_registration_mail.html"
        elif self.type == "company_mail":
            self.template_name = "company_mail.html"
        elif self.type == "not_app_company_mail":
            self.template_name = "not_app_company_mail.html"

    # approve = TakeAppointment.objects.get(id=i)
    def __call__(self):
        return self.email_sender()

    def email_sender(self):
        try:
            user_instance = User.objects.get(email=self.email_id)
            admin = User.objects.get(is_main=True)
            address = Address.objects.get(user=admin)
            if self.type == "receipt_template":
                invoice = Invoice.objects.get(invoice_number=user_instance.username)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "otp": self.otp,
                    "invoice": invoice,
                    "admin":admin,
                    "address": address,
                    "invoice_hist":self.invoice_hist,
                }
            elif (self.type == "appointment_app_mail") or self.type == "not_app_appointment_mail" :
                order = Order.objects.get(project=user_instance.username)
                appointment = TakeAppointment.objects.get(customer=order)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "order":order,
                    "appointment": appointment,
                    "reset_link": self.reset_hash,
                    "admin":admin,
                    "address": address,
                }
            elif self.type == 'installer_registration_mail':
                _profile = User.objects.get(email=self.email_id)
                add = Address.objects.get(user=_profile)
                installer = InstallerUser.objects.get(admin=add)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "to_address":add,
                    "installer": installer,
                    "admin":admin,
                    "address": address,
                }
            elif self.type == 'team_registration_mail':
                _profile = User.objects.get(email=self.email_id)
                add = Address.objects.get(user=_profile)
                installer = Team.objects.get(admin=add)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "to_address":add,
                    "installer": installer,
                    "admin":admin,
                    "address": address,
                }
            elif self.type == 'company_mail':
                _profile = User.objects.get(email=self.email_id)
                add = Address.objects.get(user=_profile)
                installer = NonAdminUser.objects.get(admin=add)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "to_address":add,
                    "installer": installer,
                    "admin":admin,
                    "otp":self.otp,
                    "address": address,
                }
            elif self.type == 'not_app_company_mail':
                _profile = User.objects.get(email=self.email_id)
                add = Address.objects.get(user=_profile)
                installer = NonAdminUser.objects.get(admin=add)
                template_data = {
                    "email":self.email_id,
                    "user":user_instance,
                    "to_address":add,
                    "installer": installer,
                    "admin":admin,
                    "otp":self.otp,
                    "address": address,
                }
            else:
                template_data = {
                    "email":self.email_id,
                    "context":user_instance,
                    "admin":admin,
                    "address": address,
                }
            html_content = render_to_string(
                self.template_name, template_data)
            text_content = strip_tags(html_content)
            msg = EmailMultiAlternatives(self.subject,
                                         text_content,
                                         settings.EMAIL_HOST_USER,
                                         [self.email_id],
                                         )
            msg.attach_alternative(html_content, "text/html")
            if (self.filename) is not None:
                for file in self.filename:
                    # msg.attach_file(file)
                    # msg.attach_file("/home/admin1/Documents/Solar_Admin/Is-It-Worth-Getting-a-10kW-Solar-System-/admin_crm"+str(file))
                    msg.attach_file("/home/ubuntu/solar_panel/Is-It-Worth-  Getting-a-10kW-Solar-System-/admin_crm"+str(file))
                return True if msg.send() else False
            else:
                return True if msg.send() else False
        except Exception as e:
            print("ef"*100, e)
            self.reason_for_failed = str(e)
            return False