from rest_framework.serializers import ModelSerializer
from .models import CallSupport, FeedBack

class CallSupportSerializer(ModelSerializer):
	
	class Meta:
		model = CallSupport
		fields = "__all__"

class FeedBackSerializer(ModelSerializer):
	
	class Meta:
		model = FeedBack
		fields = "__all__"
		# fields = ["id", "panels_brands",  "panels_docs", "inverter_brands", "inverter_docs", "battery_brands", "battery_docs"]