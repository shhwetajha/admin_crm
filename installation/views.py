from rest_framework import status, filters
from .serializer import (
    InstallationSerializer, InstallationDocumentSerializer, WarrantyDocumentSerializer, UserReferralSerializer \
        , UserReferralSuccessSerializer, InstallationDetailSerializer
)
from .models import Installation, InstallationDocument, WarrantyDocument, UserReferral, ReferralSuccess
from rest_framework.views import APIView
# from grid_approval.models import *
from common.models import User, Address
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from order.models import Order
from invoice.models import Invoice
from common.mailer import Mailer

class InstallView(APIView):
    """
    Get Installation Details for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        invoice_instance=Installation.objects.get(order=order)
        context = {}
        context["install"] = InstallationSerializer(invoice_instance).data
        return Response(context, status=status.HTTP_200_OK)

class InstallUpdateView(ModelViewSet):
    """
    Get and Update Documents for Authenticated User.
    """
    queryset = Installation.objects.all()
    serializer_class = InstallationDetailSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def update(self, request, pk=None):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            document_instance = Installation.objects.get(id=pk)
            serializer = self.serializer_class(instance=document_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (document_instance.ins_completed_date):
                    document_instance.installation_status = 'Completed'
                else:
                    document_instance.installation_status = 'Pending'
                document_instance.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

class InstallDocumentUpdateView(ModelViewSet):
    """
    Get and Update Documents for Authenticated User.
    """
    queryset = InstallationDocument.objects.all()
    serializer_class = InstallationDocumentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def update(self, request, pk=None):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            document_instance = InstallationDocument.objects.get(id=pk)
            serializer = self.serializer_class(instance=document_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (document_instance.contract_docs):
                    document_instance.contract_status = 'Received'
                else:
                    document_instance.contract_status = 'Pending'
                if (document_instance.grid_approval_docs):
                    document_instance.grid_approval_status = 'Received'
                else:
                    document_instance.grid_approval_status = 'Pending'
                if (document_instance.compliance_docs):
                    document_instance.compliance_status = 'Received'
                else:
                    document_instance.compliance_status = 'Pending'
                if (document_instance.pv_site_info_docs):
                    document_instance.pv_site_info_status = 'Received'
                else:
                    document_instance.pv_site_info_status = 'Pending'
                if (document_instance.energy_yield_report_docs):
                    document_instance.energy_yield_report_status = 'Received'
                else:
                    document_instance.energy_yield_report_status = 'Pending'

                if (document_instance.safety_certificate_docs):
                    document_instance.safety_certificate_status = 'Received'
                else:
                    document_instance.safety_certificate_status = 'Pending'
                if (document_instance.noc_docs):
                    document_instance.noc_status = 'Received'
                else:
                    document_instance.noc_status = 'Pending'
                document_instance.save()
                payslip = []
                invoice = Invoice.objects.get(order=document_instance.order)
                if (document_instance.contract_docs):
                    payslip.append(document_instance.contract_docs.url)
                if (document_instance.grid_approval_docs):
                    payslip.append(document_instance.grid_approval_docs.url)
                if (document_instance.compliance_docs):
                    payslip.append(document_instance.compliance_docs.url)
                if (document_instance.pv_site_info_docs):
                    payslip.append(document_instance.pv_site_info_docs.url)
                
                if (document_instance.energy_yield_report_docs):
                    payslip.append(document_instance.energy_yield_report_docs.url)
                if (document_instance.safety_certificate_docs):
                    payslip.append(document_instance.safety_certificate_docs.url)
                if (document_instance.noc_docs):
                    payslip.append(document_instance.noc_docs.url)
                if (invoice.invoice):
                    payslip.append(invoice.invoice.url)
                subject = str(invoice.name)
                message = "Dear" + str(invoice.name) + ", " + "\nI hope you are doing well. " + "\npayslip_"
                mail_response = Mailer(email_id=invoice.email, filename=payslip, subject=subject, otp=message, type="otp")
                _mail= mail_response()
                print(_mail)
                return Response(serializer.data, status=status.HTTP_200_OK)

class InstallDocumentView(APIView):
    """
    Get Installation Documents for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        invoice_instance=InstallationDocument.objects.get(order=order)
        context = {}
        context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
        return Response(context, status=status.HTTP_200_OK)

class WarrantyView(APIView):
    """
    Get Installation and warranty document for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        context = {}
        # order = Order.objects.get(user=request.user)
        order = Order.objects.get(project=self.request.user.username)
        invoice_instance=InstallationDocument.objects.get(order=order)
        context["install_docs"] = InstallationDocumentSerializer(invoice_instance).data
        invoice_instance=WarrantyDocument.objects.get(order=order)
        context["warranty"] = WarrantyDocumentSerializer(invoice_instance).data
        
        return Response(context, status=status.HTTP_200_OK)

class WarrantyUpdateView(ModelViewSet):
    """
    Get and Update Documents for Authenticated User.
    """
    queryset = WarrantyDocument.objects.all()
    serializer_class = WarrantyDocumentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def update(self, request, pk=None):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            document_instance = WarrantyDocument.objects.get(id=pk)
            serializer = self.serializer_class(instance=document_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (document_instance.panels_docs):
                    document_instance.war_status = 'Completed'
                if (document_instance.inverter_docs):
                    document_instance.war_status = 'Completed'
                elif (document_instance.battery_docs):
                    document_instance.war_status = 'Completed'
                else:
                    document_instance.war_status = 'Pending'
                document_instance.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

class ReferralList(APIView):
    """
    List all userreferral, or create a new user_referral.
    """
    queryset = UserReferral.objects.all()
    serializer_class = UserReferralSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    # def get(self, request, format=None):
    #     snippets = UserReferral.objects.all()
    #     serializer = UserReferralSerializer(snippets, many=True)
    #     return Response(serializer.data)
    # def get(self, request, format=None):
    #     snippets = ReferralSuccess.objects.all()
    #     serializer = UserReferralSuccessSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def get(self,request):
        admin = Address.objects.get(user=self.request.user)
        reffered_by = Order.objects.get(admin=admin)
        queryset2=UserReferral.objects.filter(referred_by=reffered_by)
        referral=ReferralSuccess.objects.get(referral_by=reffered_by)
        for i in queryset2:
            referral.referral.add(i)
            referral.save()
        serializer=UserReferralSuccessSerializer(referral).data
        return Response(serializer, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data=self.request.data
        admin = Address.objects.get(user=self.request.user)
        reffered_by = Order.objects.get(admin=admin)
        data["referred_by"] = reffered_by
        print("data"*100, data)
        serializer = UserReferralSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            no_of_ref=UserReferral.objects.filter(referred_by=reffered_by)
            try:
                ref_user = ReferralSuccess.objects.get(referral_by=reffered_by) 
                if ref_user:
                    ref_user.referrals_made = no_of_ref.count()
                    ref_user.referral_by = reffered_by
                    ref_user.referral.add(serializer.data['id'])
                    ref_user.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                ReferralSuccess.objects.create(referral_by=reffered_by, referrals_made=no_of_ref.count())
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)