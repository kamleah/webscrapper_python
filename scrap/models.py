from django.db import models
from django.utils import timezone

# """ Import Models From Account App """
from account.models import CustomUser

# Create your models here.


class UserScrapHistory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, null=True, blank=True
    )
    urls = models.JSONField(default=list)
    search_keywords = models.JSONField(default=list)
    metadata_fields = models.JSONField(default=list)
    scrap_data = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        first_url = self.urls[0] if self.urls else "No URLs"
        return f"{self.id} | {self.user.username if self.user else 'Anonymous'} | {first_url}"


class ScrapTranslatedContent(models.Model):
    id = models.AutoField(primary_key=True)
    user_scrap_history = models.ForeignKey(
        UserScrapHistory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="user_scrap_history",
    )
    language = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    content_json = models.JSONField(default=dict, null=True, blank=True)


    def __str__(self):
        return f"{self.id} | {self.language} | {self.name}"
    
