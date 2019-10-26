from datetime import timedelta
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import exceptions, permissions, generics
from rest_framework.views import APIView, status
from rest_framework.response import Response
from decouple import config
from ..util.messages import USER_CREATED, USER_NAME_EXISTS
from ..util.builders import ResponseBuilder

ResponseBuilder = ResponseBuilder()
import logging
logger = logging.getLogger('testlogger')
UNIQUE_CONSTRAINT = 'unique constraint'

class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            User.objects.create_user(
                username=request.data['username'], password=request.data['password'], email=request.data['email'])
            return ResponseBuilder.get_response(message=USER_CREATED, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            transaction.rollback()
            logger.error('User Creation Failed: {}'.format(e.args[0]))
            if(UNIQUE_CONSTRAINT in e.args[0].lower()):
                return ResponseBuilder.get_response(message=USER_NAME_EXISTS, status=status.HTTP_409_CONFLICT)
            return ResponseBuilder.get_response(message=e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

