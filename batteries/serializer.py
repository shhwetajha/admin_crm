

from rest_framework.serializers import ModelSerializer
from batteries.models import BatteryModule

class BatteryModuleSerializer(ModelSerializer):
    class Meta:
        model = BatteryModule
        fields = "__all__"

class ViewBatteryModuleSerializer(ModelSerializer):
    class Meta:
        model = BatteryModule
        # fields = "__all__"
        fields = [
			"id",
			"title",
			"code",
			"battery_logo",
            "total_energy",
			"manufacturer",
			"product_warranty",
			"my_list"
    
		]