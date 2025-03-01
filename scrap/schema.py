from drf_yasg import openapi

request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "user": openapi.Schema(type=openapi.TYPE_INTEGER, example=1),
        "urls": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING, format=openapi.FORMAT_URI),
            example=[
                "https://www.sephora.co.uk/p/KOSAS-Cloud-Set-Baked-Setting-and-Smoothing-Powder",
                "https://www.sephora.co.uk/p/KOSAS-Cloud-Set-Baked-Setting-and-Smoothing-Powder"
            ],
        ),
        "search_keywords": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(type=openapi.TYPE_STRING),
            example=[
                "KOSAS Cloud Set Baked Setting & Smoothing Powder 9.5g",
                "KOSAS Cloud Set Baked Setting & Smoothing Powder 9.5g"
            ],
        ),
        "metadata_fields": openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_STRING,
                enum=["product_name", "product_description"]
            ),
            example=["product_name", "product_description"],
        ),
    },
    required=["user", "urls", "search_keywords", "metadata_fields"]
)