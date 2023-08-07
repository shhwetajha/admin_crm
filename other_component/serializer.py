

from rest_framework.serializers import ModelSerializer
from other_component.models import OtherComponent

class OtherComponentSerializer(ModelSerializer):
    class Meta:
        model = OtherComponent
        fields = "__all__"


class ViewOtherComponentSerializer(ModelSerializer):
    class Meta:
        model = OtherComponent
        # fields = "__all__"
        fields = [
            "id",
            "title",
            "code",
            "component_logo",
            "manufacturer",
            "smart_meter",
            "optimisor",
            "product_warranty",
            "smart_meter_heading",
            "optimisor_heading",
            "my_list",
        ]