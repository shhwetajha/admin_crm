from django.shortcuts import get_object_or_404, render
from rest_framework import status, filters
from common.serializer import *
from django.contrib.auth import login, logout
import random
from common.serializer import (
    InstallerUserSerializer,
    TeamSerializer,
    UserSerializer,
    NonAdminUserSerializer,
    CustomerUserSerializer,
)
from order.serializer import *
from django.conf import settings
from common.backend import EmailBackend
from django.utils.translation import gettext as _
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
import random
from django.core.mail import send_mail
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q, Max, Min, manager
from common.mailer import Mailer
from order.models import Order
# from order.views import getFirstError
# from common.two_factor_authentication import send_msg



class CompanyRegisterView(ModelViewSet):
    """
    Self Register api for company.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['post',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def create(self, request, *args, **kwargs):
        _pass = str(random.randint(100000, 999999))
        params = self.request.data
        params._mutable = True
        # Create NON_ADMIN
        if params:
            res = '16'+params['phone']
            params['username'] = res
            params['user_type'] = 'NON_ADMIN'
            params['pin'] = _pass
            params['is_active'] = True
            user_serializer = UserSerializer(data=params)
            non_admin_serializer = NonAdminUserSerializer(data=params)
            address_serializer = BillingAddressSerializer(data=params)
            data = {}
            if not user_serializer.is_valid(raise_exception=True):
                data["user_errors"] = dict(user_serializer.errors)
            if not non_admin_serializer.is_valid(raise_exception=True):
                data["non_admin_errors"] = (non_admin_serializer.errors,)
            if not address_serializer.is_valid(raise_exception=True):
                data["address_errors"] = (address_serializer.errors,)
            if data: 
                return Response(
                    {"error": True, "errors": data},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                user = user_serializer.save()
                address = address_serializer.save()
                address.user = user
                address.save()
                address_obj = non_admin_serializer.save()
                address_obj.admin = address
                address_obj.save()
                user.username = res
                user.set_password(_pass)
                user.save()
                instance = User.objects.get(is_main=True)
                subject =  "Registration Confirmation - Welcome to Solar 365"
                # email_from = settings.EMAIL_HOST_USER
                message = "Dear" + str(user.first_name)  + " " +  str(user.last_name) + ", " + str(address_obj.company_name) + " " + "has been Registered"
                # recipient_list = [instance.email]
                # send_mail(subject,message, email_from, recipient_list)
                mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="not_app_company_mail")
                _mail= mail_response()
                return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"messsage":"Failed"}, status=status.HTTP_400_BAD_REQUEST)


class UsersCreateView(ModelViewSet):
    """
    All types of users Register apis. Register Only User is Admin or Superuser.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def create(self, request, *args, **kwargs):
        user_type = request.GET.get("user_type", None)
        _pass = str(random.randint(100000, 999999))
        # params = request.query_params if len(request.data) == 0 else request.data
        params = self.request.data
        params._mutable = True
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            # Create ADMIN    
            if user_type == "ADMIN":
                if params: 
                    res = '15'+params['phone']
                    params['username'] = res
                    params['user_type'] = user_type
                    params['pin'] = _pass
                    params['is_active'] = True
                    params['created_by'] = self.request.user.pk
                    user_serializer = UserSerializer(data=params)
                    # address_serializer = BillingAddressSerializer(data=params)
                    data = {}
                    if not user_serializer.is_valid():
                        data["user_errors"] = dict(user_serializer.errors)
                    # if not address_serializer.is_valid():
                    #     data["address_errors"] = (address_serializer.errors,)
                    if data:
                        return Response(
                            {"error": True, "errors": data},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        # address = address_serializer.save()
                        user = user_serializer.save()
                        instance = user_serializer.data['id']
                        address = Address.objects.get(user=instance)
                        # user.username = res
                        # user.user_type = user_type
                        user.is_active = True
                        user.is_staff = True
                        user.is_superuser = True
                        user.set_password(_pass)
                        # user.pin = _pass
                        user.save()
                        serializer = BillingAddressSerializer(instance=address, data=params, partial=True)
                        if serializer.is_valid():
                            serializer.save()
                            return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
                        return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
            # Create Team
            if user_type == "TEAM":
                if params:
                    res = '15'+params['phone']
                    params['username'] = res
                    params['user_type'] = user_type
                    params['pin'] = _pass
                    params['is_active'] = True
                    params['created_by'] = self.request.user.pk
                    user_serializer = UserSerializer(data=params)
                    team_serializer = TeamSerializer(data=params)
                    address_serializer = BillingAddressSerializer(data=params)
                    data = {}
                    if not user_serializer.is_valid():
                        data["user_errors"] = dict(user_serializer.errors)
                    if not team_serializer.is_valid():
                        data["team_errors"] = (team_serializer.errors,)
                    if not address_serializer.is_valid():
                        data["address_errors"] = (address_serializer.errors,)
                    if data:
                        return Response(
                            {"error": True, "errors": data},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        user = user_serializer.save()
                        address = address_serializer.save()
                        address.user = user
                        address.save()
                        address_obj = team_serializer.save()
                        address_obj.admin = address
                        address_obj.is_online = True
                        # address_obj.created_by = request.user
                        # address_obj.has_sales_access=True
                        # address_obj.has_marketing_access =True
                        # address_obj.is_organization_admin =True
                        address_obj.save()
                        # user.username = res
                        # user.user_type = user_type
                        user.set_password(_pass)
                        # user.pin = _pass
                        # user.is_active = True
                        user.save()
                        # subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "you are successfully registered"
                        subject = "Registration Confirmation - Welcome to Solar 365"
                        message = "Username : " + str(user.username) + "\nPassword : " + str(user.pin)
                        mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="team_registration_mail")
                        _mail= mail_response()
                        return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
            # Create INSTALLER
            if user_type == "INSTALLER":
                if params:
                    res = '15'+params['phone']
                    params['username'] = res
                    params['user_type'] = user_type
                    params['pin'] = _pass
                    params['is_active'] = True
                    params['created_by'] = self.request.user.pk
                    user_serializer = UserSerializer(data=params)
                    installer_serializer = InstallerUserSerializer(data=params)
                    address_serializer = BillingAddressSerializer(data=params)
                    data = {}
                    if not user_serializer.is_valid():
                        data["user_errors"] = dict(user_serializer.errors)
                    if not installer_serializer.is_valid():
                        data["installer_errors"] = (installer_serializer.errors,)
                    if not address_serializer.is_valid():
                        data["address_errors"] = (address_serializer.errors,)

                    if data:
                        return Response(
                            {"error": True, "errors": data},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        user = user_serializer.save()
                        address = address_serializer.save()
                        address.user = user
                        address.save()
                        address_obj = installer_serializer.save()
                        address_obj.admin = address
                        # address_obj.created_by = request.user
                        address_obj.save()
                        # user.username = res
                        # user.user_type = user_type
                        user.set_password(_pass)
                        # user.pin = _pass
                        # user.is_active = True
                        user.save()
                        # subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "you are successfully registered"
                        subject = "Registration Confirmation - Welcome to Solar 365"
                        # email_from = settings.EMAIL_HOST_USER
                        message = "Username : " + str(user.username) + "\nPassword : " + str(user.pin)
                        # recipient_list = [instance.email]
                        # send_mail(subject,message, email_from, recipient_list)
                        mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="installer_registration_mail")
                        _mail= mail_response()
                        # return True
                        return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
            # Create NON_ADMIN
            if user_type == "NON_ADMIN":
                if params:
                    res = '15'+params['phone']
                    params['username'] = res
                    params['user_type'] = user_type
                    params['pin'] = _pass
                    params['is_active'] = True
                    params['has_approve'] = True
                    params['created_by'] = self.request.user.pk
                    user_serializer = UserSerializer(data=params)
                    non_admin_serializer = NonAdminUserSerializer(data=params)
                    address_serializer = BillingAddressSerializer(data=params)
                    data = {}
                    if not user_serializer.is_valid():
                        data["user_errors"] = dict(user_serializer.errors)
                    if not non_admin_serializer.is_valid():
                        data["non_admin_errors"] = (non_admin_serializer.errors,)
                    if not address_serializer.is_valid():
                        data["address_errors"] = (address_serializer.errors,)
                    if data:
                        return Response(
                            {"error": True, "errors": data},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        user = user_serializer.save()
                        address = address_serializer.save()
                        address.user = user
                        address.save()
                        address_obj = non_admin_serializer.save()
                        address_obj.admin = address
                        address_obj.has_customer_access =True
                        address_obj.created_by = self.request.user
                        address_obj.has_installer_access = True
                        address_obj.save()
                        user.username = res
                        user.has_customer_access=True
                        user.has_installer_access=True
                        # user.user_type = user_type
                        # user.pin = _pass
                        user.set_password(_pass)
                        # user.is_active = True
                        user.save()
                        if (user.has_approve == True):
                            # subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "you are successfully registered"
                            subject = "Registration Confirmation - Welcome to Solar 365"
                            message = "Dear" + str(user.first_name)  + " " +  str(user.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(user.username) + "and, " + "\nPassword : " + str(user.pin)
                            mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="company_mail")
                            _mail= mail_response()
                        else:
                            # subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "you are successfully registered"
                            subject = "Registration Confirmation - Welcome to Solar 365"
                            message = "Thanks for using the Solar365" + "\nI hope you are doing well, " + "I want to inform that when admin approve your account then you can Signin. "
                            mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="not_app_company_mail")
                            _mail= mail_response()
                        return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)
            # Create CUSTOMER
            if user_type == "CUSTOMER":
                if params:
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
                    params['username'] = username
                    params['user_type'] = user_type
                    params['pin'] = _pass
                    params['created_by'] = self.request.user.pk
                    params['is_active'] = True
                    user_serializer = UserSerializer(data=params)
                    customer_serializer = CustomerUserSerializer(data=params)
                    address_serializer = BillingAddressSerializer(data=params)
                    data = {}
                    if not user_serializer.is_valid():
                        data["user_errors"] = dict(user_serializer.errors)
                    if not customer_serializer.is_valid():
                        data["customer_errors"] = (customer_serializer.errors)
                    if not address_serializer.is_valid():
                        data["address_errors"] = (address_serializer.errors)
                    if data:
                        return Response(
                            {"error": True, "errors": data},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    else:
                        user = user_serializer.save()
                        address = address_serializer.save()
                        address.user = user
                        address.save()
                        address_obj = customer_serializer.save()
                        address_obj.admin = address
                        address_obj.created_by = self.request.user
                        address_obj.save()
                        # user.username = username
                        user.set_password(_pass)
                        # user.user_type = user_type
                        # user.pin = _pass
                        # user.is_active = True
                        user.save()
                        return Response({"messsage":"Success"}, status=status.HTTP_201_CREATED)

# Update Only Customer User and Main Admin
class UpdateUserProfileViewSet(ModelViewSet):
    """
    All types of users Profile Update apis. Update Only User is Admin or Superuser.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['put', 'get']

    def update(self, request, pk=None, *args, **kwargs):
        _profile=User.objects.get(id=pk)
        user = request.user
        instance = self.get_object()
        params = self.request.data
        serializer = self.serializer_class(instance=instance,
                                            data=params, # or request.data
                                            context={'author': user},
                                            partial=True)
        billing_instance = Address.objects.get(user=instance)
        address_serializer = BillingAddressSerializer(instance=billing_instance, data=params, context={'author': user}, partial=True)
        
        if (_profile.user_type == "ADMIN"):
            data = {}
            if not serializer.is_valid():
                data["user_errors"] = dict(serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if data:
                return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
            else:
                address_obj = serializer.save()
                address_serializer.save()
                serializer = UserProfileSerializer(address_obj)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        if (_profile.user_type == "TEAM"):
            non_Admin_instance = Team.objects.get(admin=billing_instance)
            non_admin_serializer = TeamSerializer(instance=non_Admin_instance, data=params, context={'author': user}, partial=True)
            data = {}
            if not serializer.is_valid():
                data["user_errors"] = dict(serializer.errors)
            if not non_admin_serializer.is_valid():
                data["non_Admin_errors"] = (non_admin_serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if data:
                return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
            else:
                serializer.save()
                address_serializer.save()
                address_obj = non_admin_serializer.save()
                address_obj.updated_by = self.request.user
                address_obj.save()
                serializer = TeamProfileSerializer(address_obj)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        if (_profile.user_type == "INSTALLER"):
            non_Admin_instance = InstallerUser.objects.get(admin=billing_instance)
            non_admin_serializer = InstallerUserSerializer(instance=non_Admin_instance, data=params, context={'author': user}, partial=True)
            data = {}
            if not serializer.is_valid():
                data["user_errors"] = dict(serializer.errors)
            if not non_admin_serializer.is_valid():
                data["non_Admin_errors"] = (non_admin_serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if data:
                return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
            else:
                serializer.save()
                address_serializer.save()
                address_obj = non_admin_serializer.save()
                address_obj.updated_by = self.request.user
                address_obj.save()
                serializer = InstallerProfileSerializer(address_obj)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
        if (_profile.user_type == "NON_ADMIN"):
            non_Admin_instance = NonAdminUser.objects.get(admin=billing_instance)
            non_admin_serializer = NonAdminUserSerializer(instance=non_Admin_instance, data=params, context={'author': user}, partial=True)
            data = {}
            if not serializer.is_valid():
                data["user_errors"] = dict(serializer.errors)
            if not non_admin_serializer.is_valid():
                data["none_Admin_errors"] = (non_admin_serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if data:
                return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
            else:
                user = serializer.save()
                address_serializer.save()
                address_obj = non_admin_serializer.save()
                address_obj.updated_by = self.request.user
                address_obj.save()
                serializer = NonAdminProfileSerializer(address_obj)
                if params.get('has_approve'):
                    if user.has_approve == True:
                        subject = "Registration Confirmation - Welcome to Solar 365"
                        # subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "you are successfully registered"
                        # email_from = settings.EMAIL_HOST_USER
                        message = "Dear" + str(user.first_name)  + " " +  str(user.last_name) + ", " + "\nI hope you are doing well. " + "I want to inform you that the head has approved your" + "Username : " + str(user.username) + "and, " + "\nPassword : " + str(user.pin)
                        # recipient_list = [user.email]
                        # send_mail(subject,message, email_from, recipient_list)
                        mail_response = Mailer(email_id=user.email, subject=subject, otp=message, type="company_mail")
                        _mail= mail_response()
                        return Response(data=serializer.data, status=status.HTTP_200_OK)
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            
        # if (_profile.user_type == "CUSTOMER"):
        #     data = {}
        #     if not serializer.is_valid():
        #         data["user_errors"] = dict(serializer.errors)
        #     if not address_serializer.is_valid():
        #         data["address_errors"] = (address_serializer.errors)
        #     if data:
        #         return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
        #     else:
        #         serializer.save()
        #         address_obj = address_serializer.save()
        #         return Response(data=serializer.data, status=status.HTTP_200_OK)

        if (_profile.user_type == "CUSTOMER"):
            customer_instance = CustomerUser.objects.get(admin=billing_instance)
            customer_serializer = CustomerUserSerializer(instance=customer_instance, data=params, context={'author': user}, partial=True)
            data = {}
            if not serializer.is_valid():
                data["user_errors"] = dict(serializer.errors)
            if not customer_serializer.is_valid():
                data["customer_errors"] = (customer_serializer.errors)
            if not address_serializer.is_valid():
                data["address_errors"] = (address_serializer.errors)
            if data:
                return Response({"error": True, "errors": data}, status=status.HTTP_400_BAD_REQUEST, )
            else:
                serializer.save()
                address_serializer.save()
                address_obj = customer_serializer.save()
                address_obj.updated_by = request.user
                address_obj.save()
                serializer = CustomerProfileSerializer(address_obj)
                return Response(data=serializer.data, status=status.HTTP_200_OK)

# List Of All Admin Users
class GetAdminUserProfileViewSet(ModelViewSet):
    """
    List of All Admin Users, view only user is admin or superuser.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = User.objects.filter(user_type='ADMIN')
            query_set = Address.objects.filter(Q(user__in=user))
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                        status=status.HTTP_200_OK)

