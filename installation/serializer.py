from rest_framework.serializers import ModelSerializer, SerializerMethodField
from . models import Installation, InstallationDocument, WarrantyDocument, UserReferral, ReferralSuccess

class InstallationSerializer(ModelSerializer):
	
	class Meta:
		model = Installation
		fields = "__all__"
		# fields = [
		# 	"id", "ins_booking_date","ins_completed_date","important_info", "payment_due","nmi_no","installation_status", "net_meter_status"
		# ]
class InstallationDetailSerializer(ModelSerializer):
	
	class Meta:
		model = Installation
		# fields = "__all__"
		fields = [
			"ins_booking_date","ins_completed_date","important_info", "payment_due","nmi_no","installation_status", "net_meter_status"
		]

class InstallationDocumentSerializer(ModelSerializer):
	
	class Meta:
		model = InstallationDocument
		# fields = "__all__"
		fields = ["id", "contract_docs","contract_status", 
					"grid_approval_docs", "grid_approval_status", "compliance_docs", "compliance_status", 
					"user_manual", "pv_site_info_docs", "pv_site_info_status", "energy_yield_report_docs", 
					"energy_yield_report_status", "safety_certificate_docs", "safety_certificate_status", 
					"noc_docs", "noc_status"]

class WarrantyDocumentSerializer(ModelSerializer):
	
	class Meta:
		model = WarrantyDocument
		# fields = "__all__"
		fields = ["id", "panels_brands",  "panels_docs", "inverter_brands", "inverter_docs", "battery_brands", "battery_docs"]


class UserReferralSerializer(ModelSerializer):
	
	class Meta:
		model = UserReferral
		# fields = "__all__"
		fields = ["id", "referred_by",  "first_name", "last_name", "mobile_no" ,"email", "referral_address_line", "referral_street", 
						"referral_city", "referral_state", "referral_postcode", "referral_country", "referral_date",  "joined_date", ]

class UserReferralSuccessSerializer(ModelSerializer):
	referral = UserReferralSerializer(many=True)
	class Meta:
		model = ReferralSuccess
		# fields = "__all__"
		fields = ["referrals_made", "referral_by",  "referrals_paid", "approval_pending", "referral"]