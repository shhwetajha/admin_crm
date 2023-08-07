from decimal import Decimal
from rest_framework import status
from common.models import *
from django.http import JsonResponse
# Remaining time - current time function
import datetime as dt
from django.db.models import Q
from celery.schedules import crontab
from celery.decorators import periodic_task

from common.mailer import Mailer
from order.models import TakeAppointment, InstallerAvailibility, DateString
from common.models import User
from datetime import timedelta, date
from dateutil.parser import parse # pip install python-dateutil


print('UPDATE match list data automatically with celery *******************************beat update roster points and players automatically')
'''UPDATE match list data automatically with celery beat
update roster points and players automatically'''

# @periodic_task(run_every=(crontab(minute=0, hour=10, day_of_week=6)), name="approval", ingore_result=True)
# @periodic_task(run_every=(crontab(minute=0, hour='*/2')), name="approval", ingore_result=True)
@periodic_task(run_every=dt.timedelta(seconds=30), name="approval", ingore_result=True)
def approval():
    today = date.today()
    start_date = today + timedelta(days = 1)
    for day in range(1, 8):
        appoint_ment_date = start_date+timedelta(days=day)
        approval_data = TakeAppointment.objects.filter(appointment_date=appoint_ment_date).order_by('created_at')
        if len(approval_data) > 0:
            inst_user = InstallerUser.objects.filter(has_installer=True)
            if DateString.objects.filter(date=appoint_ment_date).exists():
                avail = DateString.objects.get(date=appoint_ment_date)
                elect_user = InstallerUser.objects.filter(has_electrician=True)
                inst_avail = InstallerAvailibility.objects.filter(Q(installer__in=inst_user), available_days__date=avail.date, is_anvailable=True)
                elect_avail = InstallerAvailibility.objects.filter(Q(installer__in=elect_user, available_days__date=avail.date, is_anvailable=True))
                if (int(len(inst_avail) * 0.5)) >= (len(elect_avail)):
                    if (len(approval_data) > len(elect_avail)):
                        _id = list(approval_data.values_list('id', flat=True).distinct())
                        _id.sort()
                        n=len(elect_avail) + 1
                        i = 0
                        while _id[i] < n:
                            i += 1
                        under = _id[:i]
                        over = _id[i:]
                        if len(under) > 0:
                            for i in under:
                                approve = TakeAppointment.objects.get(id=i)
                                instance = User.objects.get(username=approve.customer.project)
                                subject = "Appointment Approved" + "-" + str(approve.appointment_date)
                                message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                                mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="appointment_app_mail")
                                _mail= mail_response()
                                print(_mail)
                        else:
                            pass
                        if len(over) > 0:
                            for i in over:
                                approve = TakeAppointment.objects.get(id=i)
                                instance = User.objects.get(username=approve.customer.project)
                                subject = "Appointment Not Approved" + "-" + str(instance.first_name)  + " " +  str(instance.last_name)
                                message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                                reset_link = 'http://127.0.0.1:8000/' + 'take-appointment/' + str(i)
                                mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, reset_hash=reset_link, type="not_app_appointment_mail")
                                _mail= mail_response()
                                print(_mail)
                        else:
                            pass
                    else:
                        _id = list(approval_data.values_list('id', flat=True).distinct())
                        _id.sort()
                        for i in _id:
                            approve = TakeAppointment.objects.get(id=i)
                            instance = User.objects.get(username=approve.customer.project)
                            subject = "Appointment Approved" + "-" + str(approve.appointment_date)
                            message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                            mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="appointment_app_mail")
                            _mail= mail_response()
                            print(_mail)
                elif (int(len(inst_avail) * 0.5)) < (len(elect_avail)):
                    if (len(approval_data) > (int(len(inst_avail) * 0.5))):
                        _id = list(approval_data.values_list('id', flat=True).distinct())
                        _id.sort()
                        n=len(elect_avail) + 1
                        i = 0
                        while _id[i] < n:
                            i += 1
                        under = _id[:i]
                        over = _id[i:]
                        if len(under) > 0:
                            for i in under:
                                approve = TakeAppointment.objects.get(id=i)
                                instance = User.objects.get(username=approve.customer.project)
                                subject = "Appointment Approved" + "-" + str(approve.appointment_date)
                                message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                                mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="appointment_app_mail")
                                _mail= mail_response()
                                print(_mail)
                        else:
                            pass
                        if len(over) > 0:
                            for i in over:
                                approve = TakeAppointment.objects.get(id=i)
                                instance = User.objects.get(username=approve.customer.project)
                                subject = "Appointment Not Approved" + "-" + str(instance.first_name)  + " " +  str(instance.last_name)
                                message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                                reset_link = 'http://127.0.0.1:8000/' + 'take-appointment/' + str(i)
                                mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, reset_hash=reset_link, type="not_app_appointment_mail")
                                _mail= mail_response()
                                print(_mail)
                        else:
                            pass
                    else:
                        _id = list(approval_data.values_list('id', flat=True).distinct())
                        _id.sort()
                        for i in _id:
                            approve = TakeAppointment.objects.get(id=i)
                            instance = User.objects.get(username=approve.customer.project)
                            subject = "Appointment Approved" + "-" + str(approve.appointment_date)
                            message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                            mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="appointment_app_mail")
                            _mail= mail_response()
                            print(_mail)
                else:
                    _id = list(approval_data.values_list('id', flat=True).distinct())
                    _id.sort()
                    for i in _id:
                        approve = TakeAppointment.objects.get(id=i)
                        instance = User.objects.get(username=approve.customer.project)
                        subject = "Appointment Not Approved" + "-" + str(instance.first_name)  + " " +  str(instance.last_name)
                        message = "Dear" + " " + str(instance.first_name)  + " " +  str(instance.last_name)
                        reset_link = 'http://127.0.0.1:8000/' + 'take-appointment/' + str(i)
                        mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, reset_hash=reset_link, type="not_app_appointment_mail")
                        _mail= mail_response()
                        print(_mail)
    return '**********************Sent Approval***************'


