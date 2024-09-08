import logging
from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from rest_framework import status
from django.utils.datastructures import MultiValueDictKeyError


logger = logging.getLogger('info')
logger_error = logging.getLogger('error')


def custom_exception_handler(exc, context):

    # Call REST framework's default exception handler first

    response = exception_handler(exc, context)

    if isinstance(exc, ObjectDoesNotExist):
        err_data = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'No data found'}
        exception_name = str(exc).split("DETAIL: ")
        logger_error.error(exception_name)
        return Response(err_data)

    elif isinstance(exc, KeyError):
        err_data = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Please enter all the data'}
        exception_name = str(exc).split("DETAIL: ")
        logger_error.error(exception_name)
        return Response(err_data)

    elif isinstance(exc, AttributeError):
        err_data = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Please enter all the data'}
        exception_name = str(exc).split("DETAIL: ")
        logger_error.error(exception_name)
        return Response(err_data)

    elif isinstance(exc, (TypeError, ValueError, ValidationError)):
        err_data = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid Input'}
        exception_name = str(exc).split("DETAIL: ")
        logger_error.error(exception_name)
        return Response(err_data)

    elif isinstance(exc, MultiValueDictKeyError):
        err_data = {'status': status.HTTP_400_BAD_REQUEST, 'message': 'Please enter all the data'}
        exception_name = str(exc).split("DETAIL: ")
        logger_error.error(exception_name)
        return Response(err_data)

    return response