# List Of All Team and Installer Users
class GetUserProfileViewSet(ModelViewSet):
    """
    List of All Team and Installer Users, view only user is admin or superuser.
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "NON_ADMIN"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            # user = User.objects.filter(user_type__in=['INSTALLER','TEAM'])
            user = User.objects.filter(user_type__in=['INSTALLER'])
            return Response(self.serializer_class(user.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

# List Of All Team and Installer Users
class GetNonAdminUserProfileViewSet(ModelViewSet):
    """
    List of All None Admin Users, view only user is admin or superuser.
    """
    queryset = NonAdminUser.objects.all()
    serializer_class = NonAdminProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = User.objects.filter(user_type='NON_ADMIN', has_approve=True)
            add = Address.objects.filter(Q(user__in=user))
            query_set = NonAdminUser.objects.filter(Q(admin__id__in=add))
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

# List Of All Team and Installer Users
class GetNonAdminUserWithoutApproveProfileViewSet(ModelViewSet):
    """
    List of All None Admin Users, view only user is admin or superuser.
    """
    queryset = NonAdminUser.objects.all()
    serializer_class = NonAdminProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = User.objects.filter(user_type='NON_ADMIN', has_approve=False)
            add = Address.objects.filter(Q(user__in=user))
            query_set = NonAdminUser.objects.filter(Q(admin__id__in=add))
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

# List Of All Innstaller Users
class GetInstallerUserProfileViewSet(ModelViewSet):
    """
    List of All Installer Users, view only user is admin or superuser.
    """
    queryset = InstallerUser.objects.all()
    serializer_class = InstallerProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser) and (_profile.user_type != "TEAM") and (_profile.user_type != "INSTALLER")) :
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            context = {}
            user = User.objects.filter(user_type='INSTALLER')
            add = Address.objects.filter(Q(user__in=user))
            query_set = InstallerUser.objects.filter(Q(admin__id__in=add))
            if query_set.filter(department='Installer'):
                context['Installer'] = self.serializer_class(query_set.filter(department='Installer').order_by('created_at'), many=True).data
            if query_set.filter(department="Electrician"):
                context['Electrician'] = self.serializer_class(query_set.filter(department="Electrician").order_by('created_at'), many=True).data
            return Response(context,
                            status=status.HTTP_200_OK)
# List Of All Team Users
class GetTeamUserProfileViewSet(ModelViewSet):
    """
    List of All Team Users, view only user is admin or superuser.
    """
    queryset = Team.objects.all()
    serializer_class = TeamProfileSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = User.objects.filter(user_type='TEAM')
            add = Address.objects.filter(Q(user__in=user))
            query_set = Team.objects.filter(Q(admin__id__in=add))
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

# List Of All Customer Users                      
class GetCustomerUserProfileViewSet(ModelViewSet):
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

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            user = User.objects.filter(user_type='CUSTOMER')
            add = Address.objects.filter(Q(user__in=user))
            query_set = Order.objects.filter(Q(admin__id__in=add))
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)


# List Of All Customer Users                      
class CustomerUserProfileViewSet(ModelViewSet):
    """
    List of All Customer Users, view only user type is non admin.
    """
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def list(self, request):
        _profile=User.objects.get(id=request.user.id)
        # query = request.GET.get('query', None)
        if ((_profile.user_type != "NON_ADMIN")):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            query_set = Order.objects.filter(created_by=self.request.user)
            return Response(self.serializer_class(query_set.order_by('created_at'), many=True).data,
                            status=status.HTTP_200_OK)

# # Login For all types of users
# class LoginView(APIView):
#     """
#     Login Api for All types of users
#     """
#     @csrf_exempt
#     def post(self, request, format=None):
#         _data = request.data
#         username = _data.get('username', None)
#         password = _data.get("password", None)
#         try:
#             auth = EmailBackend.authenticate(request, username=username, password=password)
#             if auth:
#                 if Token.objects.filter(user=auth).exists():
#                     _token = Token.objects.get(user=auth)
#                     _token.delete()
#                     token = Token.objects.create(user=auth)
#                     login(request, auth)
#                     _data = UserProfileSerializer(auth).data
#                     return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
#                 else:
#                     token = Token.objects.create(user=auth)
#                     login(request, auth)
#                     _data = UserProfileSerializer(auth).data
#                     return Response({"user":_data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"message":'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
#         except User.DoesNotExist:
#             return Response({'message':'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)

