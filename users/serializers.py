from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


def mobile_validator(mobile: str):
    """
        Mobile Number Validator
    """
    if len(mobile) != 11:
        raise serializers.ValidationError(
            "The Mobile Number Must Contain Exact 11 Digits!"
        )
    if not mobile.startswith("09"):
        raise serializers.ValidationError(
            "The Mobile Number Must Be Like 09xxxxxxxxx!"
        )


class UserRegisterSerializer(serializers.ModelSerializer):
    """
        User Register Serializer
    """
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(object):
        """
            Meta
        """
        model = User
        fields = (
            "mobile",
            "first_name",
            "last_name",
            "password",
            "confirm_password"
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "mobile": {"validators": (mobile_validator,)},
        }

    def validate(self, data):
        """
            Data Validations
        """
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords Aren't Matched!")
        return data

    def create(self, validated_data: dict):
        """
            Overriding Create User Method
        """
        return User.objects.create_user(**validated_data)


class UserProfileSerializer(serializers.ModelSerializer):
    """
        User Profile Serializer
    """
    class Meta(object):
        """
            Meta
        """
        model = User
        exclude = ["password"]
