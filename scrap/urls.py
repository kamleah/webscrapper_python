from django.urls import path
from . import views

urlpatterns = [
    path("web-scrapping-v3/", views.WebScrapperV3.as_view(), name="scrapper-test"),
]