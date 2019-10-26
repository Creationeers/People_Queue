import logging
from datetime import timedelta
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from rest_framework import exceptions, permissions, generics
from rest_framework.views import APIView, status
from rest_framework.response import Response
from decouple import config
from ..util.messages import USER_CREATED, USER_NAME_EXISTS, MISSING_FIELD, VENUE_CREATED, DOES_NOT_EXIST, FORBIDDEN, TIMESTAMP_CREATED
from ..util.builders import ResponseBuilder
from ..util.constants import UNIQUE_CONSTRAINT
from ..models import Profile, Venue, Device
from ..serializers import VenueSerializer, DeviceSerializer

ResponseBuilder = ResponseBuilder()
logger = logging.getLogger('testlogger')


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
                profile.ad_consent_available = request.data['is_commercial_user'].lower(
                ).capitalize()
                profile.is_commercial_user = request.data['ad_consent_available'].lower(
                ).capitalize()
                profile.save()
                logger.info('User {} with Profile ID {} Created Successfully'.format(
                    user.username, user.profile.id))
                return ResponseBuilder.get_response(message=USER_CREATED, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            transaction.savepoint_rollback(sid)
            logger.error('User Creation Failed: {}'.format(e.args[0]))
            if(UNIQUE_CONSTRAINT in e.args[0].lower()):
                return ResponseBuilder.get_response(message=USER_NAME_EXISTS, status=status.HTTP_409_CONFLICT)
            return ResponseBuilder.get_response(message=e.args, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            transaction.savepoint_rollback(sid)
            logger.error(
                'Transactional Error: User Creation Failed: {}'.format(e.args[0]))
            return ResponseBuilder.get_response(message=MISSING_FIELD, status=status.HTTP_406_NOT_ACCEPTABLE)


class VenueView(generics.ListCreateAPIView):
    serializer_class = VenueSerializer
    queryset = Venue.objects.all()

    def post(self, request, *args, **kwargs):
        _venueSerializer = VenueSerializer(data=request.data, context={
                                           'owner': Profile.objects.get(user=request.user)}, partial=True)
        if _venueSerializer.is_valid():
            sid = transaction.savepoint()
            venue = _venueSerializer.save()
            logger.info('Venue \'{}\' created successfully'.format(venue))
            return ResponseBuilder.get_response(message=VENUE_CREATED, status=status.HTTP_201_CREATED)
        else:
            transaction.savepoint_rollback(sid)
            logger.error('{}'.format(_venueSerializer.errors))
            return ResponseBuilder.get_response(message=_venueSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VenueViewForAccount(generics.ListAPIView):
    serializer_class = VenueSerializer

    def get_queryset(self):
        try:
            return Venue.objects.filter(owner = Profile.objects.get(user = self.request.user))
        except ObjectDoesNotExist:
            return ResponseBuilder.get_response(message=DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)


class DeviceView(generics.ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        try:
            return Device.objects.filter(venue__owner = Profile.objects.get(user = self.request.user))
        except ObjectDoesNotExist:
            return ResponseBuilder.get_response(message=DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)


    def post(self, request, *args, **kwargs):
        try:
            sid = transaction.savepoint()
            venue = Venue.objects.get(id=request.data['venue'])
            profile = Profile.objects.get(user=request.user)
            if venue.owner == profile:
                _deviceSerializer = DeviceSerializer(data=request.data, context={
                                                     'venue': venue}, partial=True)
                if _deviceSerializer.is_valid():
                    device = _deviceSerializer.save()
                    logger.info(
                        'Device \'{}\ created successfully'.format(device.name))
                    return ResponseBuilder.get_response(message={'device_id': device.id}, status=status.HTTP_201_CREATED)
                else:
                    transaction.savepoint_rollback(sid)
                    logger.error('{}'.format(_deviceSerializer.errors))
                    return ResponseBuilder.get_response(message=_deviceSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                logger.info(
                    'Unauthorized request from {}'.format(request.user))
                return ResponseBuilder.get_response(message=FORBIDDEN, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist as e:
            transaction.savepoint_rollback(sid)
            logger.error('{}'.format(e))
            return ResponseBuilder.get_response(message=DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)


class UpdateOccupationView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            device = Device.objects.get(id=request.data["id"])
            count = request.data["count"]
            return ResponseBuilder.get_response(message=TIMESTAMP_CREATED, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist:
            return ResponseBuilder.get_response(message=DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)


class DetailVenueView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            data = VenueSerializer(Venue.objects.get(id=kwargs['id'])).data
            return ResponseBuilder.get_response_with_json(data, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return ResponseBuilder.get_response(message=DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)


class OccupationView(APIView):
    pass
