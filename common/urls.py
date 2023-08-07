from django.urls import path
from common import views
from order.views import slots_list, OrderView

urlpatterns = [
    # path("register/", views.RegistrationView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("logout/", views.Logout.as_view()),
    # path("profile/", views.ProfileView.as_view()),
    # path("register/", views.UsersCreateView.as_view()),
    # path("users/<int:pk>/", views.UserDetailView.as_view()),
    path('forgot-password/', views.ForgotPassword.as_view()),
    path('change-password/', views.ChangePassword.as_view()),
    path("slots_list/", slots_list, name="slots_list"),
    # path("username_list/", views.username_list, name="username_list"),
    # path("username_list_non_admin/", views.username_list_non_admin, name="username_list_non_admin"),
    # path("get_uploaded_Docs/", get_uploaded_Docs, name="get_uploaded_Docs"),
    path("get_order/", OrderView.as_view()),
    # path("cust-request/", views.CallSupport.as_view()),
    # path("cust-review/", views.FeedBackView.as_view()),
    # path("all-cust-review/", views.AllFeedBackView.as_view()),
]
