import datetime
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.timezone import now
from .util.validators import NOT_NEGATIVE_VALIDATOR, ZIP_VALIDATOR
from .util.enums import WEEKDAYS

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_commercial_user = models.BooleanField(default=False)
    ad_consent_available = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for {}'.format(self.user.username)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Address(models.Model):
    zip_code = models.IntegerField(blank=False, null=False, validators=ZIP_VALIDATOR)
    city = models.CharField(max_length=127, null=False, blank=False)
    street = models.CharField(max_length=127, null=False, blank=False)
    house_number = models.IntegerField(blank=False, null=False)


class Venue(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description_short = models.CharField(max_length=511, null=False, blank=False)
    description_long = models.CharField(max_length=4095, null=False, blank=False)
    current_occupation = models.IntegerField(default=0)
    max_occupation = models.IntegerField(default=0, null=False, blank=False)
    homepage = models.CharField(max_length=1023)
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    reservations_enabled = models.BooleanField(default=False, null=False, blank=False)
    real_time_queue_enabled = models.BooleanField(default=False, null=False, blank=False)
    address = models.ForeignKey(to=Address, on_delete=models.PROTECT)


class Bonus(models.Model):
    amount = models.FloatField(validators=NOT_NEGATIVE_VALIDATOR)
    note = models.CharField(max_length=2047)
    timestamp = models.DateTimeField(default=now, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Bonuses'


class Reservation(models.Model):
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    venue = models.ForeignKey(to=Venue, on_delete=models.CASCADE, null=False, blank=False)
    owner = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    no_of_people = models.IntegerField(default=1, null=False, blank=False)
    bonus = models.ForeignKey(to=Bonus, on_delete=models.PROTECT)


class Occupation_Past_Data(models.Model):
    timestamp = models.DateTimeField(default=now, editable=False)
    occupation = models.IntegerField()
    reservations = models.IntegerField()
    reservations_total_people = models.IntegerField()
    venue = models.ForeignKey(to=Venue, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Occupation Past Data'
        verbose_name_plural = 'Occupation Past Datas'


class Opening_Hours(models.Model):
    weekday = models.CharField(max_length=10, choices=WEEKDAYS)
    opening_morning = models.DateTimeField(blank=False, null=False)
    closing_morning = models.DateTimeField(blank=True, null=True)
    opening_noon = models.DateTimeField(blank=True, null=True)
    closing_noon = models.DateTimeField(blank=False, null=False)
    note = models.CharField(max_length=2047)
    venue = models.ForeignKey(to=Venue, on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Opening Hours'
        verbose_name_plural = 'Opening Hours'


class Conditional_Promotion(models.Model):
    venue = models.ForeignKey(to=Venue, on_delete=models.CASCADE, null=False, blank=False)
    start_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    day = models.CharField(max_length=10, choices=WEEKDAYS, null=False, blank=False)
    note = models.CharField(max_length=2043)
    trigger_occupation = models.IntegerField(default=0, null=False, blank=False)
