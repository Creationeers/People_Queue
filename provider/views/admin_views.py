from datetime import timedelta
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import exceptions, permissions, generics
from rest_framework.views import APIView, status
from rest_framework.response import Response
from decouple import config
from ..util.messages import USER_CREATED, USER_NAME_EXISTS, MISSING_FIELD, VENUE_CREATED
from ..util.builders import ResponseBuilder
from ..models import Profile, Venue
from ..serializers import VenueSerializer

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

class CreateVenueView(generics.CreateAPIView):
    serializer_class = VenueSerializer
    def post(self, request, *args, **kwargs):
        _venueSerializer = VenueSerializer(data=request.data)
        if _venueSerializer.is_valid():
            sid = transaction.savepoint()
            _venueSerializer.save()
            return ResponseBuilder.get_response(message=VENUE_CREATED, status=status.HTTP_201_CREATED)
        return ResponseBuilder.get_response(message='Failed', status=status.HTTP_400_BAD_REQUEST)

class DetailVenueView(APIView):
    def get(self, request, *args, **kwargs):
        data = VenueSerializer(Venue.objects.get(id=kwargs['id'])).data
        return ResponseBuilder.get_response_with_json(data, status.HTTP_200_OK)

class OccupationView(APIView):
    pass
