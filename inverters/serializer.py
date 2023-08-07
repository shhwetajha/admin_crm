
from rest_framework.serializers import ModelSerializer
from inverters.models import InverterModule

class InverterModuleSerializer(ModelSerializer):

    class Meta:
        model = InverterModule
        fields = '__all__'

class ViewInverterModuleSerializer(ModelSerializer):
    class Meta:
        model = InverterModule
        # fields = "__all__"
        fields = [
			"id",
			"title",
			"code",
			"inverter_logo",
            "inverter_type",
			"manufacturer",
			"rated_output_power",
			"product_warranty",
			"default_inverter_range",
            "additional_part_warranty",
			"my_list"
    
		]