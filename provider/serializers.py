from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth.models import User
from .models import Venue, Address, Profile


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializerDataProtected(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)


class ProfileSerializer(serializers.ModelSerializer):
    #user = UserSerializerDataProtected()

    class Meta:
        model = Profile
        fields = '__all__'


class VenueSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    owner = ProfileSerializer()

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address_instance = Address.objects.create(
            zip_code=address_data['zip_code'], city=address_data['city'], street=address_data['street'], house_number=address_data['house_number'])
        owner = self.context.get('owner')
        validated_data.update({'address': address_instance})
        validated_data.update({'owner': owner})
        return Venue.objects.create(**validated_data)

    class Meta:
        model = Venue
        fields = '__all__'
