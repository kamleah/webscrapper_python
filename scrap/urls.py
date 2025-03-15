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
    path("download-scrap/", views.DownloadScrapJson.as_view(), name="scrapper-test"),
    path("history-cleanup/", views.HistoryCleanup.as_view(), name="scrapper-test"),
    path("languages/", views.LanguageListAPI.as_view(), name="firecrawl_scrap_batch"),
    path("firecrawlAPI/", views.FirecrawlAPI.as_view(), name="firecrawlAPI-test"),
    path("scrapwebhook/", views.ScrapWebHook.as_view(), name="firecrawlAPI-test"),
    path("firecrawl-scrap/", views.FirecrawlScrap.as_view(), name="firecrawl_scrap"),
    path("firecrawl-scrap-batch/", views.FirecrawlBatchScrap.as_view(), name="firecrawl_scrap_batch"),
    path("firecrawl-scrap-batch-v2/", views.FirecrawlBatchScrapV2.as_view(), name="firecrawl_scrap_batch"),
    path("firecrawl-scrap/<int:scrap_id>/", views.FireCrawlScrapDetailAPIView.as_view(), name="firecrawl_scrap_batch"),
    path("firecrawl-scrap-translate/", views.FireCrawlScrapDetailTranslateAPIView.as_view(), name="firecrawl_scrap_batch"),
    path("firecrawl-scrap-translate-json/<int:scrap_id>/", views.FireCrawlTranslatedToJSONAPI.as_view(), name="firecrawl_scrap_batch"),
    path("user-firecrawl-scrap-filter/", views.UserFireCrawlScrapperPaginatedView.as_view(), name="scrapper-test"),
    path("delete-firecrawl-history/<int:history_id>/", views.DeleteFireCrawlHistory.as_view(), name="scrapper-test"),
]