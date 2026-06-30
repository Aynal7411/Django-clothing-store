
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = [
            "mobile",
            "name",
            "password",
        ]

    def validate_mobile(self, value):
        if User.objects.filter(mobile=value).exists():
            raise serializers.ValidationError(
                "This mobile number is already registered."
            )
        return value
    def validate_name(self, value):

        if len(value.strip()) < 3:
            raise serializers.ValidationError(
                "Name must contain at least 3 characters."
            )

        return value
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class MyTokenObtainPairSerializer(
    TokenObtainPairSerializer
):

    username_field = "mobile"

    @classmethod
    def get_token(cls, user):

        token = super().get_token(user)

        token["name"] = user.name
        token["mobile"] = user.mobile

        return token

    def validate(self, attrs):

        data = super().validate(attrs)

        data["user"] = {

            "id": self.user.id,

            "name": self.user.name,

            "mobile": self.user.mobile,
        }

        return data
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User

        fields = (
            "id",
            "mobile",
            "name",
        )  