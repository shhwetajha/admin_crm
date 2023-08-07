
from rest_framework import status, filters
from order.serializer import *
import json
from common.serializer import *
from invoice.serializer import InvoiceSerailizer, InvoiceHistorySerializer
from installation.models import Installation, InstallationDocument, WarrantyDocument
from installation.serializer import *
from grid_approval.serializer import (
    
    DocumentSerializer, 
    GridApprovalSerializer, PreSiteRiskSerializer
)
import random
from grid_approval.models import Document, GridApproval, PreSiteRisk
from common.mailer import Mailer
from rest_framework.viewsets import ModelViewSet
from order.models import *
from common.models import User, Address, InstallerUser, NonAdminUser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from invoice.models import Invoice, InvoiceHistory
from installation.models import Installation
from common.generate_pdf import GeneratePDF
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view, action, permission_classes
from datetime import datetime, timedelta, date
from dateutil.parser import parse # pip install python-dateutil
from rest_framework.views import APIView
from django.db.models import Q
from django.forms.models import model_to_dict
from order.timeleft import working_time_function

#2.310-celerybeat
# function for tackling multiple errors in just on variable

def getFirstError(errors):
    message = ""
    for error in errors:
        if isinstance(errors[error], dict):
            for error2 in errors[error]:
                message = errors[error][error2][0]
        else:
            if isinstance(errors[error][0], dict):
                for error2 in errors[error][0]:
                    message =  errors[error][0][error2][0]
            else:
                if errors[error][0].startswith('This'):
                    message = error + errors[error][0][4:]
                else:
                    message =  errors[error][0]
    return {"message" : message}

class OrderViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']


    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            data._mutable = True
            username = data["username"]
            _profile = User.objects.get(username=username)
            add = Address.objects.get(user=_profile)
            customer = CustomerUser.objects.get(admin=add)
            admin = User.objects.get(id=self.request.user.pk)
            data["created_by"] = admin.pk
            data["user"] = customer.pk
            data["project"] = username
            order = Order.objects.filter(project=username)
            if not order:
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    order_instance = Order.objects.get(id=serializer.data['id'])
                    if data.get('other_component'):
                        for file in (data.get('other_component')).split(", "):
                            order_instance.other_component.add(file)
                            order_instance.save()
                    # context = {"data":serializer.data}
                    # return Response({"messsage":"Success"}, status=status.HTTP_200_OK)
                    return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
                else:
                    return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"messsage":"Order Already created"}, status=status.HTTP_400_BAD_REQUEST)

                

    def update(self, request, pk=None, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = self.request.user
            instance = self.get_object()
            data = self.request.data
            serializer = self.serializer_class(instance=instance,
                                                data=data, # or request.data
                                                context={'author': user},
                                                partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                invoice_instance=Invoice.objects.get(order=instance)
                if data.get('quantity'):    
                    quantity = data.get('quantity')
                    invoice_instance.quantity = quantity
                if data.get('rate'):
                    rate = data.get('rate')
                    invoice_instance.rate = rate
                    total_amount = int(rate) * int(quantity)
                    invoice_instance.total_amount = total_amount
                if data.get('due_date'):
                    invoice_instance.due_date = data['due_date']
                if data.get('full_pay_due_date'):
                    invoice_instance.full_pay_due_date = data['full_pay_due_date']
                 # add new line
                order_instance = Order.objects.get(id=pk)
                if data.get('assign_to'):
                    order_instance.assign_to.clear()
                    for file in (data.get('assign_to')).split(", "):
                        order_instance.assign_to.add(file)
                        order_instance.save()
                if data.get('other_component'):
                    order_instance.other_component.clear()
                    for file in (data.get('other_component')).split(", "):
                        order_instance.other_component.add(file)
                        order_instance.save()
                if self.request.FILES.getlist('packing_slip'):
                    for file in (self.request.FILES.getlist('packing_slip')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.packing_slip.add(file_string)
                # else:
                #     order_instance.packing_slip_reason = data.get('packing_slip_reason')
                if self.request.FILES.getlist('western_power'):
                    for file in (self.request.FILES.getlist('western_power')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.western_power.add(file_string)
                # else:
                #     order_instance.western_power_reason = data.get('western_power_reason')
                if self.request.FILES.getlist('switch_board'):
                    for file in (self.request.FILES.getlist('switch_board')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.switch_board.add(file_string)
                # else:
                #     order_instance.switch_board_reason = data.get('switch_board_reason')
                if self.request.FILES.getlist('panel_layout'):
                    for file in (self.request.FILES.getlist('panel_layout')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.panel_layout.add(file_string)
                        order_instance.save()
                # else:
                #     order_instance.panel_layout_reason = data.get('panel_layout_reason')
                #     order_instance.save()
                if self.request.FILES.getlist('extras'):
                    for file in (self.request.FILES.getlist('extras')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.extras.add(file_string)
                        order_instance.save()
                # add new line
                if data.get('pay') and int(data.get('pay')) > 0:
                    amount_paid=(invoice_instance.amount_paid + int(data.get('pay')))
                    amount_due = (total_amount - amount_paid)
                    invoice_instance.amount_paid = amount_paid
                    invoice_instance.amount_due = amount_due
                    Installation.objects.filter(order=invoice_instance.order).update(payment_due=amount_due)
                    history_instance = InvoiceHistory.objects.create(invoice=invoice_instance,invoice_title=invoice_instance.invoice_title, invoice_number=invoice_instance.invoice_number, 
                                            to_address=invoice_instance.to_address, from_address=invoice_instance.from_address, name=invoice_instance.name, email=invoice_instance.email, 
                                            quantity=invoice_instance.quantity, phone=invoice_instance.phone,
                                            rate=rate, total_amount=total_amount, 
                                            currency=invoice_instance.currency,
                                            amount_due=amount_due, 
                                            amount_paid=int(data.get('pay')),status=invoice_instance.status
                                            )
                    if (invoice_instance.total_amount) == (invoice_instance.amount_paid):
                        invoice_instance.status = 'Paid'
                    else:
                        invoice_instance.status = 'Pending'
                    invoice_instance.updated_by = self.request.user
                    invoice_instance.pay = 0
                    invoice_instance.save()
                    order_instance = Order.objects.get(id=pk)
                    logo = User.objects.get(is_main=True)
                    from_address1 = order_instance.from_address.address_line + " " + order_instance.from_address.street
                    from_address2 = order_instance.from_address.city + " " + order_instance.from_address.state + " " +  order_instance.from_address.postcode
                    to_address1 = order_instance.to_address.address_line + " " + order_instance.to_address.street
                    to_address2 = order_instance.to_address.city + " " + order_instance.to_address.state + " " +  order_instance.to_address.postcode
                    invoice_hist = InvoiceHistory.objects.filter(invoice=invoice_instance)
                    context = {"order":order_instance, "from_address":order_instance.from_address, "to_address":order_instance.to_address, "from_address1":from_address1, "from_address2":from_address2,"to_address1":to_address1, "to_address2":to_address2, "invoice":invoice_instance, "invoice_hist":invoice_hist, "logo":logo}
                    gen_pdf = GeneratePDF(context=context, type="invoice")
                    myfile = ContentFile(gen_pdf())
                    invoice_instance.invoice.save("invoice_"+str(invoice_instance.order.project)+".pdf", myfile)  

                    if history_instance:
                        history_instance.receipt.save("payslip_"+str(invoice_instance.order.project)+".pdf", myfile)
                        subject = str(invoice_instance.name)
                        payslip = []
                        slip = history_instance.receipt.url
                        payslip.append(slip)
                        message = "Dear" + str(invoice_instance.name) + ", " + "\nI hope you are doing well. " + "\npayslip_"
                        mail_response = Mailer(email_id=invoice_instance.email, filename=payslip, subject=subject, otp=message, type="otp")
                        _mail= mail_response()
                        print(_mail)
                return Response({"messsage":"Success"}, status=status.HTTP_200_OK)



    def retrieve(self, request, pk=None):
        instance = self.get_object()

        return Response(OrderDetailSerializer(instance).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()    
            return super(OrderViewSet, self).destroy(request, pk, *args, **kwargs)

class NonAdminOrderViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['created_at']
    # ordering = ['created_at']

    def filter_queryset(self, queryset):
        queryset = super(NonAdminOrderViewSet, self).filter_queryset(queryset)
        return queryset.order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if (_profile.user_type != "NON_ADMIN"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            _pass = str(random.randint(100000, 999999))
            data = self.request.data
            
            data._mutable = True
            while True:
                uid  = str(random.randint(10000000, 99999999))
                username = 'SR' + uid
                try:
                    user = User.objects.filter(username=username)
                    if user.exists() == False:
                        username = username
                        break
                except Exception as e:
                    continue
            data['username'] = username
            data['project'] = username
            data['user_type'] = "CUSTOMER"
            data['pin'] = _pass
            data['created_by'] = self.request.user.pk
            data['is_active'] = True
            user_serializer = UserSerializer(data=data)
            address_serializer = BillingAddressSerializer(data=data)
            customer_serializer = CustomerUserSerializer(data=data)
            order_serializer = OrderSerializer(data=data)
            data = {}
            if not user_serializer.is_valid():
                data["user_errors"] = dict(user_serializer.errors)
            if not order_serializer.is_valid():
                data["customer_errors"] = (order_serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if not customer_serializer.is_valid():
                data["customer_errors"] = (customer_serializer.errors)
            if data:
                return Response(
                    {"error": True, "errors": data},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user = user_serializer.save()
                user.set_password(_pass)
                user.save()
                address = address_serializer.save()
                address.user = user
                address.save()
                address_obj = customer_serializer.save()
                address_obj.admin = address
                address_obj.created_by = self.request.user
                address_obj.save()
                order_serializer.save()
                order_instance = Order.objects.get(id=order_serializer.data['id'])
                order_instance.created_by = request.user
                order_instance.user = address_obj
                order_instance.save()
                if data.get('other_component'):
                    for file in (data.get('other_component')).split(", "):
                        order_instance.other_component.add(file)
                        order_instance.save()
                if self.request.FILES.getlist('packing_slip'):
                    for file in (self.request.FILES.getlist('packing_slip')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.packing_slip.add(file_string)
                else:
                    order_instance.packing_slip_reason = data.get('packing_slip_reason')
                if self.request.FILES.getlist('western_power'):
                    for file in (self.request.FILES.getlist('western_power')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.western_power.add(file_string)
                else:
                    order_instance.western_power_reason = data.get('western_power_reason')
                if self.request.FILES.getlist('switch_board'):
                    for file in (self.request.FILES.getlist('switch_board')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.switch_board.add(file_string)
                else:
                    order_instance.switch_board_reason = data.get('switch_board_reason')
                if self.request.FILES.getlist('panel_layout'):
                    for file in (self.request.FILES.getlist('panel_layout')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.panel_layout.add(file_string)
                        order_instance.save()
                else:
                    order_instance.panel_layout_reason = data.get('panel_layout_reason')
                    order_instance.save()
                if self.request.FILES.getlist('extras'):
                    for file in (self.request.FILES.getlist('extras')):
                        file_string = DocumentOrderUpload.objects.create(file=file)
                        order_instance.extras.add(file_string)
                        order_instance.save()
                return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)

    # def update(self, request, pk=None, *args, **kwargs):
    #     _profile=User.objects.get(id=request.user.id)
    #     if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
    #         return Response(
    #             {"error": True, "errors": "Permission Denied"}, 
    #             status=status.HTTP_403_FORBIDDEN,
    #     )
    #     else:
    #         user = self.request.user
    #         instance = self.get_object()
    #         data = self.request.data
    #         serializer = self.serializer_class(instance=instance,
    #                                             data=data, # or request.data
    #                                             context={'author': user},
    #                                             partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             # add new line
    #             order_instance = Order.objects.get(id=pk)
    #             if data.get('other_component'):
    #                 order_instance.other_component.clear()
    #                 for file in (data.get('other_component')).split(", "):
    #                     order_instance.other_component.add(file)
    #                     order_instance.save()
    #             if self.request.FILES.getlist('packing_slip'):
    #                 for file in (self.request.FILES.getlist('packing_slip')):
    #                     file_string = DocumentOrderUpload.objects.create(file=file)
    #                     order_instance.packing_slip.add(file_string)
    #             # if data.get('packing_slip_reason'):
    #             #     order_instance.packing_slip_reason = data.get('packing_slip_reason')
    #             if self.request.FILES.getlist('western_power'):
    #                 for file in (self.request.FILES.getlist('western_power')):
    #                     file_string = DocumentOrderUpload.objects.create(file=file)
    #                     order_instance.western_power.add(file_string)
    #             # if data.get('western_power_reason'):
    #             #     order_instance.western_power_reason = data.get('western_power_reason')
    #             if self.request.FILES.getlist('switch_board'):
    #                 for file in (self.request.FILES.getlist('switch_board')):
    #                     file_string = DocumentOrderUpload.objects.create(file=file)
    #                     order_instance.switch_board.add(file_string)
    #             # if data.get('switch_board_reason'):
    #             #     order_instance.switch_board_reason = data.get('switch_board_reason')
    #             if self.request.FILES.getlist('panel_layout'):
    #                 for file in (self.request.FILES.getlist('panel_layout')):
    #                     file_string = DocumentOrderUpload.objects.create(file=file)
    #                     order_instance.panel_layout.add(file_string)
    #                     order_instance.save()
    #             # if data.get('panel_layout_reason'):
    #             #     order_instance.panel_layout_reason = data.get('panel_layout_reason')
    #             #     order_instance.save()
    #             if self.request.FILES.getlist('extras'):
    #                 for file in (self.request.FILES.getlist('extras')):
    #                     file_string = DocumentOrderUpload.objects.create(file=file)
    #                     order_instance.extras.add(file_string)
    #                     order_instance.save()
    #             return Response({"messsage":"Success"}, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "NON_ADMIN")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:    
            instance = self.get_object()
            context = {} 
            context['order'] = self.serializer_class(instance).data
            # query = request.GET.get('query', None)  # read extra data
            presite = PreSiteRisk.objects.get(order=instance)
            context["presite"] = PreSiteRiskSerializer(presite).data
            docs = Document.objects.get(order=instance)
            context["document"] = DocumentSerializer(docs).data
            grid = GridApproval.objects.get(order=instance)
            context["grid_approval"] = GridApprovalSerializer(grid).data
            invoice_instance=Invoice.objects.get(order=instance)
            context["invoice"] = InvoiceSerailizer(invoice_instance).data
            docs = Installation.objects.get(order=instance)
            context["install"] = InstallationSerializer(instance).data
            docs = InstallationDocument.objects.get(order=instance)
            context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
            docs = WarrantyDocument.objects.get(order=instance)
            context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
            return Response(context,
                            status=status.HTTP_200_OK)
        
    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "NON_ADMIN")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            cust = Order.objects.filter(created_by=self.request.user)
            return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
                                status=status.HTTP_200_OK)
        
    # def retrieve(self, request, pk=None):
    #     instance = self.get_object()
    #     context = {}
    #     context["order_details"] = OrderDetailSerializer(instance).data
    #     document_instance = Document.objects.get(order=instance)
    #     context["documents"] = DocumentSerializer(document_instance).data
    #     grid_instance=GridApproval.objects.get(order=instance)
    #     context["grid_approval"] = GridApprovalSerializer(grid_instance).data
    #     presite_instance = PreSiteRisk.objects.get(order=instance)
    #     context["presite"] = PreSiteRiskSerializer(presite_instance).data
    #     oi_serialized = {}
    #     if TakeAppointment.objects.filter(customer=instance).exists():
    #         booking_instance=TakeAppointment.objects.get(customer=instance)
    #         oi_serialized["id"] = booking_instance.pk
    #         oi_serialized["customer"] = booking_instance.customer.pk
    #         oi_serialized["appointment_date"] = booking_instance.appointment_date
    #         oi_serialized["appointment_time"] = booking_instance.appointment_time
    #         oi_serialized["appointment_appove"] = booking_instance.appointment_appove
    #         oi_serialized["approval_send"] = booking_instance.approval_send
    #         oi_serialized["reason"] = booking_instance.reason
    #         oi_serialized["cancelled"] = booking_instance.cancelled
    #         oi_serialized["created_by"] = booking_instance.created_by.pk
    #         oi_serialized["created_at"] = booking_instance.created_at
    #         # if booking_instance.updated_at:
    #         #     oi_serialized["updated_at"] = booking_instance.updated_at
    #         #     oi_serialized["updated_by"] = booking_instance.updated_by.pk
    #         context["booking_appointment"] = oi_serialized
    #     else:
    #         context["booking_appointment"] = oi_serialized
    #     installation_docs_instance = InstallationDocument.objects.get(order=instance)
    #     context["installation_document"] = InstallationDocumentSerializer(installation_docs_instance).data
    #     installation_instance=Installation.objects.get(order=instance)
    #     context["installation"] = InstallationSerializer(installation_instance).data
    #     warranty_docs_instance=WarrantyDocument.objects.get(order=instance)
    #     context["warranty_document"] = WarrantyDocumentSerializer(warranty_docs_instance).data
    #     invoice_instance = Invoice.objects.get(order=instance)
    #     context["invoice"] = InvoiceSerailizer(invoice_instance).data
    #     invoice_instance = InvoiceHistory.objects.filter(invoice=invoice_instance)
    #     context["invoice_history"] = InvoiceHistorySerializer(invoice_instance, many=True).data
    #     return Response(context,
    #                     status=status.HTTP_200_OK)
    def destroy(self, request, pk=None, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            return super(OrderViewSet, self).destroy(request, pk, *args, **kwargs)
        


        
        
class TakeAppointmentViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = TakeAppointment.objects.all()
    serializer_class = TakeAppointmentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "CUSTOMER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            data._mutable = True
            project = data["project"]
            customer = Order.objects.get(project=project)
            data["customer"] = customer.pk
            data["created_by"] = self.request.user.pk
            slots = TakeAppointment.objects.filter(appointment_date=data.get('appointment_date'))
            remaininig_slots = 6 - len(slots)
            if remaininig_slots > 0:
                if TakeAppointment.objects.filter(customer=customer, appointment_date=data.get('appointment_date')).exists():
                    return Response({"Error":True, "messsage":"Already Booked"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    serializer = self.serializer_class(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        appointment = serializer.data['id']
                        instance = TakeAppointment.objects.get(id=appointment)
                        installation = Installation.objects.get(order=customer)
                        installation.ins_booking_date = instance.created_at
                        installation.save()
                        slots = TakeAppointment.objects.filter(appointment_date=data.get('appointment_date'))
                        remaininig_slots = 6 - len(slots)
                        return Response({"messsage":"Success", "remainig_slots": remaininig_slots}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Error":True, "messsage":"Slots Full"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "CUSTOMER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            data=self.request.data
            serializer = UpdateTakeAppointmentSerializer(instance, data=data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                slots = TakeAppointment.objects.filter(appointment_date=data.get('appointment_date'))
                remaininig_slots = 6 - len(slots)
                return Response({"messsage":"Success","data":TakeAppointmentSerializer(instance).data, "remainig_slots": remaininig_slots}, status=status.HTTP_201_CREATED)
            else:
                return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
            
    def list(self, request, pk=None):
        instance = TakeAppointment.objects.all()
        return Response(self.serializer_class(instance, many=True).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            return super(TakeAppointmentViewSet, self).destroy(request, pk, *args, **kwargs)

# from datetime import datetime, timedelta   
# import pytz
# IST = pytz.timezone('Asia/Kolkata')
# _now = datetime.now(IST)
# __now = datetime.strftime(_now, "%Y-%m-%d")
# now = datetime.strptime(__now,"%Y-%m-%d")
# for day in range(1, 31): 
#   print(now+timedelta(days=day))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def slots_list(request):
    date_list  = []
    today = datetime.today()
    today = datetime.strftime(today, '%Y-%m-%d')
    start_date = datetime.strptime(today,"%Y-%m-%d")
    for day in range(1, 31):
        sample_dict = {}
        day = start_date+timedelta(days=day)
        day = datetime.strftime(day, '%Y-%m-%d')
        slots = TakeAppointment.objects.filter(appointment_date=day)
        remaininig_slots = 6 - len(slots)
        date = "date"
        slots = "remaininig_slots"
        sample_dict[date] = day
        sample_dict[slots] = remaininig_slots
        # print("sample_dict"*100, sample_dict)
        date_list.append(sample_dict)
    return Response({"data":date_list}, status=status.HTTP_200_OK)

class InstallerAvailViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = InstallerAvailibility.objects.all()
    serializer_class = InstallerAvailableSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
)


        else:
            data = self.request.data
            data._mutable = True
            start_time = parse('10:00:00 AM') #returns datetime object
            end_time = parse('5:00:00 PM')
            available_start_time = datetime.strftime(start_time, '%H:%M:%S').lower()
            available_end_time = datetime.strftime(end_time, '%H:%M:%S').lower()
            username = data["username"]
            data["is_anvailable"] = True
            data["available_start_time"] = available_start_time
            data["available_end_time"] = available_end_time
            _profile = User.objects.get(username=username)
            add = Address.objects.get(user=_profile)
            installer = InstallerUser.objects.get(admin=add)
            data["installer"] = installer.pk
            data["created_by"] = self.request.user.pk
            # _now = datetime.now()
            today = date.today()
            # __now = datetime.strftime(_now, "%Y-%m-%d %H:%M:%S")
            # now = datetime.strptime(__now,"%Y-%m-%d %H:%M:%S")
            if InstallerAvailibility.objects.filter(installer=installer, created_at__date=today).exists():
                install = InstallerAvailibility.objects.get(installer=installer, created_at__date=today)
                if data.get('available_days'):
                    install.available_days.clear()
                    for file in (data.get('available_days')).split(", "):
                    # for file in (data.get('available_days')):
                        try:
                            date_string = DateString.objects.get(date=file)
                            if date_string:
                                install.available_days.add(date_string)
                        except Exception as e:
                            date_string = DateString.objects.create(date=file)
                            install.available_days.add(date_string)
                    return Response({"messsage":"Success", "data":GetInstallerAvailableSerializer(install).data}, status=status.HTTP_201_CREATED)
            else:
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    install=InstallerAvailibility.objects.get(id=serializer.data["id"])
                    if data.get('available_days'):
                        install.available_days.clear()
                        # for file in (data.get('available_days')).split(", "):
                        for file in (data.get('available_days')):
                            try:
                                date_string = DateString.objects.get(date=file)
                                if date_string:
                                    install.available_days.add(date_string)
                            except Exception as e:
                                date_string = DateString.objects.create(date=file)
                                install.available_days.add(date_string)
                        return Response({"messsage":"Success", "data":GetInstallerAvailableSerializer(install).data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"messsage":"Success", "data":GetInstallerAvailableSerializer(install).data}, status=status.HTTP_201_CREATED)
                else:
                    return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,)
        else:
            instance = self.get_object()
            data=self.request.data  
            serializer = GetInstallerAvailableSerializer(instance, data=self.request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            install=InstallerAvailibility.objects.get(id=serializer.data["id"])
            if data.get('available_days'):
                date_list = []
                # for file in (data.get('available_days')).split(", "):
                for file in (data.get('available_days')):
                    # start = datetime.strptime(file, "%Y-%m-%d")
                    # _now = datetime.now()
                    # __now = datetime.strftime(_now, "%Y-%m-%d %H:%M:%S")
                    # now = datetime.strptime(__now,"%Y-%m-%d %H:%M:%S")
                    # startdate = start - now
                    # if startdate.days >= 1:
                    try:
                        date = DateString.objects.get(date=file)
                        if date:
                            install.available_days.remove(date)
                    except Exception as e:
                        date = DateString.objects.create(date=file)
                        install.available_days.remove(date)
                    # else:
                    #     sample_dict = {}
                    #     date = "date"
                    #     slots = "message"
                    #     sample_dict[date] = file
                    #     sample_dict[slots] = "you can't cancel on " + str(file) + ", " +"Otherwise you have to pay the penalty"
                    #     date_list.append(sample_dict)
                return Response({"messsage":"Success", "data":GetInstallerAvailableSerializer(install).data, "date_list": date_list}, status=status.HTTP_201_CREATED)
            return Response(GetInstallerAvailableSerializer(install).data)
            
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(GetInstallerAvailableSerializer(instance).data,
                        status=status.HTTP_200_OK)

    def list(self, request):
        today = datetime.today()
        today = datetime.strftime(today, '%Y-%m-%d')
        instance = InstallerAvailibility.objects.filter(is_anvailable=True)
        return Response(GetInstallerAvailableSerializer(instance, many=True).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            return super(InstallerAvailViewSet, self).destroy(request, pk, *args, **kwargs)
        



class InstallerHolidayViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = InstallerHoliday.objects.all()
    serializer_class = InstallerHolidaySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            data._mutable = True
            # start_time = parse('10:00:00 AM') #returns datetime object
            # end_time = parse('5:00:00 PM')
            # unavailable_start_time = datetime.strftime(start_time, '%H:%M:%S').lower()
            # unavailable_end_time = datetime.strftime(end_time, '%H:%M:%S').lower()
            username = data["username"]
            data["is_unavailable"] = True
            # data["unavailable_start_time"] = unavailable_start_time
            # data["unavailable_end_time"] = unavailable_end_time
            _profile = User.objects.get(username=username)
            add = Address.objects.get(user=_profile)
            installer = InstallerUser.objects.get(admin=add)
            data["installer"] = installer.pk
            data["created_by"] = self.request.user.pk
            # _now = datetime.now()
            today = date.today()
            # __now = datetime.strftime(_now, "%Y-%m-%d %H:%M:%S")
            # now = datetime.strptime(__now,"%Y-%m-%d %H:%M:%S")
            if InstallerHoliday.objects.filter(installer=installer, created_at__date=today).exists():
                install = InstallerHoliday.objects.get(installer=installer, created_at__date=today)
                if data.get('holiday_days'):
                    install.holiday_days.clear()
                    for file in (data.get('holiday_days')).split(", "):
                    # for file in (data.get('available_days')):
                        try:
                            date_string = DateString.objects.get(date=file)
                            if date_string:
                                install.holiday_days.add(date_string)
                        except Exception as e:
                            date_string = DateString.objects.create(date=file)
                            install.holiday_days.add(date_string)
                    return Response({"messsage":"Success", "data":GetInstallerHolidaySerializer(install).data}, status=status.HTTP_201_CREATED)
            else:
                serializer = self.serializer_class(data=data)
                if serializer.is_valid():
                    serializer.save()
                    install=InstallerHoliday.objects.get(id=serializer.data["id"])
                    if data.get('holiday_days'):
                        install.holiday_days.clear()
                        # for file in (data.get('available_days')).split(", "):
                        for file in (data.get('holiday_days')):
                            try:
                                date_string = DateString.objects.get(date=file)
                                if date_string:
                                    install.holiday_days.add(date_string)
                            except Exception as e:
                                date_string = DateString.objects.create(date=file)
                                install.holiday_days.add(date_string)
                        return Response({"messsage":"Success", "data":GetInstallerHolidaySerializer(install).data}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"messsage":"Success", "data":GetInstallerHolidaySerializer(install).data}, status=status.HTTP_201_CREATED)
                else:
                    return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            data=self.request.data  
            serializer = GetInstallerHolidaySerializer(instance, data=self.request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            install=InstallerHoliday.objects.get(id=serializer.data["id"])
            if data.get('holiday_days'):
                date_list = []
                # for file in (data.get('available_days')).split(", "):
                for file in (data.get('holiday_days')):
                    # start = datetime.strptime(file, "%Y-%m-%d")
                    # _now = datetime.now()
                    # __now = datetime.strftime(_now, "%Y-%m-%d %H:%M:%S")
                    # now = datetime.strptime(__now,"%Y-%m-%d %H:%M:%S")
                    # startdate = start - now
                    # if startdate.days >= 1:
                    try:
                        date = DateString.objects.get(date=file)
                        if date:
                            install.holiday_days.remove(date)
                    except Exception as e:
                        date = DateString.objects.create(date=file)
                        install.holiday_days.remove(date)
                    # else:
                    #     sample_dict = {}
                    #     date = "date"
                    #     slots = "message"
                    #     sample_dict[date] = file
                    #     sample_dict[slots] = "you can't cancel on " + str(file) + ", " +"Otherwise you have to pay the penalty"
                    #     date_list.append(sample_dict)
                return Response({"messsage":"Success", "data":GetInstallerHolidaySerializer(install).data, "date_list": date_list}, status=status.HTTP_201_CREATED)
            return Response(GetInstallerHolidaySerializer(install).data)
            
    def retrieve(self, request, pk=None):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(GetInstallerHolidaySerializer(instance).data,
                        status=status.HTTP_200_OK)

    def list(self, request):
        today = datetime.today()
        today = datetime.strftime(today, '%Y-%m-%d')
        instance = InstallerHoliday.objects.filter(is_anvailable=True)
        return Response(GetInstallerHolidaySerializer(instance, many=True).data,
                        status=status.HTTP_200_OK)

    def destroy(self, request, pk=None, *args, **kwargs):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            return super(InstallerAvailViewSet, self).destroy(request, pk, *args, **kwargs)

class InstallerOrderViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    def list(self, request):
        ids = []
        _profile = User.objects.get(id=request.user.id)
        customer = Order.objects.filter(assign_to=_profile)
        if customer.exists():
            for i in customer:
                ids.append(i.to_address.user.username)
        ord = Order.objects.filter(project__in=ids)
        return Response(self.serializer_class(ord.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)
    
class InstallerElectricianAvailibilityViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = InstallerAvailibility.objects.all()
    serializer_class = GetInstallerAvailableSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance=User.objects.get(pk=pk)
            address = Address.objects.get(user=instance)
            _profile = InstallerUser.objects.get(admin=address)
            customer = InstallerAvailibility.objects.filter(installer=_profile)
            if customer.exists():
                customer = InstallerAvailibility.objects.filter(installer=_profile).order_by('-id')[0]
                return Response(self.serializer_class(customer).data, 
                                status=status.HTTP_200_OK)
            return Response(customer, status=status.HTTP_200_OK)




# class InstallerElectricianAvailibilityListViewSet(ModelViewSet):
#     """
#     Create and Update Order if User is Admin or Superuser.
#     """
#     queryset = InstallerAvailibility.objects.all()
#     serializer_class = GetInstallerAvailableSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']

#     def retrieve(self, request, pk=None):
#         _profile=User.objects.get(id=request.user.id)
#         if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
#             return Response(
#                 {"error": True, "errors": "Permission Denied"}, 
#                 status=status.HTTP_403_FORBIDDEN,
#         )
#         else:
#             instance=User.objects.get(pk=pk)
#             address = Address.objects.get(user=instance)
#             _profile = InstallerUser.objects.get(admin=address)
#             customer = InstallerAvailibility.objects.filter(installer=_profile).order_by('-id')[0]
#             customer = InstallerAvailibility.objects.filter(installer=_profile).exclude(id=customer.id).order_by('-id')
#             return Response(self.serializer_class(customer, many=True).data,
#                             status=status.HTTP_200_OK)


class InstallerElectricianAvailibilityListViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = InstallerAvailibility.objects.all()
    serializer_class = GetInstallerAvailableSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance=User.objects.get(pk=pk)
            address = Address.objects.get(user=instance)
            _profile = InstallerUser.objects.get(admin=address)
            customer = InstallerAvailibility.objects.filter(installer=_profile).order_by('-id')[0]
            customer = InstallerAvailibility.objects.filter(installer=_profile).exclude(id=customer.id).order_by('-id')
            ls = customer.values('available_days')
            json_data = []
            context = {}
            for i in ls:
                date = DateString.objects.get(id=i['available_days'])
                json_data.append({
                        'id': date.pk,
                        'date': date.date
                    })
            context['available_days'] = json_data
            return Response(context, status=status.HTTP_200_OK)

# Listing of those orders assigned to installer
class InstallerElectricianOrderViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = Order.objects.all()  
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def list(self, request, pk=None):
        _profile=User.objects.get(id=self.request.user.id)
        if (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            ord = Order.objects.filter(assign_to=_profile, order_status='Pending')
            return Response(self.serializer_class(ord.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)
        
# List Of All Customer Users                      
class InstallerCompletedOrderView(ModelViewSet):
    """
    List of All Customer Users, view only user is admin or superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "INSTALLER")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:    
            instance = self.get_object()
            context = {} 
            context['order'] = self.serializer_class(instance).data
            if (instance.order_start_date) and (instance.order_end_date):
                wprking_time = working_time_function(instance.order_start_date, instance.order_end_date)
                context["working_hour"] = wprking_time
            # query = request.GET.get('query', None)  # read extra data
            presite = PreSiteRisk.objects.get(order=instance)
            context["presite"] = PreSiteRiskSerializer(presite).data
            docs = Document.objects.get(order=instance)
            context["document"] = DocumentSerializer(docs).data
            grid = GridApproval.objects.get(order=instance)
            context["grid_approval"] = GridApprovalSerializer(grid).data
            invoice_instance=Invoice.objects.get(order=instance)
            context["invoice"] = InvoiceSerailizer(invoice_instance).data
            docs = Installation.objects.get(order=instance)
            context["install"] = InstallationSerializer(instance).data
            docs = InstallationDocument.objects.get(order=instance)
            context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
            docs = WarrantyDocument.objects.get(order=instance)
            context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
            return Response(context,
                            status=status.HTTP_200_OK)
    def list(self, request, pk=None):
        _profile=User.objects.get(id=self.request.user.id)
        if (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            ord = Order.objects.filter(assign_to=_profile, order_status='Completed')
            return Response(self.serializer_class(ord.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)
            # cust = Order.objects.filter(order_status='Completed')
            # return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
            #                     status=status.HTTP_200_OK)
        

class CompanyOrderViewSet(ModelViewSet):
    """
    Create and Update Order if User is Admin or Superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=self.request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            customer = User.objects.get(pk=pk)
            ord = Order.objects.filter(created_by=customer)
            return Response(self.serializer_class(ord.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

    

# Apis for Customer User Panel
class OrderView(APIView):
    """
    Get Order Details for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        # order_instance=Order.objects.get(user=request.user)
        context = {}
        context["order"] = OrderDetailSerializer(order).data
        return Response(context, status=status.HTTP_200_OK)
    
# class GetOrderView(APIView):
    
#     """
#     Get Order Details for Authenticated User.
#     """
#     permission_classes = (IsAuthenticated,)

#     def get(self, request, format=None):
#         order = Order.objects.get(project=self.request.user.username)
#         # order_instance=Order.objects.get(user=request.user)
#         context = {}
#         context["order"] = OrderDetailSerializer(order).data
#         return Response(context, status=status.HTTP_200_OK)

# List Of All Customer Users                      
class NewOrderListWithoutAssignView(ModelViewSet):
    """
    List of All Customer Users, view only user is admin or superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:    
            instance = self.get_object()
            context = {} 
            context['order'] = self.serializer_class(instance).data
            # query = request.GET.get('query', None)  # read extra data
            presite = PreSiteRisk.objects.get(order=instance)
            context["presite"] = PreSiteRiskSerializer(presite).data
            docs = Document.objects.get(order=instance)
            context["document"] = DocumentSerializer(docs).data
            grid = GridApproval.objects.get(order=instance)
            context["grid_approval"] = GridApprovalSerializer(grid).data
            invoice_instance=Invoice.objects.get(order=instance)
            context["invoice"] = InvoiceSerailizer(invoice_instance).data
            docs = Installation.objects.get(order=instance)
            context["install"] = InstallationSerializer(instance).data
            docs = InstallationDocument.objects.get(order=instance)
            context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
            docs = WarrantyDocument.objects.get(order=instance)
            context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
            return Response(context,
                            status=status.HTTP_200_OK)
    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            cust = Order.objects.exclude(assign_to__isnull=False).exclude(order_status='Completed')
            return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
                                status=status.HTTP_200_OK)

# List Of All Customer Users                      
class AssignedGetOrderView(ModelViewSet):
    """
    List of All Customer Users, view only user is admin or superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:    
            instance = self.get_object()
            context = {} 
            context['order'] = self.serializer_class(instance).data
            # query = request.GET.get('query', None)  # read extra data
            presite = PreSiteRisk.objects.get(order=instance)
            context["presite"] = PreSiteRiskSerializer(presite).data
            docs = Document.objects.get(order=instance)
            context["document"] = DocumentSerializer(docs).data
            grid = GridApproval.objects.get(order=instance)
            context["grid_approval"] = GridApprovalSerializer(grid).data
            invoice_instance=Invoice.objects.get(order=instance)
            context["invoice"] = InvoiceSerailizer(invoice_instance).data
            docs = Installation.objects.get(order=instance)
            context["install"] = InstallationSerializer(instance).data
            docs = InstallationDocument.objects.get(order=instance)
            context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
            docs = WarrantyDocument.objects.get(order=instance)
            context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
            return Response(context,
                            status=status.HTTP_200_OK)
    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            cust = Order.objects.exclude(assign_to__isnull=True).exclude(order_status='Completed')
            return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
                                status=status.HTTP_200_OK)


# # List Of All Customer Users                      
# class GetOrderView(ModelViewSet):
#     """
#     List of All Customer Users, view only user is admin or superuser.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderDetailSerializer
#     permission_classes = (IsAuthenticated,)
#     http_method_names = ['get', ]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['created_at']
#     ordering = ['created_at']

#     def retrieve(self, request, pk=None):
#         _profile=User.objects.get(id=request.user.id)
#         # query = request.GET.get('query', None)
#         if ((_profile.user_type != "NON_ADMIN")):
#             return Response(
#                 {"error": True, "errors": "Permission Denied"}, 
#                 status=status.HTTP_403_FORBIDDEN,
#         )
#         else:    
#             instance = self.get_object()
#             context = {} 
#             context['order'] = self.serializer_class(instance).data
#             # query = request.GET.get('query', None)  # read extra data
#             presite = PreSiteRisk.objects.get(order=instance)
#             context["presite"] = PreSiteRiskSerializer(presite).data
#             docs = Document.objects.get(order=instance)
#             context["document"] = DocumentSerializer(docs).data
#             grid = GridApproval.objects.get(order=instance)
#             context["grid_approval"] = GridApprovalSerializer(grid).data
#             invoice_instance=Invoice.objects.get(order=instance)
#             context["invoice"] = InvoiceSerailizer(invoice_instance).data
#             docs = Installation.objects.get(order=instance)
#             context["install"] = InstallationSerializer(instance).data
#             docs = InstallationDocument.objects.get(order=instance)
#             context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
#             docs = WarrantyDocument.objects.get(order=instance)
#             context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
#             return Response(context,
#                             status=status.HTTP_200_OK)
#     def list(self, request):
#         _profile=User.objects.get(id=request.user.id)
#         # query = request.GET.get('query', None)
#         if ((_profile.user_type != "NON_ADMIN")):
#             return Response(
#                 {"error": True, "errors": "Permission Denied"}, 
#                 status=status.HTTP_403_FORBIDDEN,
#         )
#         else:
#             cust = Order.objects.filter(created_by=self.request.user)
#             return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
#                                 status=status.HTTP_200_OK)

class DocumentUploadViewSet(ModelViewSet):
    """
    Create and Update Order Documents And Photos if User is Admin or Superuser, Team, Non Admin, Installer.
    """
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', 'put', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    def create(self, request, *args, **kwargs):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            data._mutable = True 
            project = data["project"]
            order = Order.objects.get(project=project)
            data["order"] = order.pk
            data["created_by"] = self.request.user.pk
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"messsage":"Success", "data": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    # def update(self, request, pk=None, *args, **kwargs):
    #     _profile=User.objects.get(id=request.user.id)
    #     if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
    #         return Response(
    #             {"error": True, "errors": "Permission Denied"}, 
    #             status=status.HTTP_403_FORBIDDEN,
    #     )
    #     else:
    #         instance = self.get_object()
    #         data=self.request.data
    #         serializer = DocumentUploadSerializer(instance, data=data, partial=True)
    #         if serializer.is_valid(raise_exception=True):
    #             serializer.save()
    #             slots = DocumentUpload.objects.filter(appointment_date=data.get('appointment_date'))
    #             remaininig_slots = 6 - len(slots)
    #             return Response({"messsage":"Success","data":DocumentUploadSerializer(instance).data, "remainig_slots": remaininig_slots}, status=status.HTTP_201_CREATED)
    #         else:
    #             return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, pk=None):
        data = self.request.data
        upload_type = data["upload_type"]
        project = data["project"]
        order = Order.objects.get(project=project)
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            if project:
                instance = DocumentUpload.objects.filter(upload_type=upload_type, order=order)
                return Response(self.serializer_class(instance, many=True).data,
                                status=status.HTTP_200_OK)      
    # def list(self, request, pk=None):
    #     data = self.request.data
    #     project = data["upload_type"]
    #     _profile=User.objects.get(id=request.user.id)
    #     if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
    #         return Response(
    #             {"error": True, "errors": "Permission Denied"}, 
    #             status=status.HTTP_403_FORBIDDEN,
    #     )
    #     else:
    #         if project:
    #             instance = DocumentUpload.objects.filter(created_by=self.request.user.id, upload_type=project)
    #             return Response(self.serializer_class(instance, many=True).data,
    #                             status=status.HTTP_200_OK)
    def destroy(self, request, pk=None, *args, **kwargs):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            instance = self.get_object()
            return super(DocumentUploadViewSet, self).destroy(request, pk, *args, **kwargs)
        
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_uploaded_Docs(request):
#     try:
#         if request.method == 'GET':
#             data = request.data
#             project = data["upload_type"]
#             _profile=User.objects.get(id=request.user.id)
#             if ((_profile.user_type != "ADMIN") and (not request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
#                 return Response(
#                     {"error": True, "errors": "Permission Denied"}, 
#                     status=status.HTTP_403_FORBIDDEN,
#             )
#             else:
#                 if project:
#                     instance = DocumentUpload.objects.filter(created_by=request.user.id, upload_type=project)
#                     json_data = []
                    
#                     for x in instance:
#                         days = timeleft_function(x.created_at)
#                         json_data.append({
#                             "id": x.pk,
#                             "order": x.order.pk,
#                             "upload_type": x.upload_type,
#                             "title":x.title,
#                             "file": (request.build_absolute_uri())[:21]+str(x.file.url),
#                             "taken_from": x.taken_from,
#                             "created_at": x.created_at,
#                             "created_by": x.created_by.pk,
#                             "uploaded_at": days

#                         })
#                     print(json_data)
#                     # return Response({"status": True, "message": "success",}, json_data,  status=status.HTTP_200_OK)
#                     return JsonResponse(
#                     {"status": True, "message": "success", "data": json_data})
#     except Exception as e:
#         print(e)
#         return Response({"status": False, "message": "Service temporarily unavailable, try again later", },
#                             status=status.HTTP_503_SERVICE_UNAVAILABLE)



    # def create(self, request, *args, **kwargs):
    #     _profile=User.objects.get(id=request.user.id)
    #     if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN"):
    #         return Response(
    #             {"error": True, "errors": "Permission Denied"}, 
    #             status=status.HTTP_403_FORBIDDEN,
    #     )
    #     else:
    #         data = self.request.data
    #         data._mutable = True
    #         username = data["username"]
    #         _profile = User.objects.get(username=username)
    #         add = Address.objects.get(user=_profile)
    #         customer = Order.objects.get(admin=add)
    #         # admin = User.objects.get(id=self.request.user.pk)
    #         data["created_by"] = self.request.user
    #         data["user"] = customer.pk
    #         data["project"] = username
    #         order = Order.objects.filter(project=username)
    #         if not order:
    #             serializer = self.serializer_class(data=data)
    #             if serializer.is_valid():
    #                 serializer.save()
    #                 order_instance = Order.objects.get(id=serializer.data['id'])
    #                 order_instance.created_by = self.request.user
    #                 order_instance.save()
    #                 if data.get('other_component'):
    #                     for file in (data.get('other_component')).split(", "):
    #                         order_instance.other_component.add(file)
    #                         order_instance.save()
    #                 # context = {"data":serializer.data}
    #                 # return Response({"messsage":"Success"}, status=status.HTTP_200_OK)
    #                 return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
    #             else:
    #                 return Response(getFirstError(serializer.errors), status=status.HTTP_400_BAD_REQUEST)
    #         else:
    #             return Response({"messsage":"Order Already created"}, status=status.HTTP_400_BAD_REQUEST)



# List Of All Customer Users                      
class CompletedOrderView(ModelViewSet):
    """
    List of All Customer Users, view only user is admin or superuser.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def retrieve(self, request, pk=None):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:    
            instance = self.get_object()
            context = {} 
            context['order'] = self.serializer_class(instance).data
            if (instance.order_start_date) and (instance.order_end_date):
                wprking_time = working_time_function(instance.order_start_date, instance.order_end_date)
                context["working_hour"] = wprking_time
            # query = request.GET.get('query', None)  # read extra data
            presite = PreSiteRisk.objects.get(order=instance)
            context["presite"] = PreSiteRiskSerializer(presite).data
            docs = Document.objects.get(order=instance)
            context["document"] = DocumentSerializer(docs).data
            grid = GridApproval.objects.get(order=instance)
            context["grid_approval"] = GridApprovalSerializer(grid).data
            invoice_instance=Invoice.objects.get(order=instance)
            context["invoice"] = InvoiceSerailizer(invoice_instance).data
            docs = Installation.objects.get(order=instance)
            context["install"] = InstallationSerializer(instance).data
            docs = InstallationDocument.objects.get(order=instance)
            context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
            docs = WarrantyDocument.objects.get(order=instance)
            context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
            return Response(context,
                            status=status.HTTP_200_OK)
    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "TEAM")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            cust = Order.objects.filter(order_status='Completed')
            return Response(self.serializer_class(cust.order_by('created_at'), many=True).data,
                                status=status.HTTP_200_OK)
        


# class TeamUpdateOrderViewSet(ModelViewSet):
#     """
#     Create and Update Order if User is Admin or Superuser.
#     """
#     queryset = Order.objects.all()
#     serializer_class = TeamOrderSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['put', ]

#     def update(self, request, pk=None, *args, **kwargs):
#         _profile=User.objects.get(id=request.user.id)
#         if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NONE_ADMIN") and (_profile.user_type != "INSTALLER"):
#             return Response(
#                 {"error": True, "errors": "Permission Denied"}, 
#                 status=status.HTTP_403_FORBIDDEN,
#         )
#         else:
#             user = request.user
#             instance = self.get_object()
#             data = self.request.data
#             serializer = self.serializer_class(instance=instance,
#                                                 data=data, # or request.data
#                                                 context={'author': user},
#                                                 partial=True)
#             if serializer.is_valid(raise_exception=True):
#                 order_instance = serializer.save()
#                 if data.get('assign_to'):
#                     order_instance.assign_to.clear()
#                     for file in (data.get('assign_to')).split(", "):
#                         order_instance.assign_to.add(file)
#                         order_instance.save()
#                 return Response({"messsage":"Success", "order":serializer.data}, status=status.HTTP_200_OK)

# Team Panel Apis

# class InvoicingOrderViewSet(ModelViewSet):
#     """
#     Create and Update Order if User is Admin or Superuser.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['put',]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['created_at']
#     ordering = ['created_at']

#     def update(self, request, pk=None, *args, **kwargs):
#         _profile=User.objects.get(id=request.user.id)
#         if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN") and (_profile.user_type != "INSTALLER"):
#             return Response(
#                 {"error": True, "errors": "Permission Denied"}, 
#                 status=status.HTTP_403_FORBIDDEN,
#         )
#         else:
#             user = self.request.user
#             instance = self.get_object()
#             data = self.request.data
#             serializer = self.serializer_class(instance=instance,
#                                                 data=data, # or request.data
#                                                 context={'author': user},
#                                                 partial=True)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 invoice_instance=Invoice.objects.get(order=instance)
#                 if data['quantity']:
#                     quantity = data['quantity']
#                     invoice_instance.quantity = quantity
#                 if data['rate']:
#                     rate = data['rate']
#                     invoice_instance.rate = rate
#                     total_amount = int(rate) * int(quantity)
#                     invoice_instance.total_amount = total_amount
#                 if data.get('due_date'):
#                     invoice_instance.due_date = data['due_date']
#                 if data.get('full_pay_due_date'):
#                     invoice_instance.full_pay_due_date = data['full_pay_due_date']
#                 # add new line
#                 if data.get('pay') and int(data.get('pay')) > 0:
#                     amount_paid=(invoice_instance.amount_paid + int(data.get('pay')))
#                     amount_due = (total_amount - amount_paid)
#                     invoice_instance.amount_paid = amount_paid
#                     invoice_instance.amount_due = amount_due
#                     Installation.objects.filter(order=invoice_instance.order).update(payment_due=amount_due)
#                     history_instance = InvoiceHistory.objects.create(invoice=invoice_instance,invoice_title=invoice_instance.invoice_title, invoice_number=invoice_instance.invoice_number, 
#                                             to_address=invoice_instance.to_address, from_address=invoice_instance.from_address, name=invoice_instance.name, email=invoice_instance.email, 
#                                             quantity=invoice_instance.quantity, phone=invoice_instance.phone,
#                                             rate=rate, total_amount=total_amount, 
#                                             currency=invoice_instance.currency,
#                                             amount_due=amount_due, 
#                                             amount_paid=int(data.get('pay')),status=invoice_instance.status
#                                             )
#                 if (invoice_instance.total_amount) == (invoice_instance.amount_paid):
#                     invoice_instance.status = 'Paid'
#                 else:
#                     invoice_instance.status = 'Pending'
#                 invoice_instance.updated_by = self.request.user
#                 invoice_instance.pay = 0
#                 invoice_instance.save()
#                 order_instance = Order.objects.get(id=pk)
#                 logo = User.objects.get(is_main=True)
#                 from_address1 = order_instance.from_address.address_line + " " + order_instance.from_address.street
#                 from_address2 = order_instance.from_address.city + " " + order_instance.from_address.state + " " +  order_instance.from_address.postcode
#                 to_address1 = order_instance.to_address.address_line + " " + order_instance.to_address.street
#                 to_address2 = order_instance.to_address.city + " " + order_instance.to_address.state + " " +  order_instance.to_address.postcode
#                 invoice_hist = InvoiceHistory.objects.filter(invoice=invoice_instance)
#                 context = {"order":order_instance, "from_address":order_instance.from_address, "to_address":order_instance.to_address, "from_address1":from_address1, "from_address2":from_address2,"to_address1":to_address1, "to_address2":to_address2, "invoice":invoice_instance, "invoice_hist":invoice_hist, "logo":logo}
#                 gen_pdf = GeneratePDF(context=context, type="invoice")
#                 myfile = ContentFile(gen_pdf())
#                 invoice_instance.invoice.save("invoice_"+str(invoice_instance.order.project)+".pdf", myfile)  

#                 if history_instance:
#                     history_instance.receipt.save("payslip_"+str(invoice_instance.order.project)+".pdf", myfile)
#                     subject = str(invoice_instance.name)
#                     payslip = []
#                     slip = history_instance.receipt.url
#                     payslip.append(slip)
#                     message = "Dear" + str(invoice_instance.name) + ", " + "\nI hope you are doing well. " + "\npayslip_"
#                     mail_response = Mailer(email_id=invoice_instance.email, filename=payslip, subject=subject, otp=message, type="otp")
#                     _mail= mail_response()
#                 return Response({"messsage":"Success"}, status=status.HTTP_200_OK)

