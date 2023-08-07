from rest_framework import status, filters
from batteries.serializer import BatteryModuleSerializer
from batteries.models import BatteryModule
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

class BatteryModuleView(ModelViewSet):
	"""
    Add, Update, list, and delete Batteries Module.
    """
	permission_classes = (IsAuthenticated,)
	serializer_class = BatteryModuleSerializer
	queryset = BatteryModule.objects.all()
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
		query_set = BatteryModule.objects.filter(my_list=True)
		return Response(self.serializer_class(query_set, many=True).data,
                        status=status.HTTP_200_OK)
	
	def destroy(self, request, pk=None, *args, **kwargs):
		instance = self.get_object()
		return super(BatteryModuleView, self).destroy(request, pk, *args, **kwargs)