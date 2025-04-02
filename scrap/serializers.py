from rest_framework import serializers

""" Import django models here """
from .models import (
    UserScrapHistory,
    ScrapTranslatedContent,
    FireCrawlScrapperModal,
    LanguagesModal,
    FireCrawlScrapperTranslationModal
)
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


class GetScrapTranslatedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapTranslatedContent
        fields = ["id", "language", "name", "content", "content_json"]


class ScrapTranslatedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapTranslatedContent
        fields = "__all__"


class GetUserScrapHistoryListSerializer(serializers.ModelSerializer):
    user = UserRegistrationListSerializer(read_only=True)
    user_scrap_history = ScrapTranslatedContentSerializer(many=True, read_only=True)

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
            "user_scrap_history",
        ]


class FireCrawlScrapperModalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FireCrawlScrapperModal
        fields = "__all__"


class LanguagesModalSerializers(serializers.ModelSerializer):
    class Meta:
        model = LanguagesModal
        fields = "__all__"

class FireCrawlScrapperTranslationModalSerializers(serializers.ModelSerializer):
    class Meta:
        model = FireCrawlScrapperTranslationModal
        fields = "__all__"


class GetUserFireCrawlScrapHistoryListSerializer(serializers.ModelSerializer):
    user = UserRegistrationListSerializer(read_only=True)
    firecrawl_scrapper = FireCrawlScrapperTranslationModalSerializers(many=True, read_only=True)

    class Meta:
        model = FireCrawlScrapperModal
        fields = [
            "id",
            "user",
            "urls",
            "name",
            "tags",
            "data",
            # "firecrawl_id",
            "created_at",
            "updated_at",
            "firecrawl_scrapper",
        ]