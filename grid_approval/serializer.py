from rest_framework.serializers import ModelSerializer
from grid_approval.models import  Document, GridApproval, PreSiteRisk
from rest_framework import fields
# from common.serializer import ProfileSerializer

class GridApprovalSerializer(ModelSerializer):
	class Meta:
		model = GridApproval
		fields = ["id","nmi_no", "meter_date","meter_Approved_date", "grid_status","energy_provider"]

class DocumentSerializer(ModelSerializer):
    # created_by = ProfileSerializer()

    class Meta:
        model = Document
        # fields = "__all__"

        fields = [
            "id",
            "order",
            "contract_file",
            "contract_status",
            "meter_box",
            "meter_status",
            "electricity_bill",
            "electricity_status",
            "council_rate",
            "council_status",
            "miscellaneous_file",
            "miscellaneous_status",
            "doc_status",
        ]

class DocumentCreateSerializer(ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].required = True

    class Meta:
        model = Document
        fields = ["title", "document_file", "status"]

class PreSiteRiskSerializer(ModelSerializer):

    # roof_structure = fields.MultipleChoiceField(choices=ROOF_STRUCTURE_CHOICE, required=False)
    # select_hazards = fields.MultipleChoiceField(choices=HAZARDS_CHOICE, required=False)
    class Meta:
        model = PreSiteRisk
        fields = '__all__'
        # fields = [
        #     "id",
        #     "approximate_age",
        #     "hazards",
        #     "select_hazards",
        #     "roof_structure",
        #     "moss",
        #     "moss_comment",
        #     "high_tension",
        #     "high_tension_attachment",
        #     "damaged_severley",
        #     "roof_damage",
        #     "any_damage",
        #     "vehicle_activities",
        #     "asbestos_presence",
        #     "safety_concerns",
        #     "safety_concerns_comment",
        # ]
