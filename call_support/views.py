from django.shortcuts import render
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from .serializer import CallSupportSerializer, FeedBackSerializer
from .models import FeedBack, CallSupport

class CallSupportView(ModelViewSet):
    """
    Customers call support api.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = CallSupportSerializer
    queryset = CallSupport.objects.all()
    http_method_names = ['post', 'patch', 'get', 'delete',]
    
    def create(self, request, *args, **kwargs):
        data=self.request.data
        data["requested_by"] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def list(self, request):
    #     query_set = CallSupport.objects.filter(my_list=True)
    #     return Response(self.serializer_class(query_set, many=True).data,
    #                     status=status.HTTP_200_OK)

class FeedBackView(ModelViewSet):
    """
    Customers feedback api.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()
    http_method_names = ['post', 'patch', 'get', 'delete',]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['created_at']
    
    def create(self, request, *args, **kwargs):
        data=self.request.data
        data["feedback_by"] = self.request.user.id
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # def list(self, request):
    #     query_set = FeedBack.objects.filter(my_list=True)
    #     return Response(self.serializer_class(query_set, many=True).data,
    #                     status=status.HTTP_200_OK)

# class CallSupport(APIView):

#     permission_classes = (IsAuthenticated,)
    
#     """
#     Create User Call Support.
#     """

#     def post(self, request, format=None):
#         data=self.request.data
#         data["requested_by"] = request.user.id
#         serializer = CallSupportSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                         {"message":"Success", "status": True}, 
#                          status=status.HTTP_201_CREATED
#                         )
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FeedBackView(APIView):

#     permission_classes = (IsAuthenticated,)
#     """
#     Create User Feedback.
#     """
    
#     def get(Self,request):
#         queryset2=FeedBack.objects.filter(feedback_by=request.user.id)
#         data = []
#         for i in queryset2:
#             serializer = FeedBackSerializer(i).data
#             data.append(serializer)
#         return Response(data, status=status.HTTP_200_OK)

#     def post(self, request, format=None):
#         data=self.request.data
#         data["feedback_by"] = request.user.id
#         serializer = FeedBackSerializer(data=data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                         {"message":"Success", "status":True}, 
#                          status=status.HTTP_201_CREATED
#                         )
#             # return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AllFeedBackView(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = FeedBack.objects.all()
#         serializer = FeedBackSerializer(snippets, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)