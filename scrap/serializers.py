from rest_framework import serializers

""" Import django models here """
from .models import UserScrapHistory, ScrapTranslatedContent
from account.models import CustomUser

""" Import Serializers """
from account.serializers import UserRegistrationListSerializer


class UserScrapHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserScrapHistory
        fields = "__all__"


class UserScrapHistoryListSerializer(serializers.ModelSerializer):
    user = UserRegistrationListSerializer(read_only=True)

    class Meta:
        model = UserScrapHistory
        fields = [
            "id",
            "user",
            "urls",
            "search_keywords",
            "metadata_fields",
            "scrap_data",
            "created_at",
            "updated_at",
        ]


class ScrapTranslatedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapTranslatedContent
        fields = "__all__"
