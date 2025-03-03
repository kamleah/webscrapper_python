from rest_framework import serializers
import re
import random
import string

""" Import django models here """
from .models import UserRoleModel, CustomUser, RoleModel


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )
        if not re.search(r"\d", value):
            raise serializers.ValidationError(
                "Password must contain at least one digit."
            )
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )
        return value

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value

    def create(self, validated_data):
        username = self.generate_unique_username()
        user = CustomUser.objects.create_user(username=username, **validated_data)
        return user

    def generate_unique_username(self):
        while True:
            random_username = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=10)
            )
            if not CustomUser.objects.filter(username=random_username).exists():
                return random_username

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_role",
            "user_created_by",
        )

class UserRegistrationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "user_role",
            "user_created_by",
            "process_type"
        )

class PutUserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, read_only=True)
    username = serializers.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = "__all__"

class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ["id", "name"] 

class GetUserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=False, read_only=True)
    username = serializers.CharField(required=False)
    user_created_by = serializers.SerializerMethodField()
    user_role = RoleModelSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"

    def get_user_created_by(self, obj):
            """Returns details of the user who created this user."""
            if obj.user_created_by:
                return {
                    "id": obj.user_created_by.id,
                    "username": obj.user_created_by.username,
                    "email": obj.user_created_by.email,
                    "first_name": obj.user_created_by.first_name,
                    "last_name": obj.user_created_by.last_name,
                }
            return None
        

class UserListViewSerializer(serializers.ModelSerializer):
    user_created_by = serializers.SerializerMethodField()
    user_role = RoleModelSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "last_login",
            "is_superuser",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "user_role",
            "user_created_by",
            "process_type"
        ]

    def get_user_created_by(self, obj):
            """Returns details of the user who created this user."""
            if obj.user_created_by:
                return {
                    "id": obj.user_created_by.id,
                    "username": obj.user_created_by.username,
                    "email": obj.user_created_by.email,
                    "first_name": obj.user_created_by.first_name,
                    "last_name": obj.user_created_by.last_name,
                }
            return None

class UserViewSerializer(serializers.ModelSerializer):
    user_role = RoleModelSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = "__all__"