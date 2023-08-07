from common.models import User, Address
from django.conf import settings
from django.core.mail import send_mail
from grid_approval.models import Document, GridApproval, PreSiteRisk
from installation.models  import Installation, WarrantyDocument, InstallationDocument
from account.models import Email, Account
from invoice.models import Invoice
from common.mailer import Mailer

def update_user_type(sender, instance, created, *args, **kwargs):
	"""
    Update User And Admin Role And Creating Address.
    """
	if created:
		if (instance.is_superuser == True) or (instance.is_staff == True):
			instance.user_type = 'ADMIN'
			instance.save()
			try:
				address = Address.objects.get(user=instance)
				if address:
					pass
			except Exception as e:
				Address.objects.create(user=instance)
		else:
			pass
		# if (instance.user_type=='CUSTOMER'):
		# 	pass
		# elif (instance.user_type == 'NON_ADMIN'):
		# 	if (instance.has_approve == True):
		# 		subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
		# 		# email_from = settings.EMAIL_HOST_USER
		# 		message = "Dear" + str(instance.first_name)  + " " +  str(instance.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(instance.username) + "and, " + "\nPassword : " + str(instance.pin)
		# 		# recipient_list = [instance.email]
		# 		# send_mail(subject,message, email_from, recipient_list)
		# 		mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="register")
		# 		_mail= mail_response()
		# 	else:
		# 		subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
		# 		# email_from = settings.EMAIL_HOST_USER
		# 		message = "Thanks for using the Solar365" + "\nI hope you are doing well, " + "I want to inform that when admin approve your account then you can Signin. "
		# 		# recipient_list = [instance.email]
		# 		# send_mail(subject,message, email_from, recipient_list)
		# 		mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="register")
		# 		_mail= mail_response()
		# else:
		# 	subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
		# 	# email_from = settings.EMAIL_HOST_USER
		# 	message = "Username : " + str(instance.username) + "\nPassword : " + str(instance.pin)
		# 	# recipient_list = [instance.email]
		# 	# send_mail(subject,message, email_from, recipient_list)
		# 	mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="installer_registration_mail")
		# 	_mail= mail_response()


def update_order_id(sender, instance, created, *args, **kwargs):
	"""
    Update Order Id and Create Presite Risk Assesement when Order Created.
    """
	if created:
		user = User.objects.get(username=instance.project)
		to_address = Address.objects.get(user=user)
		admin_user = User.objects.get(user_type='ADMIN', is_superuser=True, is_main=True)
		from_address = Address.objects.get(user=admin_user)
		instance.admin = to_address
		instance.customer_name = user.first_name + " " + user.first_name
		instance.to_address = to_address
		# instance.created_by = admin_user
		instance.from_address = from_address
		# instance.order_status = 'Completed'
		instance.save()
		name = user.first_name + " " + user.first_name

		try:
			presite = PreSiteRisk.objects.get(order=instance)
			if presite:
				pass
		except Exception as e:
			PreSiteRisk.objects.create(order=instance, created_by=instance.created_by)

		try:
			docs = Document.objects.get(order=instance)
			if docs:
				pass
		except Exception as e:
			Document.objects.create(order=instance, created_by=instance.created_by)
		try:
			grid = GridApproval.objects.get(order=instance)
			if grid:
				pass
		except Exception as e:
			GridApproval.objects.create(order=instance, nmi_no=instance.nmi_no, created_by=instance.created_by)
		# try:
		# 	docs = Account.objects.get(order=instance)
		# 	if docs:
		# 		pass
		# except Exception as e:
			
		# 	Account.objects.create(name=name, email=user.email, phone=user.phone, assigned_by=instance.created_by, created_by=instance.created_by, billing_address=to_address, order=instance)
		try:
			docs = Invoice.objects.get(order=instance)
			if docs:
				pass
		except Exception as e:
			email = user.email
			mobile = user.phone
			invoice_number = user.username
			Invoice.objects.create(invoice_number=invoice_number, email=email, name=name, phone=mobile, from_address=from_address, to_address=to_address, created_by=instance.created_by, order=instance)
			# Invoice.objects.create(invoice_number=invoice_number, email=email, name=name, phone=mobile, to_address=to_address, created_by=instance.created_by, order=instance)
		try:
			docs = Installation.objects.get(order=instance)
			if docs:
				pass
		except Exception as e:
			Installation.objects.create(order=instance, nmi_no=instance.nmi_no, created_by=instance.created_by)
		try:
			docs = InstallationDocument.objects.get(order=instance)
			if docs:
				pass
		except Exception as e:
			InstallationDocument.objects.create(order=instance, created_by=instance.created_by)
		try:
			docs = WarrantyDocument.objects.get(order=instance)
			if docs:
				pass
		except Exception as e:
			WarrantyDocument.objects.create(order=instance)
			subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "your order successfully registered"
			# email_from = settings.EMAIL_HOST_USER
			message = "Project : " + str(user.username)+"\nPin : " + user.pin
			# recipient_list = [user.email]
			# send= send_mail(subject,message, email_from, recipient_list)
			mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="register")
			_mail= mail_response()
			# Email.objects.create(order=instance, message_subject=subject, message_body=message, from_email=email_from)
	else:
		pass

# def formfield_for_foreignkey(sender, instance, **kwargs):
# 	if instance.id is None:
# 		exclude_ids=Order.objects.all().values_list("user__id",flat=True)
# 		kwargs["queryset"] = User.objects.filter(is_superuser=False).exclude(id__in=exclude_ids)
# 	else:
# 		pass
