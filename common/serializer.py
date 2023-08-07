from rest_framework import serializers
from common.models import (
    User,
    Team,
    NonAdminUser,
    InstallerUser,
    Address,
    CustomerUser
)

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = '__all__'

class NonAdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NonAdminUser
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "user_type",
            "phone",
            "profile_pic",
            "has_approve"
        )

    # class UserProfileSerializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = User
    #         fields = ("id", "user_type", "username", "first_name", "last_name", "phone", "profile_pic", "email",)

class BillingAddressSerializer(serializers.ModelSerializer):
    # user = UserProfileSerializer()
    
    # def get_user(self, instance):
    #     print(instance)
    #     return UserProfileSerializer(instance.user_type.all(), many=True).data

    class Meta:
        model = Address
        fields = ("address_line", "street", "city", "state", "postcode", "country")

    def __init__(self, *args, **kwargs):
        account_view = kwargs.pop("account", False)

        super().__init__(*args, **kwargs)

        if account_view:
            # self.fields["user"].required = False
            self.fields["address_line"].required = False
            self.fields["street"].required = True
            self.fields["city"].required = True
            self.fields["state"].required = True
            self.fields["postcode"].required = True
            self.fields["country"].required = True

# class CustomerUserSerializer(serializers.ModelSerializer):
#     assign_to = UserSerializer(many=True, read_only=True)
#     # assign_to = serializers.SerializerMethodField(many=True)

#     class Meta:
#         model = CustomerUser
#         fields = '__all__'

class InstallerUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = InstallerUser
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):

    user = UserProfileSerializer()
    def get_user(self, instance):
        return UserProfileSerializer(instance.user_type.all(), many=True).data
    class Meta:
        model = Address
        # fields = '__all__'
        fields = ("id", "user")

class GetResponceSerializer(serializers.Serializer):
    status = serializers.SerializerMethodField()
    message = serializers.SerializerMethodField()

    def get_status(self, obj):
        return True

    def get_message(self, obj):
        return "success"
        
# class CustomerProfileSerializer(serializers.ModelSerializer):
#     assign_to = UserProfileSerializer(many=True, read_only=True)
#     # assign_to = serializ ers.SerializerMethodField(many=True)
#     admin = AddressSerializer()
#     class Meta:
#         model = CustomerUser
#         # fields = '__all__'
#         fields = ("id", "admin", "alternate_phone", "looking_for", "project_capacity", "utility_bill", "assign_to", "supply", "roof_type", "floor", "remarks", "buying_options", "follows_up_1", "follows_up_2", "quote_sent")
#         # fields = ("id", "admin")

class InstallerProfileSerializer(serializers.ModelSerializer):
    admin = AddressSerializer()

    def get_admin(self, instance):
        return AddressSerializer(instance.user.all(), many=True).data

    class Meta:
        model = InstallerUser
        # fields = '__all__'
        # fields = ("id", "admin")
        fields = ("id", "admin", "alternate_phone", "department", "ec_file", "ec_number", "el_file", "el_number", "abm_number", "acn_number", "tfn_number", "is_online")

class InstallerAvailProfileSerializer(serializers.ModelSerializer):
    # admin_address_line = serializers.CharField(source='admin', read_only=True)
    # admin_user_username = serializers.CharField(source='admin', read_only=True)
    # admin_user_phone = serializers.CharField(source='admin', read_only=True)
    # admin_user_email = serializers.CharField(source='admin', read_only=True)
    # admin_user_email = serializers.CharField(source='admin', read_only=True)
    admin = AddressSerializer()

    def get_admin(self, instance):
        return AddressSerializer(instance.user.all(), many=True).data

    class Meta:
        model = InstallerUser
        # fields = '__all__'
        # fields = ("id", "admin")
        fields = ("id",  "alternate_phone", "admin", "department", "ec_file", "ec_number", "el_file", "el_number", "abm_number", "acn_number", "tfn_number", "is_online")
        
class TeamProfileSerializer(serializers.ModelSerializer):
    # admin = UserProfileSerializer(many=True)
    admin = AddressSerializer()
    class Meta:
        model = Team
        # fields = '__all__'
        fields = ("id", "admin", "alternate_phone", "department", "is_sales_Manager", "is_installation_Manager", "is_marketing_Manager", "is_invoice_Manager", "description",   "is_online")
        # fields = ("id", "admin")

class NonAdminProfileSerializer(serializers.ModelSerializer):
    admin = AddressSerializer()


    # def get_admin(self, instance):
    #     return AddressSerializer(instance.user.all(), many=True).data

# fields = ("id", "admin__address_line", "admin__street", "admin__city", "admin__state", "admin__country", "alternate_phone", "company_name", "has_customer_access", "has_installer_access")
    class Meta:
        model = NonAdminUser
        # fields = '__all__'
        # fields = ("id", "admin")
        fields = ("id", "admin", "alternate_phone", "company_name", "has_customer_access", "has_installer_access")
        # fields = ("id", "admin__user", "admin__address_line", "admin__street", "admin__city", "admin__state", "admin__country", "alternate_phone", "company_name", "has_customer_access", "has_installer_access")




class CustomerUserSerializer(serializers.ModelSerializer):
    # assign_to = UserSerializer(many=True, read_only=True)
    # assign_to = serializers.SerializerMethodField(many=True)

    class Meta:
        model = CustomerUser
        fields = '__all__'

class CustomerProfileSerializer(serializers.ModelSerializer):
    # assign_to = UserProfileSerializer(many=True, read_only=True)
    # assign_to = serializ ers.SerializerMethodField(many=True)
    admin = BillingAddressSerializer()
    class Meta:
        model = CustomerUser
        # fields = '__all__'
        fields = ("id", "admin")

class GetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email__iexact=email).last()
        if not user:
            raise serializers.ValidationError(
                "You don't have an account. Please create one."
            )
        return data