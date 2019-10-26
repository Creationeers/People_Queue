from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Venue

class VenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venue
        fields = '__all__'

