from django.shortcuts import render
from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status

from django.utils import timezone
from datetime import date, datetime, timedelta

import random
import json

import requests
from bs4 import BeautifulSoup

""" Imports from rest framework """
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics

# """ Import from Utils here """
from utils.response import (
    create_bad_request_response,
    create_internal_server_error_response,
    create_success_response,
)

from utils.helper_function import BasicPagination

""" Import From Form """
from .forms import ScrapRequestForm, TranslateContentForm

""" Import Schema """
from .schema import request_schema

""" Import Swagger here """
from drf_yasg.utils import swagger_auto_schema

""" Import Serializers """
from .serializers import (
    UserScrapHistorySerializer,
    UserScrapHistoryListSerializer,
    ScrapTranslatedContentSerializer,
    GetUserScrapHistoryListSerializer,
)

from account.serializers import UserListViewSerializer

""" Import Modals """
from .models import UserScrapHistory, ScrapTranslatedContent
from account.models import CustomUser
from django.db.models import Q

""" Import Django Filters """
import django_filters
from django_filters.rest_framework import DjangoFilterBackend


jasper_key = (
    "api_3472BD0447F14F87BD6A61FA954A7FD2:BN41RwfWAEtGVRnF76XsgASplSd11LBuHhaHuYJKzbM="
)


