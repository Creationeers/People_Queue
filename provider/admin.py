from django.contrib import admin
from .models import Profile, Venue, Bonus, Reservation, Occupation_Past_Data
# Register your models here.

admin.site.register(Profile)
admin.site.register(Venue)
admin.site.register(Bonus)
admin.site.register(Reservation)
admin.site.register(Occupation_Past_Data)