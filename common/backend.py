# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend

# class EmailBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=username)
#         except UserModel.DoesNotExist:
#             return None
#         else:
#             if user.check_password(password):
#                 return user
#         return None

# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.backends import ModelBackend
# from common.models import User
# class EmailBackend(ModelBackend):
#     """
#     This is a ModelBacked that allows authentication
#     with either a username or an email address.
    
#     """
#     def authenticate(self, username=None, password=None):
#         if '@' in username:
#             kwargs = {'email': username}
#         else:
#             kwargs = {'username': username}
#         try:
#             user = get_user_model().objects.get(**kwargs)
#             if user.check_password(password):
#                 return user
#         except User.DoesNotExist:
#             return None

    # def get_user(self, username):
    #     try:
    #         return get_user_model().objects.get(pk=username)
    #     except get_user_model().DoesNotExist:
    #         return None

from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from django.db.models import Q
from common.models import User

User = get_user_model()

class EmailBackend(object):
    def authenticate(request, username=None, password=None):
        try:
            user = User.objects.get(
               Q(email=username) | Q(username=username)
            )
        except User.DoesNotExist:
            return None
        if user and check_password(password, user.password):
            return user
        return None
    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None