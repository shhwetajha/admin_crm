from rest_framework.serializers import ModelSerializer, SerializerMethodField
from order.models import Order, InstallerAvailibility, TakeAppointment, DateString, DocumentUpload, DocumentOrderUpload,InstallerHoliday
from common.serializer import AddressSerializer, UserProfileSerializer
from other_component.serializer import OtherComponentSerializer, ViewOtherComponentSerializer
from module.serializer import ViewModuleSerializer

from inverters.serializer import ViewInverterModuleSerializer
from common.serializer import InstallerProfileSerializer, InstallerAvailProfileSerializer, UserSerializer
from rest_framework import serializers
from other_component.models import OtherComponent
from batteries.serializer import ViewBatteryModuleSerializer
from order.timeleft import timeleft_function

class DocumentOrderUploadSerializer(ModelSerializer):
	class Meta:
		model = DocumentOrderUpload
		fields = [
			"file"
		]

class OrderDetailSerializer(ModelSerializer):
	other_component = ViewOtherComponentSerializer(many=True, read_only=True)
	panels = ViewModuleSerializer()
	inverter = ViewInverterModuleSerializer()
	batteries = ViewBatteryModuleSerializer()
	to_address = AddressSerializer()
	packing_slip = DocumentOrderUploadSerializer(many=True, read_only=True)
	western_power = DocumentOrderUploadSerializer(many=True, read_only=True)
	switch_board = DocumentOrderUploadSerializer(many=True, read_only=True)
	panel_layout = DocumentOrderUploadSerializer(many=True, read_only=True)
	extras = DocumentOrderUploadSerializer(many=True, read_only=True)
	assign_to = UserProfileSerializer(many=True, read_only=True)
	class Meta:
		model = Order
		# fields = "__all__"
		fields = [
			"id",
			"order_start_date",
			"order_end_date",
			"to_address",
			"company_Name",
			"project",
			"system_Size",
			"building_Type",
			"nmi_no",
			"panels_quantity",
			"panels",
			"batteries",
			"inverter_quantity",
			"inverter",
			"monitoring_quantity",
			"monitoring",
			"meter_Phase",
			"meter_Number", 
			"order_status",
			"assign_to",
			"installation_Type",
			"other_component",
			"packing_slip",
			"western_power",
			"switch_board",
			"panel_layout",
			"extras",
			"packing_slip_reason",
			"western_power_reason",
			"switch_board_reason",
			"panel_layout_reason",
			"description",
			"created_at",
			"updated_at",
    
		]
		# fields = [
		# 	"id",
		# 	"project",
		# 	"to_address",
		# 	"customer_name",
		# 	"quotation",
		# 	"system_Size",
		# 	"building_Type",
		# 	"nmi_no",
		# 	"panels_quantity",
		# 	"panels",
		# 	"batteries",
		# 	"inverter",
		# 	"meter_Phase", 
		# 	"order_status",
		# 	"installation_Type",
		# 	"other_component",
		# 	"order_time",
		# 	"description",
    
		# ]
# class OrderDetailSerializer(ModelSerializer):
# 	other_component = ViewOtherComponentSerializer(many=True)
# 	panels = ViewModuleSerializer()
# 	inverter = ViewInverterModuleSerializer()
# 	def get_or_create_packages(self, packages):
# 		other_components = []
# 		for other_component in other_components:
# 			other_component_instance, created = OtherComponent.objects.get_or_create(pk=other_component.get('id'), defaults=other_component)
# 			other_components.append(other_component_instance.pk)
# 		return other_components
		
# 	def create_or_update_packages(self, packages):
# 		other_components = []
# 		for other_component in other_components:
# 			package_instance, created = OtherComponent.objects.get_or_create(pk=other_component.get('id'), defaults=other_component)
# 			other_components.append(package_instance.pk)
# 		return other_components
		
