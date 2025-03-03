from rest_framework.response import Response
from rest_framework import status


def create_internal_server_error_response(exception=None, message=None):
    """
    Creates a response for internal server errors.

    Args:
        exception (Exception, optional): The exception that occurred (if any).
        message (str, optional): Additional message to include in the response.

    Returns:
        Response: A Response object representing an internal server error with appropriate error message.

    Example:
        create_internal_server_error_response(exception, message)

    """
    # Construct the error message based on provided exception and message
    error_message = "An error occurred"
    if exception:
        error_message += f": {str(exception)}"
    if message:
        error_message += f": {message}"

    # Create the error response dictionary
    error_response = {
        "status": "failed",
        "error": "Internal server error",
        "message": error_message,
    }

    # Return the response with HTTP status 500
    return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def create_bad_request_response(errors=None, message="Invalid data"):
    """
    Creates a response for bad request errors.

    Args:
        errors (dict, optional): A dictionary containing detailed error messages (default: None).
        message (str, optional): A general error message to include in the response (default: "Invalid data").

    Returns:
        Response: A Response object representing a bad request error with appropriate error message and details.

    Example:
        create_bad_request_response(errors={"field_name": "Error message"}, message="Custom message")
    """
    # Construct the response data dictionary
    response_data = {
        "status": "failed",
        "message": message,
        "errors": errors if errors else {},
    }

    # Return the response with HTTP status 400
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

def create_not_found_response(errors=None, message="Resource not found"):
    """
    Creates a response for not found errors.

    Args:
        errors (dict, optional): A dictionary containing detailed error messages (default: None).
        message (str, optional): A general error message to include in the response (default: "Resource not found").

    Returns:
        Response: A Response object representing a not found error with appropriate error message and details.

    Example:
        create_not_found_response(errors={"field_name": "Error message"}, message="Custom message")
    """
    # Construct the response data dictionary
    response_data = {
        "status": "failed",
        "message": message,
        "errors": errors if errors else {},
    }

    # Return the response with HTTP status 404
    return Response(response_data, status=status.HTTP_404_NOT_FOUND)

def create_success_response(data=None, message="Data is valid"):
    """
    Creates a response for successful requests.

    Args:
        data (dict, optional): Data to include in the response (default: None).
        message (str, optional): A message to include in the response (default: "Data is valid").

    Returns:
        Response: A Response object representing a successful response with appropriate data and message.

    Example:
        create_success_response(data={"key": "value"}, message="Custom success message")
    """
    # Construct the response data dictionary
    response_data = {
        "status": "success",
        "message": message,
        "data": data,
    }

    # Return the response with HTTP status 200
    return Response(response_data, status=status.HTTP_200_OK)

def create_payment_required_response(data=None, message="Payment is required"):
    """
    Creates a response indicating that payment is required.

    Args:
        data (dict, optional): Additional data to include in the response (default: None).
        message (str, optional): A custom message to include in the response (default: "Payment is required").

    Returns:
        Response: A Response object representing a payment required error with appropriate message and data.

    Example:
        create_payment_required_response(data={"key": "value"}, message="Custom payment message")
    """
    # Construct the response data dictionary
    response_data = {
        "status": "error",
        "code": "PAYMENT_REQUIRED",
        "message": message,
        "data": data,
    }

    # Return the response with HTTP status 402
    return Response(response_data, status=status.HTTP_402_PAYMENT_REQUIRED)
