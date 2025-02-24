from django.shortcuts import render
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
        "PRODUCT_NAME": {
            "product_link": "",
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
                "context": f"Translate this into {target_language}",
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


def get_jasper_json_data(text):
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

        payload = {
            "inputs": {
                "command": str(text),
                "context": f"Convert the following data into JSON format. Ensure that all language-specific product details are combined into a single object per product, with each language's fields prefixed accordingly, don't miss any data and languages. Follow this structure: {JASPER_JSON_REFERENCE_V2}.",
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


class WebScrapperV2(APIView):
    def post(self, request):
        try:
            if "url" in request.data:
                urls = request.data["url"]
                languages = request.data["languages"]
                combined_languages = ["English"] + languages
                scrapped_data = []
                for url in urls:
                    sd = get_scrapper_data(url=url)
                    scrapped_data.append(sd)
                jasper_translated_data = get_jasper_translation(
                    str(scrapped_data), combined_languages
                )
                jasper_translated_data = jasper_translated_data["data"][0]["text"]
                json_data = get_jasper_json_data(jasper_translated_data)
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
                scrapped_data = []
                for url in urls:
                    sd = get_scrapper_data(url=url)
                    sd["product_link"] = url
                    scrapped_data.append(sd)
                jasper_translated_data = get_jasper_translation(
                    combined_languages, str(scrapped_data)
                )
                jasper_translated_data = jasper_translated_data["data"][0]["text"]
                json_data = get_jasper_json_data(jasper_translated_data)
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
