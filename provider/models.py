from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from .util.validators import NOT_NEGATIVE_VALIDATOR

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


class Venue(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description_shot = models.CharField(max_length=511, null=False, blank=False)
    description_long = models.CharField(max_length=4095, null=False, blank=False)
    current_occupation = models.IntegerField(default=0)
    max_occupation = models.IntegerField(default=0, null=False, blank=False)
    homepage = models.CharField(max_length=1023)
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)


class Bonus(models.Model):
    amount = models.FloatField(validators=NOT_NEGATIVE_VALIDATOR)
    note = models.CharField(max_length=2047)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Bonuses'

class Reservation(models.Model):
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)
    venue = models.ForeignKey(to=Venue, on_delete=models.CASCADE, null=False, blank=False)
    owner = models.OneToOneField(to=Profile, on_delete=models.CASCADE)
    no_of_people = models.IntegerField(default=1, null=False, blank=False)
    bonus = models.ForeignKey(to=Bonus, on_delete=models.PROTECT)
