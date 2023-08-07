# Create your views here.
from rest_framework import status, filters
from grid_approval.serializer import (
    
    DocumentSerializer, 
    GridApprovalSerializer, PreSiteRiskSerializer
)
from grid_approval.models import Document, GridApproval, PreSiteRisk
from order.models import Order
from installation.models import Installation, WarrantyDocument
from rest_framework.views import APIView
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.viewsets import ModelViewSet
from common.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from order.views import getFirstError

class DocumentViewSet(ModelViewSet):
    """
    Get and Update Documents for Authenticated User.
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']

    # def get_queryset(self):
    #     order = Order.objects.get(project=self.request.user.username)
        
    #     return Document.objects.filter(order=order)

    def update(self, request, pk=None):
        _profile=User.objects.get(id=self.request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM") and (_profile.user_type != "CUSTOMER"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            document_instance = Document.objects.get(id=pk)
            serializer = self.serializer_class(instance=document_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                document_instance.doc_status = 'Completed'
                document_instance.save()
                if (document_instance.contract_file):
                    document_instance.contract_status = 'Completed'
                else:
                    document_instance.contract_status = 'Pending'
                if (document_instance.meter_box):
                    print(document_instance.meter_box)
                    document_instance.meter_status = 'Completed'
                else:
                    document_instance.meter_status = 'Pending'
                if (document_instance.electricity_bill):
                    document_instance.electricity_status = 'Completed'
                else:
                    document_instance.electricity_status = 'Pending'
                if (document_instance.council_rate):
                    document_instance.council_status = 'Completed'
                else:
                    document_instance.council_status = 'Pending'
                if (document_instance.miscellaneous_file):
                    document_instance.miscellaneous_status = 'Completed'
                else:
                    document_instance.miscellaneous_status = 'Pending'
                document_instance.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

class GridApprovalView(ModelViewSet):
    """
    Get and Update Documents for Authenticated User.
    """
    queryset = GridApproval.objects.all()
    serializer_class = GridApprovalSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put', 'get']
    
    def update(self, request, pk=None):

        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)) and (_profile.user_type != "TEAM"):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            data = self.request.data
            document_instance = GridApproval.objects.get(id=pk)
            serializer = self.serializer_class(instance=document_instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                if (document_instance.meter_Approved_date):
                    document_instance.grid_status = 'Completed'
                else:
                    document_instance.grid_status = 'Pending'
                document_instance.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

# only for customer user
class GridView(APIView):
    """
    Get Grid Approval for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        order_instance=GridApproval.objects.get(order=order)
        if order.nmi_no:
            order_instance.nmi_no = order.nmi_no
            order_instance.save()
        if order_instance.meter_Approved_date:
            order_instance.grid_status = 'Completed'
            order_instance.save()
        context = {}    
        context["grid_approval"] = GridApprovalSerializer(order_instance).data
        return Response(context, status=status.HTTP_200_OK)

# only for customer user
class DocumentView(APIView):
    """
    Get Grid Approval for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        docs = Document.objects.get(order=order)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        contract = []
        meter = []
        electricity = []
        council = []
        miscellaneous = []
        if (docs.contract_file):
            contract.append({
                        'id': docs.id,
                        'contract_file': docs.contract_file.url,
                        'contract_status': docs.contract_status,
                        'doc_status':docs.doc_status                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
                    })
        else:
            contract = []
        if (docs.meter_box):
            meter.append({
                        # 'id': docs.id,
                        'meter_box': docs.meter_box.url,
                        'meter_status': docs.meter_status,
                        # 'doc_status':docs.doc_status
                    })
        else:
            meter.append({
                        # 'id': docs.id,
                        'meter_box': "",
                        'meter_status': docs.meter_status,
                        # 'doc_status':docs.doc_status
                    })
        if (docs.electricity_bill):
            electricity.append({
                        # 'id': docs.id,
                        'electricity_bill': docs.electricity_bill.url,
                        'electricity_status': docs.electricity_status,
                        # 'doc_status':docs.doc_status
                    })
        else:
            electricity.append({
                        # 'id': docs.id,
                        'electricity_bill': "",
                        'electricity_status': docs.electricity_status,
                        # 'doc_status':docs.doc_status
                    })
        if (docs.council_rate):
            council.append({
                        # 'id': docs.id,
                        'council_rate': docs.council_rate.url,
                        'council_status': docs.council_status,
                        # 'doc_status':docs.doc_status
                    })
        else:
            council.append({
                        # 'id': docs.id,
                        'council_rate': "",
                        'council_status': docs.council_status,
                        # 'doc_status':docs.doc_status
                    })
        if (docs.miscellaneous_file):
            miscellaneous.append({
                            # 'id': docs.id,
                            'miscellaneous_file': docs.miscellaneous_file.url,
                            'miscellaneous_status': docs.miscellaneous_status,
                            # 'doc_status':docs.doc_status
                        })
        else:
            miscellaneous.append({
                            # 'id': docs.id,
                            'miscellaneous_file': "",
                            'miscellaneous_status': docs.miscellaneous_status,
                            # 'doc_status':docs.doc_status
                        })
        # return JsonResponse({"status": True, "message": "success","contract":contract, "meter": meter, "electricity":electricity, "council":council, "misxcellaneous":misxcellaneous}, status=status.HTTP_200_OK)
        context = {}    
        context["contract"] = contract
        context["meter"] = meter
        context["electricity"] = electricity
        context["council"] = council
        context["miscellaneous"] = miscellaneous
        return Response(context, status=status.HTTP_200_OK)

# only for customer user
class HomeStatusView(APIView):
    """
    Get Grid Approval for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        order = Order.objects.get(project=self.request.user.username)
        docs = Document.objects.get(order=order)
        grid_status = GridApproval.objects.get(order=order)
        installation_status = Installation.objects.get(order=order)
        docs_warr_status = WarrantyDocument.objects.get(order=order)
        presite = PreSiteRisk.objects.get(order=order)
        home_status = []
        home_status.append({
                    'id': order.id,
                    'order_status':order.order_status,
                    'grid_status': grid_status.grid_status,
                    'doc_status':docs.doc_status,
                    "installation_status": installation_status.ins_status,
                    'war_status': docs_warr_status.war_status,
                    'presite_status': presite.presite_status,
                })
        return Response(home_status, status=status.HTTP_200_OK)


class PresiteRiskViewSet(ModelViewSet):
    """
    Get and Update Presite risk Assesement for Authenticated User.
    """
    queryset = PreSiteRisk.objects.all()
    serializer_class = PreSiteRiskSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get','put', 'patch']
    
    def get_queryset(self):
        order = Order.objects.get(project=self.request.user.username)
        return PreSiteRisk.objects.filter(order=order)
    
    def update(self, request, pk=None):

        data = self.request.data

        order_instance = PreSiteRisk.objects.get(id=pk)
        serializer = self.serializer_class(instance=order_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)