from rest_framework import status, filters
from module.serializer import ModuleSerializer
from module.models import Module
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from rest_framework.viewsets import ModelViewSet

class ModuleView(ModelViewSet):
	"""
    List all project action, or create a new pproject action.
    """
	permission_classes = (IsAuthenticated,)
	# model = Module
	queryset = Module.objects.all()
	serializer_class = ModuleSerializer
	http_method_names = ['post', 'patch', 'get', 'delete',]
	filter_backends = [filters.OrderingFilter]
	ordering_fields = ['created_at']
	ordering = ['created_at']
		
	def create(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def update(self, request, pk=None, *args, **kwargs): 
		user = request.user
		instance = self.get_object()
		data = self.request.data
		serializer = self.serializer_class(instance=instance,
                                            data=data, # or request.data
                                            context={'author': user},
                                            partial=True)
		if serializer.is_valid(raise_exception=True):
			serializer.save()
			return Response(data=serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	# def retrieve(self, request, pk=None):
	# 	instance = self.get_object()
	# 	return Response(self.serializer_class(instance).data,
    #                     status=status.HTTP_200_OK)
	
	def list(self, request):
		# query_set = Module.objects.filter(my_list=True)
		return Response(self.serializer_class(self.queryset, many=True).data,
                        status=status.HTTP_200_OK)

	def destroy(self, request, pk=None, *args, **kwargs):
		instance = self.get_object()
		return super(ModuleView, self).destroy(request, pk, *args, **kwargs)