class ScrapperFunction(APIView):
    def get(self, request):
        url = "https://www.sephora.co.uk/p/RARE-BEAUTY-Soft-Pinch-Liquid-Blush"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            # response = requests.get(url, headers=headers, timeout=10)
            # response.raise_for_status()  # Raise HTTP errors (404, 500, etc.)

            # soup = BeautifulSoup(response.content, "html.parser")
            # links = [a["href"] for a in soup.find_all("a", href=True)]

            return Response({"links": "get links"}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        url = "https://www.sephora.co.uk/p/KOSAS-Cloud-Set-Baked-Setting-and-Smoothing-Powder"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()  # Raise HTTP errors (404, 500, etc.)

            soup = BeautifulSoup(response.content, "html.parser")
            product_section = soup.find(class_="pdp-product-brand-name")
            product_text = product_section.get_text(strip=True)

            product_price = soup.find(class_="Price")
            product_price_text = product_price.get_text(strip=True)

            product_description = soup.find(class_="Layout-golden-main")
            product_description_text = product_description.get_text(strip=True)

            payloads = {
                "price": product_price_text,
                "name": product_text,
                "description": product_description_text,
            }

            jasperurl = "https://api.jasper.ai/v1/command"

            payload = {
                "inputs": {
                    "command": str(payloads),
                    "context": "translate it in spanish, japanese, in proper language to render in html with proper json",
                },
                "options": {
                    "outputCount": 1,
                    "outputLanguage": "English",
                    "inputLanguage": "English",
                    "languageFormality": "default",
                    "completionType": "performance",
                },
            }
            headers = {
                "accept": "application/json",
                "content-type": "application/json",
                "X-API-Key": jasper_key,
            }

            response = requests.post(jasperurl, json=payload, headers=headers)

            # print(response.text)

            return Response({"links": "links"}, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# {
# "url":"https://www.sephora.co.uk/p/tatcha-the-dewy-cream-50ml"
# }


def markdown_to_json(markdown):
    translations = []
    sections = markdown.split("### ")[1:]  # Split by language sections

    for section in sections:
        lines = section.split("\n")
        language = lines[0].strip()  # Extract language
        details = {}

        for line in lines[1:]:
            if line.startswith("**"):
                key, value = line.split(":", 1)
                key = key.replace("**", "").strip()
                value = value.strip()
                details[key] = value

        translations.append({"language": language, "details": details})

    return translations


""" Actual Working Codes """
web_scrapper_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

""" JASPER API """
jasper_api_endpoints = "https://api.jasper.ai/v1/command"

prompt_1 = f"Translate this into {"target_language"} and don't miss any language.Output should be in text. Each of the product transalated data add some divider or seprrator to verify different products with all the languages."


class WebScrapper(APIView):
    def post(self, request):
        try:
            if "url" in request.data:

                # Process to scrapp the details from the web starts here
                url = request.data["url"]
                languages = request.data["languages"]

                response = requests.get(url, headers=web_scrapper_header, timeout=10)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")
                product_name = soup.find(class_="pdp-product-brand-name")
                product_name_text = product_name.get_text(strip=True)

                product_price = soup.find(class_="Price")
                product_price_text = product_price.get_text(strip=True)

                product_description = soup.find(class_="Layout-golden-main")
                product_description_text = product_description.get_text(strip=True)

                payload = {
                    "price": product_price_text,
                    "name": product_name_text,
                    "description": product_description_text,
                }

                jasper_api_payload = {
                    "inputs": {
                        "command": str(payload),
                        "context": f"translate it in {languages}",
                    },
                    "options": {
                        "outputCount": 1,
                        "outputLanguage": "English",
                        "inputLanguage": "English",
                        "languageFormality": "default",
                        "completionType": "performance",
                    },
                }

                headers = {
                    "accept": "application/json",
                    "content-type": "application/json",
                    "X-API-Key": jasper_key,
                }

                response = requests.post(
                    jasper_api_endpoints, json=jasper_api_payload, headers=headers
                )

                json_response = response.json()
                json_ref = [
                    {
                        "language": "",
                        "name": "",
                        "price": "",
                        "description": "",
                        "ingredients": "",
                    }
                ]
                # -----------------------------------------------------------------------------------
                jasper_api_payload2 = {
                    "inputs": {
                        "command": str(json_response["data"][0]["text"]),
                        "context": f"convert data into json, json ref {json_ref}",
                    },
                    "options": {
                        "outputCount": 2,
                        "outputLanguage": "English",
                        "inputLanguage": "English",
                        "languageFormality": "default",
                        "completionType": "performance",
                    },
                }

                response2 = requests.post(
                    jasper_api_endpoints, json=jasper_api_payload2, headers=headers
                )

                json_response2 = response2.json()
                aa = json_response2["data"][0]["text"].split("```json")
                bb = aa[1].split("```")
                import json

                cc = json.loads(bb[0])
                headers = list(cc[0].keys())

                return Response(
                    {"data": json_response, "json": cc},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "URL not provided"}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


JASPER_API_KEY = (
    "api_3472BD0447F14F87BD6A61FA954A7FD2:BN41RwfWAEtGVRnF76XsgASplSd11LBuHhaHuYJKzbM="
)
JASPER_API_URL = "https://api.jasper.ai/v1/command"

JASPER_API_OPTION = {
    "outputCount": 1,
    "outputLanguage": "English",
    "inputLanguage": "English",
    "languageFormality": "default",
    "completionType": "performance",
}

JASPER_API_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": JASPER_API_KEY,
}

JASPER_JSON_REFERENCE = [
    {
        "language": "",
        "name": "",
        "price": "",
        "description": "",
        "ingredients": "",
    }
]

JASPER_JSON_REFERENCE_V2 = [
    {
        "PRODUCT_NAME_IN_ENGLISH": {
            "product_link": "",
            "english_language_name": "",
            "english_language_description": "",
            "english_language_price": "",
            "language_first_language_name": "",
            "language_first_language_description": "",
            "language_first_language_price": "",
            "language_second_language_name": "",
            "language_second_language_description": "",
            "language_second_language_price": "",
            "language_other_language_name": "",
            "language_other_language_description": "",
            "language_other_language_price": "",
        }
    }
]


def create_jasper_json_reference(product_name, languages):
    """
    Create a dynamic JASPER JSON reference structure based on provided languages.

    Args:
        product_name (str): Product name in English.
        languages (list): List of languages to include.

    Returns:
        dict: JASPER JSON reference structure.
    """
    # Base structure for English
    language_structure = {
        "product_link": "",
        "english_language_name": "",
        "english_language_description": "",
        "english_language_price": "",
    }

    # Dynamically add fields for each language
    for index, lang in enumerate(languages):
        prefix = f"{lang.lower()}_language"
        language_structure[f"{prefix}_name"] = ""
        language_structure[f"{prefix}_description"] = ""
        language_structure[f"{prefix}_price"] = ""

    # Create final structured JSON
    jasper_json = {product_name: language_structure}

    return jasper_json


def get_scrapper_data(url):
    try:
        empty_payload = {"price": "", "name": "", "description": ""}
        if url:
            response = requests.get(url, headers=web_scrapper_header, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            product_name = soup.find(class_="pdp-product-brand-name")
            product_name_text = product_name.get_text(strip=True)

            product_price = soup.find(class_="Price")
            product_price_text = product_price.get_text(strip=True)

            product_description = soup.find(class_="Layout-golden-main")
            product_description_text = product_description.get_text(strip=True)

            payload = {
                "price": product_price_text,
                "name": product_name_text,
                "description": product_description_text,
                "url": url,
            }
            return payload
        else:
            return empty_payload
    except Exception as e:
        return empty_payload


def get_jasper_translation(text, target_language):
    """
    Translates the given text into the specified target language using the Jasper API.

    :param text: The text to be translated.
    :param target_language: The language to translate the text into.
    :return: Translated text or an error response.
    """
    try:
        if not text or not target_language:
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = {
            "inputs": {
                "command": str(text),
                "context": f"Translate this into {target_language} without missing any details."
                "The output should be in text format. Separate each product's translated data "
                "with a clear divider or separator to distinguish between different products "
                "and their respective languages."
                "Transalate product name also in {target_language}",
            },
            "options": JASPER_API_OPTION,
        }

        response = requests.post(
            JASPER_API_URL, json=payload, headers=JASPER_API_HEADERS
        )
        response_data = response.json()

        if response.status_code != 201:
            return Response(
                {"error": response_data.get("message", "Translation failed")},
                status=response.status_code,
            )

        return response_data

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_jasper_json_data(text, languages, product_names):
    """
    Converts given text into a JSON format using Jasper API.

    :param text: The input text to be converted into JSON.
    :return: A dictionary containing the parsed JSON data or an error response.
    """
    try:
        if not text:
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        languages_results = create_jasper_json_reference(
            "product_name_in_english", languages
        )

        payload = {
            "inputs": {
                "command": str(text),
                "context": f"Convert the following data into JSON format. Ensure that all language-specific product details are combined into a single object per product, with each language's fields prefixed accordingly, don't miss any data and languages. Follow this structure: {[languages_results]}. and don't miss any language. product_name_in_english key should be match from this array of products {product_names} and object should be match same as {[languages_results]}.",
            },
            "options": JASPER_API_OPTION,
        }

        response = requests.post(
            JASPER_API_URL, json=payload, headers=JASPER_API_HEADERS
        )
        response_data = response.json()

        # Extract JSON response from text
        json_text_parts = response_data["data"][0]["text"].split("```json")
        if len(json_text_parts) < 2:
            return Response(
                {"error": "Invalid JSON format received from API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        json_block = json_text_parts[1].split("```")[0].strip()
        parsed_json = json.loads(json_block)

        return {"data": parsed_json}

    except json.JSONDecodeError:
        return Response(
            {"error": "Failed to parse JSON response"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except KeyError:
        return Response(
            {"error": "Unexpected API response format"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def convert_content_to_json_data(text):
    try:
        if not text:
            return Response(
                {"error": "Missing required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        payload = {
            "inputs": {
                "command": str(text),
                "context": f"Convert the following data into JSON format properly.json shouldn't have any parent key, and inside of the json also don't add any parent key",
            },
            "options": JASPER_API_OPTION,
        }

        response = requests.post(
            JASPER_API_URL, json=payload, headers=JASPER_API_HEADERS
        )
        response_data = response.json()
        json_text_parts = response_data["data"][0]["text"].split("```json")
        if len(json_text_parts) < 2:
            return Response(
                {"error": "Invalid JSON format received from API"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        json_block = json_text_parts[1].split("```")[0].strip()
        parsed_json = json.loads(json_block)

        return parsed_json
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WebScrapperV2(APIView):
    def post(self, request):
        try:
            if "url" in request.data:
                urls = request.data["url"]
                languages = request.data["languages"]
                combined_languages = ["English"] + languages
                scrapped_data = []
                for index, url in enumerate(urls):
                    sd = get_scrapper_data(url=url)
                    scrapped_data.append(sd)
                jasper_translated_data = get_jasper_translation(
                    str(scrapped_data), combined_languages
                )
                jasper_translated_data = jasper_translated_data["data"][0]["text"]
                json_data = get_jasper_json_data(
                    jasper_translated_data, combined_languages
                )
                return Response(
                    {"data": jasper_translated_data, "json": json_data["data"]},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "URL not provided"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class WebScrapperV3(APIView):
    def post(self, request):
        try:
            if "url" in request.data:
                urls = request.data["url"]
                languages = request.data["languages"]
                combined_languages = languages + ["English"]
                product_names = []

                scrapped_data = []
                for index, url in enumerate(urls):
                    sd = get_scrapper_data(url=url)
                    sd["product_link"] = url
                    product_names.append(sd["name"])
                    scrapped_data.append(sd)
                jasper_translated_data = get_jasper_translation(
                    combined_languages, str(scrapped_data)
                )
                jasper_translated_data = jasper_translated_data["data"][0]["text"]
                json_data = get_jasper_json_data(
                    jasper_translated_data, combined_languages, product_names
                )
                return Response(
                    {"data": jasper_translated_data, "json": json_data["data"]},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "URL not provided"}, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserScraperAPIView(APIView):

    @swagger_auto_schema(tags=["User Scraper"])
    def get(self, request):
        try:
            da = UserScrapHistory.objects.all()
            sdd = UserScrapHistorySerializer(da, many=True).data
            return create_success_response(message="Scraping successful", data=sdd)
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))

    @swagger_auto_schema(
        tags=["User Scraper"],
        request_body=request_schema,
    )
    def post(self, request):
        try:
            # Validate request data using form
            scrap_form = ScrapRequestForm(data=request.data)
            if not scrap_form.is_valid():
                return create_bad_request_response(errors=scrap_form.errors)

            # Extract request data
            user_id = request.data["user"]
            urls = request.data["urls"]
            search_keywords = request.data["search_keywords"]
            metadata_fields = request.data["metadata_fields"]

            # Scrape data efficiently using list comprehension
            scraped_data = [get_scrapper_data(url) for url in urls]

            # Save history record
            history_data = {
                "user": user_id,
                "urls": urls,
                "search_keywords": search_keywords,
                "metadata_fields": metadata_fields,
                "scrap_data": scraped_data,
            }

            history_serializer = UserScrapHistorySerializer(data=history_data)
            if history_serializer.is_valid():
                history_serializer.save()
                saved_id = history_serializer.instance.id
            else:
                return create_bad_request_response(errors=history_serializer.errors)

            return create_success_response(
                message="Scraping successful",
                data={"scraped_data": scraped_data, "scraped_id": saved_id},
            )

        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


class GetScrapperData(APIView):
    def get(self, request, *args, **kwargs):
        try:
            scrapped_id = kwargs["scrapped_id"]
            scrapped_data = UserScrapHistory.objects.get(id=scrapped_id)
            scrapped_data_serializer = UserScrapHistorySerializer(scrapped_data).data
            return create_success_response(
                message="Scraping successful",
                data={"scraped_data": scrapped_data_serializer},
            )
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


class UserScrapperFilter(django_filters.FilterSet):
    urls = django_filters.CharFilter(lookup_expr="icontains")
    search_keywords = django_filters.CharFilter(lookup_expr="icontains")
    metadata_fields = django_filters.CharFilter(lookup_expr="icontains")
    scrap_data = django_filters.CharFilter(lookup_expr="icontains")
    user = django_filters.CharFilter(method="filter_created_by")

    class Meta:
        model = UserScrapHistory
        fields = ["urls", "search_keywords", "metadata_fields", "scrap_data", "user"]

    def filter_created_by(self, queryset, name, value):
        """
        Filter by user_created_by's email, first_name, or last_name in a single filter.
        """
        return queryset.filter(
            Q(user__id__icontains=value)
            | Q(user__email__icontains=value)
            | Q(user__first_name__icontains=value)
            | Q(user__last_name__icontains=value)
        )


@swagger_auto_schema(tags=["Search User Scrapper"])
class UserScrapperPaginatedView(generics.ListAPIView):
    serializer_class = GetUserScrapHistoryListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserScrapperFilter
    pagination_class = BasicPagination

    def get_queryset(self):
        requested_user_id = self.request.query_params.get("user_id")

        if not requested_user_id:
            return UserScrapHistory.objects.none()

        try:
            requested_user = CustomUser.objects.get(id=requested_user_id)
            user_serialized_data = UserListViewSerializer(requested_user).data

            if user_serialized_data["user_role"]["name"] == "SuperAdmin":
                return UserScrapHistory.objects.prefetch_related(
                    "user_scrap_history"
                ).order_by("-created_at")
            else:
                return (
                    UserScrapHistory.objects.filter(user=requested_user)
                    .order_by("-created_at")
                    .prefetch_related("user_scrap_history")
                )

        except CustomUser.DoesNotExist:
            return UserScrapHistory.objects.none()


class DeleteHistory(APIView):
    def get(self, request, *args, **kwargs):
        try:
            history_id = kwargs["history_id"]
            history_data = UserScrapHistory.objects.prefetch_related(
                "user_scrap_history"
            ).get(id=history_id)
            serialized_history_data = GetUserScrapHistoryListSerializer(
                history_data
            ).data
            return create_success_response(
                message="History deleted successful", data=serialized_history_data
            )
        except UserScrapHistory.DoesNotExist:
            return create_bad_request_response(errors="History Does Not Exist")
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))

    def delete(self, request, *args, **kwargs):
        try:
            history_id = kwargs["history_id"]
            history_data = UserScrapHistory.objects.get(id=history_id)
            history_data.delete()
            return create_success_response(message="History deleted successful")
        except UserScrapHistory.DoesNotExist:
            return create_bad_request_response(errors="History Does Not Exist")
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


def flatten_json(nested_dict, prefix=""):
    """Recursively flattens a nested JSON structure with prefixed keys."""
    flattened_dict = {}

    for key, value in nested_dict.items():
        new_key = f"{prefix}_{key}" if prefix else key

        if isinstance(value, dict):  # If value is a nested dictionary, recurse
            flattened_dict.update(flatten_json(value, new_key))
        else:
            flattened_dict[new_key] = value  # Assign the value directly

    return flattened_dict


def get_grouped_scraped_data_v1(scrapped_id):
    """
    Retrieves and groups scraped product data by URL with translations.

    :param scrapped_id: The ID of the scraped data entry.
    :return: A list of grouped product data dictionaries.
    """
    try:
        scrapped_translate_data = ScrapTranslatedContent.objects.filter(
            user_scrap_history=scrapped_id
        )
        scrapped_translate_data_serializer = ScrapTranslatedContentSerializer(
            scrapped_translate_data, many=True
        ).data

        grouped_data = defaultdict(lambda: {"product_name": None, "url": None})

        for scrapped_transalsted_data in scrapped_translate_data_serializer:
            formatted_data = format_content_json(
                scrapped_transalsted_data["content_json"]
            )
            url = scrapped_transalsted_data["url"]
            product_name = scrapped_transalsted_data["name"]
            language = scrapped_transalsted_data["language"]

            if not grouped_data[url]["product_name"]:
                grouped_data[url]["product_name"] = product_name
                grouped_data[url]["url"] = url

            for key, value in formatted_data.items():
                print(key)
                print(language)
                grouped_data[url][f"{language}_{key}"] = value

        return list(grouped_data.values())

    except Exception as e:
        raise Exception(f"Error while fetching and grouping scraped data: {str(e)}")


def get_grouped_scraped_data(scrapped_id):
    """
    Retrieves and groups scraped product data by URL with translations.

    :param scrapped_id: The ID of the scraped data entry.
    :return: A list of grouped product data dictionaries.
    """
    try:
        scrapped_translate_data = ScrapTranslatedContent.objects.filter(
            user_scrap_history=scrapped_id
        )
        scrapped_translate_data_serializer = ScrapTranslatedContentSerializer(
            scrapped_translate_data, many=True
        ).data

        grouped_data = defaultdict(lambda: {"product_name": None, "url": None})

        for scrapped_translated_data in scrapped_translate_data_serializer:
            url = scrapped_translated_data.get("url", "N/A")  # Fallback if missing
            product_name = scrapped_translated_data.get("name", "Unknown Product")
            language = scrapped_translated_data.get("language", "unknown")

            # Ensure content_json exists before processing
            content_json = scrapped_translated_data.get("content_json", {})
            if content_json.get("product"):
                content_json = content_json.get("product")
            else:
                content_json = content_json

            formatted_data = format_content_json(content_json) if content_json else {}
            # print(formatted_data)
            formatted_data = flatten_json(formatted_data)

            if not grouped_data[url]["product_name"]:
                grouped_data[url]["product_name"] = product_name
                grouped_data[url]["url"] = url

            for key, value in formatted_data.items():
                grouped_data[url][f"{language}_{key}"] = value

        return list(grouped_data.values())

    except Exception as e:
        raise Exception(f"Error while fetching and grouping scraped data: {str(e)}")


class TranslateContentAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            translate_content_form = TranslateContentForm(data=data)
            if not translate_content_form.is_valid():
                return create_bad_request_response(errors=translate_content_form.errors)

            content_id = data.get("content_id")
            translated_languages = data.get("languages")

            # Fetch user scrap history
            try:
                scrap_history = UserScrapHistory.objects.get(id=content_id)
            except UserScrapHistory.DoesNotExist:
                return create_bad_request_response(errors="Invalid content_id provided")

            scrap_data = UserScrapHistorySerializer(scrap_history).data.get(
                "scrap_data", []
            )

            translated_results = []

            for content in scrap_data:
                for language in translated_languages:
                    if language is not "English":
                        translation_response = get_jasper_translation(
                            str(content), [language]
                        )
                        translated_text = translation_response.get("data", [{}])[0].get(
                            "text", ""
                        )
                    else:
                        translated_text = f"""---
                            **{content['name']}**
                            Price: {content['price']}
                            Description: {content['description']}
                            ---"""

                    translated_results.append(
                        {
                            "language": language,
                            "name": content.get("name", ""),
                            "content": translated_text,
                        }
                    )

                    # Save translation
                    translation_entry = {
                        "user_scrap_history": content_id,
                        "language": language,
                        "name": content.get("name", ""),
                        "content": translated_text,
                        "url": content.get("url", ""),
                    }
                    translation_serializer = ScrapTranslatedContentSerializer(
                        data=translation_entry
                    )

                    if translation_serializer.is_valid():
                        translation_serializer.save()

            return create_success_response(
                message="Translation successful",
                data=translated_results,
            )

        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


class GetTranslationResult(APIView):
    def get(self, request, *args, **kwargs):
        try:
            transalated_content_id = kwargs["transalated_content"]
            translated_content_data = ScrapTranslatedContent.objects.filter(
                user_scrap_history=transalated_content_id
            )

            if not translated_content_data.exists():
                return create_bad_request_response(errors="Invalid content_id provided")

            translated_content_data_serialized = ScrapTranslatedContentSerializer(
                translated_content_data, many=True
            ).data

            # Process content and convert to JSON
            translated_content = [
                {
                    **tData,
                    "content_json": convert_content_to_json_data(tData["content"]),
                }
                for tData in translated_content_data_serialized
            ]

            for tc in translated_content:
                ScrapTranslatedContent.objects.filter(id=tc["id"]).update(
                    content_json=tc["content_json"]
                )

            translated_content_data = ScrapTranslatedContent.objects.filter(
                user_scrap_history=transalated_content_id
            ).order_by("id")

            translated_content_data_serialized = ScrapTranslatedContentSerializer(
                translated_content_data, many=True
            ).data

            grouped_list = get_grouped_scraped_data(transalated_content_id)
            return create_success_response(
                message="Translation successful", data=grouped_list
            )
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


class GetScrapperTranslatedData(APIView):
    def get(self, request, *args, **kwargs):
        try:
            scrapped_id = kwargs["scrapped_id"]

            scrapped_data = ScrapTranslatedContent.objects.filter(
                user_scrap_history=scrapped_id
            )
            scrapped_data_serializer = ScrapTranslatedContentSerializer(
                scrapped_data, many=True
            ).data
            return create_success_response(
                message="Scraping successful",
                data={"scraped_data": scrapped_data_serializer},
            )
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


def format_content_json(content_json):
    formatted_data = {}

    for key, value in content_json.items():
        if isinstance(value, list):  # If value is a list, join elements with commas
            formatted_data[key] = f"{key}: " + ", ".join(map(str, value))
        elif isinstance(
            value, dict
        ):  # If value is a dictionary, format key-value pairs
            formatted_data[key] = f"{key}: " + ", ".join(
                f"{sub_key}: {sub_value}" for sub_key, sub_value in value.items()
            )
        else:  # If value is a string or number, keep it as is
            formatted_data[key] = f"{key}: {value}"

    return formatted_data


# class DownloadScrapJsonV1(APIView):
#     def post(self, request):
#         try:
#             scrapped_id = 79
#             scrapped_data = UserScrapHistory.objects.get(id=scrapped_id)
#             scrapped_serialized_data = UserScrapHistorySerializer(scrapped_data).data

#             scrapped_translate_data = ScrapTranslatedContent.objects.filter(
#                 user_scrap_history=scrapped_id
#             )
#             scrapped_translate_data_serializer = ScrapTranslatedContentSerializer(
#                 scrapped_translate_data, many=True
#             ).data

#             dsd = []
#             for index, scrapped_transalsted_data in enumerate(
#                 scrapped_translate_data_serializer, start=1
#             ):
#                 formatted_data = format_content_json(
#                     scrapped_transalsted_data["content_json"]
#                 )
#                 # print(f"{index}: {formatted_data}")
#                 dsd.append(
#                     {
#                         "content": formatted_data,
#                         "url": scrapped_transalsted_data["url"],
#                         "product_name": scrapped_transalsted_data["name"],
#                         "language":scrapped_transalsted_data["language"],
#                     }
#                 )

#             print(dsd)

#             return create_success_response(
#                 message="Scraping successful",
#                 data={"scraped_data": dsd},
#             )
#         except Exception as e:
#             return create_internal_server_error_response(exception=str(e))

from collections import defaultdict


class DownloadScrapJsonV2(APIView):
    def post(self, request):
        try:
            scrapped_id = 79
            scrapped_data = UserScrapHistory.objects.get(id=scrapped_id)
            scrapped_serialized_data = UserScrapHistorySerializer(scrapped_data).data

            scrapped_translate_data = ScrapTranslatedContent.objects.filter(
                user_scrap_history=scrapped_id
            )
            scrapped_translate_data_serializer = ScrapTranslatedContentSerializer(
                scrapped_translate_data, many=True
            ).data

            grouped_data = defaultdict(
                lambda: {"product_name": None, "translations": []}
            )

            for scrapped_transalsted_data in scrapped_translate_data_serializer:
                formatted_data = format_content_json(
                    scrapped_transalsted_data["content_json"]
                )
                url = scrapped_transalsted_data["url"]
                product_name = scrapped_transalsted_data["name"]

                # Store product name (ensures it's not overwritten)
                if not grouped_data[url]["product_name"]:
                    grouped_data[url]["product_name"] = product_name

                # Append translation details
                grouped_data[url]["translations"].append(
                    {
                        "content": formatted_data,
                        "language": scrapped_transalsted_data["language"],
                    }
                )

            # Convert grouped_data dictionary into a list
            grouped_list = [
                {
                    "url": url,
                    "product_name": data["product_name"],
                    "translations": data["translations"],
                }
                for url, data in grouped_data.items()
            ]

            return create_success_response(
                message="Scraping successful",
                data={"scraped_data": grouped_list},
            )
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))


class DownloadScrapJson(APIView):
    def post(self, request):
        try:

            scrapped_id = request.data.get("scrapped_id")
            if not scrapped_id:
                return create_internal_server_error_response(
                    "Missing scrapped_id in request."
                )

            grouped_list = get_grouped_scraped_data(scrapped_id)

            return create_success_response(
                message="Scraping completed successfully. The translated product data has been grouped by URL.",
                data=grouped_list,
            )
        except Exception as e:
            return create_internal_server_error_response(exception=str(e))