# Forgot Password for All Types of users
class ForgotPassword(APIView):
    """
    Forgot Password For All Types of users.
    """
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        
        email = request.data.get('email', None)
        # username = request.data.get('username', None)
        try:
            # user = User.objects.get(username=username)
            user = User.objects.get(email=email)
            _pass = str(random.randint(100000, 999999))
            user.set_password(_pass)
            user.pin = _pass
            user.save()
            subject = "Congratulations!" +  " " + str(user.first_name)  + " " +  str(user.last_name) + " " + "Pin Reset Successfully!"
            email_from = settings.EMAIL_HOST_USER
            message = "Project : "+str(user.username)+"\nPin : "+ user.pin
            recipient_list = [user.email]
            send= (subject,message, email_from, recipient_list)
            return Response(
                {"message":"Password Reset Successfully! ", "username": user.username, "password": _pass}, 
                status=status.HTTP_200_OK
                )
        except User.DoesNotExist:
            return Response(
                {"message":"User Does Not exist."}, 
                status=status.HTTP_404_NOT_FOUND
                )

# Logout All types of Users           
class Logout(APIView):
    """
    Logout Api for All Types of User If User Authenticated.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        token.delete()
        logout(request)
        return Response({"message":"Logout successfully."},status=status.HTTP_200_OK)

# # view for assign to user for example installer
# class CustomerUsersViewSet(ModelViewSet):
#     """
#     List All Customer Details Only For Installer
#     """
#     serializer_class = OrderDetailSerializer
#     permission_classes = [IsAuthenticated]
#     http_method_names = ['get']
    
