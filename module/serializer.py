

from rest_framework.serializers import ModelSerializer
from module.models import Module

class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

class ViewModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        # fields = "__all__"
        fields = [
			"id",
			"title",
			"code",
			"component_logo",
			"manufacturer",
			"technology",
			"product_warranty",
			"performance_warranty",
			"my_list"
    
		]