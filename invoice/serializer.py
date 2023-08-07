from rest_framework import serializers
from invoice.models import Invoice, InvoiceHistory

class InvoiceSerailizer(serializers.ModelSerializer):
    # from_address = BillingAddressSerializer()
    # to_address = BillingAddressSerializer()
    # invoice_number = serializers.SerializerMethodField()

    # order = serializers.SerializerMethodField()

    # def get_invoice_number(self, instance):
    #     if instance.invoice_number:
    #         return str(instance.invoice_number.username)
    #     else:
    #         return "null"
    # def get_order(self, instance):
    #     if instance.order:
    #         return str(instance.order)
    #     else:
    #         return "null"
    class Meta:
        model = Invoice
        fields = '__all__'
        # ["id", "invoice_title","name","email", 'rate', 'quantity']
        # ['invoice_number', 'from_address','order', 'to_address',]
        # fields = (
        #     "id",
        #     "order",
        #     "invoice_title",
        #     "invoice_number",
        #     "due_date",
        #     "name",
        #     "email",
        #     "phone",
        #     "to_address",
        #     "from_address",
        #     "currency",
        #     "quantity",
        #     "website",
        #     "rate",
        #     "tax",
        #     "total_amount",
        #     "amount_due",
        #     "amount_paid",
        # )


class InvoiceHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = InvoiceHistory
        # fields = '__all__'
        fields = (
            "id",
            "invoice_title",
            "name",
            "email",
            "quantity",
            "rate",
            "total_amount",
            "payment_method",
            "currency",
            "phone",
            "created_on",
            "amount_due",
            "amount_paid",
            "is_email_sent",
            "status",
            "receipt",
            "details",
            "due_date",
            "payment_date",
            "invoice",
            "invoice_number",
            "to_address",
            "from_address",
        )
        # fields = (
        #     "id",
        #     "invoice_number",
        #     "status",
        #     "due_date",
        #     "name",
        #     "email",
        #     "phone",
        #     "created_on",
        #     "currency",
        #     "quantity",
        #     "rate",
        #     "total_amount",
        #     "amount_due",
        #     "amount_paid",
        #     "payment_method",
        #     "payment_date",
        # )


# class InvoiceCreateSerializer(serializers.ModelSerializer):
#     def __init__(self, *args, **kwargs):
#         invoice_view = kwargs.pop("invoice", False)
#         request_obj = kwargs.pop("request_obj", None)
#         super(InvoiceCreateSerializer, self).__init__(*args, **kwargs)

#         self.org = request_obj.org

#     def validate_invoice_title(self, invoice_title):
#         if self.instance:
#             if (
#                 Invoice.objects.filter(
#                     invoice_title__iexact=invoice_title, org=self.org
#                 )
#                 .exclude(id=self.instance.id)
#                 .exists()
#             ):
#                 raise serializers.ValidationError(
#                     "Invoice already exists with this invoice_title"
#                 )
#         else:
#             if Invoice.objects.filter(
#                 invoice_title__iexact=invoice_title, org=self.org
#             ).exists():
#                 raise serializers.ValidationError(
#                     "Invoice already exists with this invoice_title"
#                 )
#         return invoice_title

#     class Meta:
#         model = Invoice
#         fields = (
#             "id",
#             "invoice_title",
#             "status",
#             "name",
#             "email",
#             "phone",
#             "due_date",
#             "created_on",
#             "created_by",
#             "currency",
#             "quantity",
#             "rate",
#             "tax",
#             "total_amount",
#             "amount_due",
#             "amount_paid",
#             "is_email_sent",
#             "details",
#             "org",
#         )
