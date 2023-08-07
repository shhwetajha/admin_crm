from django.urls import path
from invoice import  views
urlpatterns = [
    # path("get_presite/", presite_detail, name='order_detail'),
    path("invoice/", views.InvoiceView.as_view()),
    path("invoice_hist/", views.InvoiceHistoryView.as_view()),
    path("order_invoice/<int:id>/", views.order_invoice),
    path("order_invoice_hist/<int:id>/", views.order_invoice_hist),
]
