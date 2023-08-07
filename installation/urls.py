from django.urls import path
from installation import  views
urlpatterns = [
    
    path("install/", views.InstallView.as_view()),
    path("installdocs/", views.InstallDocumentView.as_view()),
    path("warranty/", views.WarrantyView.as_view()),
    path("referral/", views.ReferralList.as_view()),
]
