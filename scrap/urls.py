from django.urls import path
from . import views

urlpatterns = [
    path("web-scrapping-v3/", views.WebScrapperV3.as_view(), name="scrapper-test"),
    path("user-scrapping/", views.UserScraperAPIView.as_view(), name="scrapper-test"),
    path("user-scrap-filter/", views.UserScrapperPaginatedView.as_view(), name="scrapper-test"),
    path("scrapped/<int:scrapped_id>/", views.GetScrapperData.as_view(), name="scrapper-test"),
    path("translate-content/", views.TranslateContentAPI.as_view(), name="scrapper-test"),
    path("delete-history/<int:history_id>/", views.DeleteHistory.as_view(), name="scrapper-test"),
    path("translations-results/<int:transalated_content>/", views.GetTranslationResult.as_view(), name="scrapper-test"),
    path("scrap-translations-results/<int:scrapped_id>/", views.GetScrapperTranslatedData.as_view(), name="scrapper-test"),
]