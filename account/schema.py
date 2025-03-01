from drf_yasg import openapi

# Reusable schema for 400 (Bad Request)
bad_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="failed"),
        "message": openapi.Schema(type=openapi.TYPE_STRING, example="Invalid data"),
        "errors": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            additional_properties=openapi.Schema(type=openapi.TYPE_STRING),
            example={
                "email": "This field is required.",
                "password": "Password is too short.",
            },
        ),
    },
)

# Reusable schema for 500 (Internal Server Error)
internal_server_error_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="failed"),
        "error": openapi.Schema(
            type=openapi.TYPE_STRING, example="Internal server error"
        ),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING,
            example="An error occurred: Database connection failed",
        ),
    },
)

# Reusable schema for 200 (Success Response)
success_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, example="Operation successful"
        ),
        "data": openapi.Schema(type=openapi.TYPE_STRING, default=None),
    },
)

""" Registration Schema """

registration_schema = {
    "request_body": openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL
            ),
            "password": openapi.Schema(type=openapi.TYPE_STRING),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING),
            "process_type": openapi.Schema(type=openapi.TYPE_STRING),
            "user_role": openapi.Schema(type=openapi.TYPE_INTEGER),
            "user_created_by": openapi.Schema(type=openapi.TYPE_INTEGER),
        },
        required=[
            "email",
            "password",
            "first_name",
            "last_name",
            "user_role",
            "user_created_by",
            "process_type",
        ],
    ),
    "responses": {
        200: openapi.Response(
            description="Registration successful", schema=success_response_schema
        ),
        400: openapi.Response(description="Bad Request", schema=bad_request_schema),
        500: openapi.Response(
            description="Internal Server Error", schema=internal_server_error_schema
        ),
    },
}


""" Login Schema """

# Reusable Login Response Schema
login_response_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "status": openapi.Schema(type=openapi.TYPE_STRING, example="success"),
        "message": openapi.Schema(
            type=openapi.TYPE_STRING, example="Login is successfull"
        ),
        "data": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "id": openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                "last_login": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    nullable=True,
                    example=None,
                ),
                "is_superuser": openapi.Schema(
                    type=openapi.TYPE_BOOLEAN, example=False
                ),
                "first_name": openapi.Schema(
                    type=openapi.TYPE_STRING, example="emily.white@example.com"
                ),
                "last_name": openapi.Schema(
                    type=openapi.TYPE_STRING, example="white@example.com"
                ),
                "email": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_EMAIL,
                    example="emily.white@example.com",
                ),
                "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True),
                "date_joined": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format=openapi.FORMAT_DATETIME,
                    example="2025-02-25T07:40:32.410504Z",
                ),
                "role": openapi.Schema(
                    type=openapi.TYPE_STRING, example="Admin | SuperAdmin | Staff"
                ),
                "access": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                ),
                "refresh": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                ),
            },
            required=["id", "email", "access", "refresh"],
        ),
    },
)

# Reusable Login Request Schema
login_request_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        "email": openapi.Schema(
            type=openapi.TYPE_STRING,
            format=openapi.FORMAT_EMAIL,
            example="user@example.com",
        ),
        "password": openapi.Schema(
            type=openapi.TYPE_STRING, example="SecurePassword@123"
        ),
    },
    required=["email", "password"],
)

# Login Response & Response Schema
login_schema = {
    "request_body": login_request_schema,
    "responses": {
        200: openapi.Response(
            description="Login successful", schema=login_response_schema
        ),
        400: openapi.Response(description="Bad Request", schema=bad_request_schema),
        500: openapi.Response(
            description="Internal Server Error", schema=internal_server_error_schema
        ),
    },
}
