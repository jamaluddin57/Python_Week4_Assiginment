from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied as DjangoPermissionDenied
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, APIException

def custom_exception_handler(exc, context):
    """
    Custom exception handler that handles common and unexpected exceptions in DRF.
    """
    # Call REST framework's default exception handler first to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        return response

    # Custom handling for specific exceptions
    if isinstance(exc, IntegrityError):
        return Response(
            {"detail": "Database integrity error."},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, DatabaseError):
        return Response(
            {"detail": "Database error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    elif isinstance(exc, ObjectDoesNotExist):
        return Response(
            {"detail": "The requested resource was not found."},
            status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, DjangoPermissionDenied):
        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN
        )
    elif isinstance(exc, ValidationError):
        return Response(
            {"detail": "Invalid data provided."},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, PermissionDenied):
        return Response(
            {"detail": "Permission denied."},
            status=status.HTTP_403_FORBIDDEN
        )
    elif isinstance(exc, NotFound):
        return Response(
            {"detail": "Not Found."},
            status=status.HTTP_404_NOT_FOUND
        )
    elif isinstance(exc, AssertionError):
        return Response(
            {"detail": "Assertion failed. Check your assumptions."},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, TypeError):
        return Response(
            {"detail": f"A type error occurred. Please check your data.{TypeError}"},
            status=status.HTTP_400_BAD_REQUEST
        )
    elif isinstance(exc, APIException):
        return Response(
            {"detail": str(exc.detail)},
            status=exc.status_code
        )
    else:
        # Catch-all for any other unhandled exceptions
        return Response(
            {"detail": "An unexpected error occurred."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
