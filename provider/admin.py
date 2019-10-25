from django.contrib import admin
from .models import Profile, Venue, Bonus, Reservation
# Register your models here.

admin.site.register(Profile)
admin.site.register(Venue)
admin.site.register(Bonus)
admin.site.register(Reservation)
