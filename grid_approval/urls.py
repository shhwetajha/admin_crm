from django.urls import path
from grid_approval import  views
urlpatterns = [
    # path("get_presite/", views.presite_detail, name='order_detail'),
    path("grid_approval/", views.GridView.as_view()),
    path("get_docs/", views.DocumentView.as_view()),
    path("home_status/", views.HomeStatusView.as_view()),
]