# 	def update(self, instance, validated_data):
# 		other_component = validated_data.pop('other_component', [])
# 		instance.other_component.set(self.create_or_update_packages(other_component))
# 		# fields = ['other_component']
# 		# for field in fields:
# 		# 	try:
# 		# 		setattr(instance, field, validated_data[field])
# 		# 	except KeyError:  # validated_data may not contain all fields during HTTP PATCH
# 		# 		pass
# 		instance.save()
# 		return instance

# 	class Meta:
# 		model = Order
# 		# fields = "__all__"
# 		fields = [
# 			"id",
# 			"project",
# 			"customer_name",
# 			"quotation",
# 			"system_Size",
# 			"building_Type",
# 			"nmi_no",
# 			"panels_quantity",
# 			"panels",
# 			"inverter",
# 			"meter_Phase", 
# 			"order_status",
# 			"installation_Type",
# 			"other_component",
# 			"document_file",
# 			"order_time",
# 			"description",
    
# 		]


    

# https://docs.djangoproject.com/en/4.2/topics/http/file-uploads/

class TeamOrderSerializer(ModelSerializer):
	assign_to = UserSerializer(many=True, read_only=True)

	class Meta:
		model = Order
		# fields = "__all__"
		fields = [
			"id",
			"company_Name",
			"project",
			"order_status",
			"assign_to",
    
		]

class OrderSerializer(ModelSerializer):
	other_component = OtherComponentSerializer(many=True, read_only=True)
	packing_slip = DocumentOrderUploadSerializer(many=True, read_only=True)
	western_power = DocumentOrderUploadSerializer(many=True, read_only=True)
	switch_board = DocumentOrderUploadSerializer(many=True, read_only=True)
	panel_layout = DocumentOrderUploadSerializer(many=True, read_only=True)
	extras = DocumentOrderUploadSerializer(many=True, read_only=True)
	# assign_to = UserSerializer(many=True, read_only=True)

	class Meta:
		model = Order
		# fields = "__all__"
		fields = [
			"id",
			"company_Name",
			"customer_name",
			"project",
			"system_Size",
			"building_Type",
			"nmi_no",
			"panels_quantity",
			"panels",
			"batteries",
			"inverter_quantity",
			"inverter",
			"monitoring_quantity",
			"monitoring",
			"meter_Phase",
			"meter_Number", 
			"order_status",
			# "assign_to",
			"installation_Type",
			"other_component",
			"packing_slip",
			"western_power",
			"switch_board",
			"panel_layout",
			"extras",
			"packing_slip_reason",
			"western_power_reason",
			"switch_board_reason",
			"panel_layout_reason",
			"description",
			"order_start_date",
			"order_end_date",
    
		]
		# fields = [
		# 	"id",
		# 	"project",
		# 	"customer_name",
		# 	"quotation",
		# 	"order_id",
		# 	"system_Size",
		# 	"building_Type",
		# 	"nmi_no",
		# 	"panels",
		# 	"inverter",
		# 	"roof_Type",
		# 	"roof_Angle",
		# 	"meter_Phase", 
		# 	"order_status",
		# 	"installation_Type",
		# 	"document_file",
		# 	"order_time",
		# 	"description",
    
		# ]

class DateStringSerializer(ModelSerializer):

    class Meta:
        model = DateString
        fields = [
            "id",
            "date",
        ]

# class DateStringSerializer(serializers.Serializer):
#     date = serializers.DateField()
#     # Add any other fields as needed
class InstallerAvailableSerializer(ModelSerializer):
	# installer = InstallerProfileSerializer()
	available_days = DateStringSerializer(read_only=True, many=True)
	class Meta:
		model = InstallerAvailibility
		# fiels = "__all__"
		fields = [
			"id",
			"installer",
			"available_days",
            "available_start_time",
            "available_end_time",
			"reason",
			"is_anvailable",
			"cancelled",
            "created_at",
            "created_by",
        ]