# @periodic_task(run_every=(crontab(minute=0, hour=10, day_of_week=6)), name="approval", ingore_result=True)
# def approval():
#     today = date.today()
#     start_date = today + timedelta(days = 1)
#     end_date = today + timedelta(days = 7)

#     approval_data = TakeAppointment.objects.filter(appointment_date__range=[start_date, end_date]).order_by('created_at')
#     print("approval_data"*10, approval_data)
#     if len(approval_data) > 0:
#         # for i in a
#         inst_user = InstallerUser.objects.filter(has_installer=True)
#         if DateString.objects.filter(date=start_date).exists():
#             avail = DateString.objects.get(date=start_date)
#             elect_user = InstallerUser.objects.filter(has_electrician=True)
#             inst_avail = InstallerAvailibility.objects.filter(Q(installer__in=inst_user), available_days__date=avail.date, is_anvailable=True)
#             elect_avail = InstallerAvailibility.objects.filter(Q(installer__in=elect_user, available_days__date=avail.date, is_anvailable=True))
#             print("elect_avail"*10, len(elect_avail), len(inst_avail))
#             # if len(inst_avail) > 0 and len(elect_avail) > 0:
#             #     if (len(inst_avail) > len(approval_data)) and  (len(elect_avail) >= len(approval_data)):
#             #         print("approve all Customers")
#             #         subject = "Appointment Status"
#             #         # email_from = settings.EMAIL_HOST_USER
#             #         message = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "your Appointment has been approved"
#             #         # recipient_list = [instance.email]
#             #         # send_mail(subject,message, email_from, recipient_list)
#             #         mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="otp")
#             #     elif (len(inst_avail) <= len(approval_data)) and  (len(elect_avail) >= len(approval_data)):
#             #         print("those who come first will get first approval")
#             #         subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
#             #         # email_from = settings.EMAIL_HOST_USER
#             #         message = "Dear" + str(instance.first_name)  + " " +  str(instance.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(instance.username) + "and, " + "\nPassword : " + str(instance.pin)
#             #         # recipient_list = [instance.email]
#             #         # send_mail(subject,message, email_from, recipient_list)
#             #         mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="otp")
#             #     elif (len(inst_avail) < len(approval_data)) and  (len(elect_avail) < len(approval_data)):
#             #         print("Appointment not approved as no availibility left")
#             #         subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
#             #         # email_from = settings.EMAIL_HOST_USER
#             #         message = "Dear" + str(instance.first_name)  + " " +  str(instance.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(instance.username) + "and, " + "\nPassword : " + str(instance.pin)
#             #         # recipient_list = [instance.email]
#             #         # send_mail(subject,message, email_from, recipient_list)
#             #         mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="otp")
#             # else:
#             #     print("Cancelled all customers")
#                 # subject = "Congratulations!" +  " " + str(instance.first_name)  + " " +  str(instance.last_name) + " " + "you are successfully registered"
# 				# # email_from = settings.EMAIL_HOST_USER
# 				# message = "Dear" + str(instance.first_name)  + " " +  str(instance.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(instance.username) + "and, " + "\nPassword : " + str(instance.pin)
# 				# # recipient_list = [instance.email]
# 				# # send_mail(subject,message, email_from, recipient_list)
# 				# mail_response = Mailer(email_id=instance.email, subject=subject, otp=message, type="otp")

#         return '**********************Sent Approval***************'
#     else:
#         return '------------No Appointments Available--------------'