#     def get_queryset(self):
#         return Order.objects.filter(assign_to=self.request.user).order_by('-created_at')

# # view for assign to user for example team and installer
# class CustomerUsersViewSet(ModelViewSet):

# 	serializer_class = CustomerProfileSerializer
# 	permission_classes = [IsAuthenticated]
# 	http_method_names = ['get']

# 	def get_queryset(self):
# 		return Order.objects.filter(assign_to=self.request.user)
    

# Change Password for all Tyoes of users
class ChangePassword(APIView):
    """
    Change Password For All Types of Users if User is Authenticated
    """
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        current_password = request.data.get('current_password', None)
        password = request.data.get('password', None)
        confirm_password = request.data.get('confirm_password', None)
        # id = request.data.get("id", None)
        id = request.user.id
        user_instance = User.objects.get(id=id)
        if current_password:
            if user_instance.check_password(current_password):
                if password and confirm_password:
                    if password == confirm_password:
                        SpecialSym =['$', '@', '#', '%', '-', '_']
                        if(len(str(password)) < 8):
                            return Response({"message":"Password should be at least 8 characters."}, status=status.HTTP_400_BAD_REQUEST)
                        elif (len(str(password)) > 32):
                            return Response({"message":"Password should be not be greater than 20 characters."}, status=status.HTTP_400_BAD_REQUEST)
                        elif(not any(char.isdigit() for char in str(password))):
                            return Response({"message":"Password should have at least one numeral."}, status=status.HTTP_400_BAD_REQUEST)
                        elif (not any(char.isupper() for char in str(password))):
                            return Response({"message":"Password should have at least one uppercase letter."}, status=status.HTTP_400_BAD_REQUEST)
                        elif (not any(char.islower() for char in str(password))):
                            return Response({"message":"Password should have at least one lowercase letter."}, status=status.HTTP_400_BAD_REQUEST)
                        elif (not any(char in SpecialSym for char in str(password))):
                            return Response({"message":"Password should have at least one of the special characters."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            user_instance.set_password(password)
                            user_instance.pin = password
                            user_instance.save()
                            return Response({"message":'Password changed.'}, status=status.HTTP_200_OK)
                    else:
                        return Response({"message":"Password and confirm password are not matched."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"message":"Please enter a valid password."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Current password wrong."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if password and confirm_password:
                if password == confirm_password:
                    SpecialSym =['$', '@', '#', '%', '-', '_']
                    if(len(str(password)) < 8):
                        return Response({"message":"Password should be at least 8 characters."}, status=status.HTTP_400_BAD_REQUEST)
                    elif (len(str(password)) > 32):
                        return Response({"message":"Password should be not be greater than 20 characters."}, status=status.HTTP_400_BAD_REQUEST)
                    elif(not any(char.isdigit() for char in str(password))):
                        return Response({"message":"Password should have at least one numeral."}, status=status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.isupper() for char in str(password))):
                        return Response({"message":"Password should have at least one uppercase letter."}, status=status.HTTP_400_BAD_REQUEST)
                    elif (not any(char.islower() for char in str(password))):
                        return Response({"message":"Password should have at least one lowercase letter."}, status=status.HTTP_400_BAD_REQUEST)
                    elif (not any(char in SpecialSym for char in str(password))):
                        return Response({"message":"Password should have at least one of the special characters."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user_instance.set_password(password)
                        user_instance.pin = password
                        user_instance.save()
                        return Response({"message":'Password changed.'}, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"Password and confirm password are not matched."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message":"Please enter a valid password."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def username_list(request):
    """
    List those Customer Username Order is not created
    """
    ids = []
    # cust = CustomerUser.objects.all()
    cust = CustomerUser.objects.all()
    if cust.exists():
        for i in cust:
            try:
                ord = Order.objects.get(project=i.admin.user.username)
                if ord:
                    pass
            except Exception as e:
                ids.append(i.admin.user.username)
        return Response({"data":ids}, status=status.HTTP_200_OK)
    return Response({"data":ids}, status=status.HTTP_200_OK)



# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def username_list_non_admin(request):
#     """
#     List those Customer Username Order is not created which is registered by company
#     """
#     ids = []
#     # cust = CustomerUser.objects.all()
#     cust = CustomerUser.objects.filter(created_by=request.user)
#     if cust.exists():
#         for i in cust:
#             try:
#                 ord = Order.objects.get(project=i.admin.user.username)
#                 if ord:
#                     pass
#             except Exception as e:
#                 ids.append(i.admin.user.username)
#         return Response({"data":ids}, status=status.HTTP_200_OK)
#     return Response({"data":ids}, status=status.HTTP_200_OK)





# Login For all types of users
class LoginView(APIView):
    """
    Login Api for All types of users
    """
    @csrf_exempt
    def post(self, request, format=None):
        _data = request.data
        username = _data.get('username', None)
        password = _data.get("password", None)
        try:
            auth = EmailBackend.authenticate(request, username=username, password=password)
            if auth:
                if Token.objects.filter(user=auth).exists():
                    _token = Token.objects.get(user=auth)
                    _token.delete()
                    token = Token.objects.create(user=auth)
                    login(request, auth)
                    # Profile Team
                    if auth.user_type == "ADMIN":
                        _data = UserProfileSerializer(auth).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    # Profile Team
                    if auth.user_type == "TEAM":
                        address = Address.objects.get(user=auth)
                        team = Team.objects.get(admin=address)
                        _data = TeamProfileSerializer(team).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    # Profile INSTALLER
                    if auth.user_type == "INSTALLER":
                        address = Address.objects.get(user=auth)
                        installer = InstallerUser.objects.get(admin=address)
                        _data = InstallerProfileSerializer(installer).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    # Profile NON_ADMIN
                    if auth.user_type == "NON_ADMIN":
                        address = Address.objects.get(user=auth)
                        company = NonAdminUser.objects.get(admin=address)
                        _data = NonAdminProfileSerializer(company).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    # Profile CUSTOMER
                    if auth.user_type == "CUSTOMER":
                        _data = UserProfileSerializer(auth).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                else:
                    token = Token.objects.create(user=auth)
                    login(request, auth)

                    # Profile Team
                    if auth.user_type == "ADMIN":
                        _data = UserProfileSerializer(auth).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    
                    # Profile Team
                    if auth.user_type == "TEAM":
                        address = Address.objects.get(user=auth)
                        team = Team.objects.get(admin=address)
                        _data = TeamProfileSerializer(team).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    
                    # Profile INSTALLER
                    if auth.user_type == "INSTALLER":
                        address = Address.objects.get(user=auth)
                        installer = InstallerUser.objects.get(admin=address)
                        _data = InstallerProfileSerializer(installer).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    
                    # Profile NON_ADMIN
                    if auth.user_type == "NON_ADMIN":
                        address = Address.objects.get(user=auth)
                        company = NonAdminUser.objects.get(admin=address)
                        _data = NonAdminProfileSerializer(company).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
                    
                    # Profile CUSTOMER
                    if auth.user_type == "CUSTOMER":
                        _data = UserProfileSerializer(auth).data
                        return Response({"user": _data,"message":'Success', "token":token.key}, status=status.HTTP_200_OK)
            else:
                return Response({"message":'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message':'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)