class InstallerHolidaySerializer(ModelSerializer):
	# installer = InstallerProfileSerializer()
	holiday_days = DateStringSerializer(read_only=True, many=True)
	class Meta:
		model = InstallerHoliday
		# fiels = "__all__"
		fields = [
			"id",
			"installer",
			"holiday_days",
			"reason",
			# "is_unavailable",
			"cancelled",
            "created_at",
            "created_by",
        ]

class GetInstallerAvailableSerializer(ModelSerializer):
	installer = InstallerAvailProfileSerializer()
	available_days = DateStringSerializer(many=True, read_only=True)
	class Meta:
		model = InstallerAvailibility
		# fiels = "__all__"
		fields = [
			"id",
			"installer",
            "available_days",
            "available_start_time",
            "available_end_time",
			"reason",
			"is_anvailable",
			"cancelled",
            "created_at",
            "created_by",
        ]


class GetInstallerHolidaySerializer(ModelSerializer):
	installer = InstallerAvailProfileSerializer()
	holiday_days = DateStringSerializer(many=True, read_only=True)
	class Meta:
		model = InstallerHoliday
		# fiels = "__all__"
		fields = [
			"id",
			"installer",
			"reason",
			# "is_unanvailable",
			"holiday_days",
			"cancelled",
            "created_at",
            "created_by",
	    	"is_unavailable",
        ]
	# def validate(self, data):
	# 	available_day = data.get("available_days")
	# 	user = InstallerAvailibility.objects.filter(available_days__iexact=available_day)
	# 	if user:
	# 		raise serializers.ValidationError(
    #             "You have already added your availibility, Please Select another day."
    #         )
	# 	return data

class GetInstallersAvailableSerializer(ModelSerializer):
	
	class Meta:
		model = InstallerAvailibility
		# fiels = "__all__"
		fields = [
        ]
class UpdateInstallerAvailableSerializer(ModelSerializer):
	installer = InstallerProfileSerializer(read_only = True)
	# available_days = serializers.DateField()
	class Meta:
		model = InstallerAvailibility
		# fiels = "__all__"
		fields = (
			"id",
			"installer",
            "available_days",
            "available_start_time",
            "available_end_time",
			"reason",
			"cancelled",
            "created_at",
            "created_by",
		)

		


class ViewTakeAppointmentSerializer(ModelSerializer):
	customer = OrderDetailSerializer(read_only = True)
	class Meta:
		model = TakeAppointment
		# fiels = "__all__"
		fields = [
			"id",
            "customer",
            "appointment_date",
            "appointment_time",
			"appointment_appove",
			"reason",
            "created_at",
            "created_by",
        ]

class TakeAppointmentSerializer(ModelSerializer):
	# customer = OrderSerializer()
	class Meta:
		model = TakeAppointment
		# fiels = "__all__"
		fields = [
			"id",
            "customer",
            "appointment_date",
            "appointment_time",
			"appointment_appove",
			"reason",
            "created_at",
            "created_by",
        ]
		# def validate(self, data):
		# 	available_day = data.get("available_day")
		# 	user = InstallerAvailibility.objects.filter(available_day__iexact=available_day)
		# 	if user:
		# 		raise serializers.ValidationError(
		# 			"You have already added your availibility, Please Select another day."
		# 		)
		# 	return data


class UpdateTakeAppointmentSerializer(ModelSerializer):
	# customer = OrderSerializer()
	class Meta:
		model = TakeAppointment
		# fiels = "__all__"
		fields = [
			"id",
            "appointment_date",
            "appointment_time",
			"appointment_appove",
        ]

class DocumentUploadSerializer(ModelSerializer):
	# customer = OrderSerializer()
	uploaded_at = SerializerMethodField()
	
	def get_uploaded_at(self, instance):
			days = timeleft_function(instance.created_at)
			return days

	class Meta:
		model = DocumentUpload
		fields = [

			"id",
			"order",
			"upload_type",
			"title", "file",
			"taken_from", 
			"created_at",
            "created_by",
			"uploaded_at",
			]

class GetResponceSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_status(self, obj):
        return True

    def get_message(self, obj):
        return "success"
