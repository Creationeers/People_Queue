from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import exceptions, permissions, generics
from rest_framework.views import APIView, status
from rest_framework.response import Response
from decouple import config
from ..util.messages import USER_CREATED, USER_NAME_EXISTS, MISSING_FIELD
from ..util.builders import ResponseBuilder
from ..models import Profile, Venue

ResponseBuilder = ResponseBuilder()
import logging
logger = logging.getLogger('testlogger')
UNIQUE_CONSTRAINT = 'unique constraint'

class RegisterUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            with transaction.atomic():
                user = User.objects.create_user(
                    username=request.data['username'], password=request.data['password'], email=request.data['email'])
                profile = Profile.objects.get(user=user)
                profile.ad_consent_available = request.data['is_commercial_user'].lower().capitalize()
                profile.is_commercial_user = request.data['ad_consent_available'].lower().capitalize()
                profile.save()
                logger.info('User {} with Profile ID {} Created Successfully'.format(user.username, user.profile.id))
                return ResponseBuilder.get_response(message=USER_CREATED, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            transaction.savepoint_rollback(sid)
            logger.error('User Creation Failed: {}'.format(e.args[0]))
            if(UNIQUE_CONSTRAINT in e.args[0].lower()):
                return ResponseBuilder.get_response(message=USER_NAME_EXISTS, status=status.HTTP_409_CONFLICT)
            return ResponseBuilder.get_response(message=e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            transaction.savepoint_rollback(sid)
            logger.error('Transactional Error: User Creation Failed: {}'.format(e.args[0]))
            return ResponseBuilder.get_response(message=MISSING_FIELD, status=status.HTTP_406_NOT_ACCEPTABLE)

class CreateVenueView(APIView):
    def post(self, request, *args, **kwargs):
        pass

class DetailVenueView(APIView):
    pass

class OccupationView(APIView):
    pass