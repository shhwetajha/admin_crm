from rest_framework import status, filters
from other_component.serializer import OtherComponentSerializer
from other_component.models import OtherComponent
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

class OtherComponentView(ModelViewSet):
	"""
    List all project action, or create a new pproject action.
    """
	permission_classes = (IsAuthenticated,)
	serializer_class = OtherComponentSerializer
	queryset = OtherComponent.objects.all()
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
		query_set = OtherComponent.objects.filter(my_list=True)
		return Response(self.serializer_class(query_set, many=True).data,
                        status=status.HTTP_200_OK)

	def destroy(self, request, pk=None, *args, **kwargs):
		instance = self.get_object()
		return super(OtherComponentView, self).destroy(request, pk, *args, **kwargs)
		
# class OtherComponentView(APIView):
# 	"""
#     List all project action, or create a new pproject action.
#     """
# 	permission_classes = (IsAuthenticated,)
# 	model = OtherComponent
# 	serializer_class = OtherComponentSerializer
	
# 	def get(self, request, format=None):
# 		snippets = OtherComponent.objects.all()
# 		serializer = self.serializer_class(snippets, many=True)
# 		return Response(serializer.data)
		
# 	def post(self, request, format=None):
# 		serializer = self.serializer_class(data=request.data)
# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class OtherComponentDetail(APIView):
# 	"""
#     Retrieve, update or delete a project action instance.
#     """
# 	permission_classes = (IsAuthenticated,)
# 	model = OtherComponent
# 	serializer_class = OtherComponentSerializer

# 	def get_object(self, pk):
# 		try:
# 			return OtherComponent.objects.get(pk=pk)
# 		except OtherComponent.DoesNotExist:
# 			raise Http404
			
# 	def get(self, request, pk, format=None):
# 		snippet = self.get_object(pk)
# 		serializer = self.serializer_class(snippet)
# 		return Response(serializer.data)
	
# 	def put(self, request, pk, format=None):
# 		snippet = self.get_object(pk)
# 		serializer = self.serializer_class(snippet, data=request.data)

# 		if serializer.is_valid():
# 			serializer.save()
# 			return Response(serializer.data)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		
# 	def delete(self, request, pk, format=None):
# 		snippet = self.get_object(pk)
# 		snippet.delete()
# 		return Response(status=status.HTTP_204_NO_CONTENT)