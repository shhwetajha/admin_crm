from rest_framework import status
from .serializer import (
    InvoiceSerailizer, InvoiceHistorySerializer
)
from .models import Invoice, InvoiceHistory
from rest_framework.views import APIView
from grid_approval.models import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, action, permission_classes

class InvoiceView(APIView):
    """
    Get Invoice for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)
    

    def get(self, request, format=None):
        invoice_instance=Invoice.objects.get(invoice_number=request.user.username)
        # print
        context = {}
        context["invoice"] = InvoiceSerailizer(invoice_instance).data
        return Response(context, status=status.HTTP_200_OK)

class OrderInvoiceView(ModelViewSet):
    """
    Get Invoice for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        # data = request.data
        _profile=User.objects.get(id=request.user.id)
        if ((_profile.user_type != "ADMIN") and (not self.request.user.is_superuser)):
            return Response(
                {"error": True, "errors": "Permission Denied"}, 
                status=status.HTTP_403_FORBIDDEN,
        )
        else:
            # project = self.request.data.get('project')
            project = request.query_params.get("project", None)
            order = Order.objects.get(project=project)
            print("order"*10, order)
            invoice_instance=Invoice.objects.get(order=order)
            print("invoice_instance"*100, invoice_instance)
            context = {}
            context["invoice"] = InvoiceSerailizer(invoice_instance, many=True).data
            return Response(context, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_invoice(request, id):
    # particular single order invoice
    _profile=User.objects.get(id=request.user.id)
    if ((_profile.user_type != "ADMIN") and (not request.user.is_superuser)):
        return Response({"error": True, "errors": "Permission Denied"},status=status.HTTP_403_FORBIDDEN, )
    else:
        order = Order.objects.get(id=id)
        invoice_instance=Invoice.objects.get(order=order)
        context = {}
        context["invoice"] = InvoiceSerailizer(invoice_instance).data
        return Response(context, status=status.HTTP_200_OK)

class InvoiceHistoryView(APIView):
    """
    Get All Invoice Transaction History for Authenticated User.
    """
    permission_classes = (IsAuthenticated,)
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get(self, request, format=None):
        invoice_instance=InvoiceHistory.objects.filter(invoice_number=request.user.username)
        context = {}
        
        context["invoice"] = InvoiceHistorySerializer(invoice_instance, many=True).data
        return Response(context, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_invoice_hist(request, id):

    # paricular invoice history
    _profile=User.objects.get(id=request.user.id)
    if ((_profile.user_type != "ADMIN") and (not request.user.is_superuser)):
        return Response({"error": True, "errors": "Permission Denied"},status=status.HTTP_403_FORBIDDEN, )
    else:
        order = Order.objects.get(id=id)
        invoice_instance=Invoice.objects.get(order=order)
        invoice_instance=InvoiceHistory.objects.filter(invoice=invoice_instance)
        context = {}
        context["invoice"] = InvoiceHistorySerializer(invoice_instance, many=True).data
        return Response(context, status=status.HTTP_200_OK)

# def home(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         amount = 50000

#         client = razorpay.Client(
#             auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

#         payment = client.order.create({'amount': amount, 'currency': 'INR',
#                                        'payment_capture': '1'})
#     return render(request, 'index.html')
