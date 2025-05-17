from django.contrib import admin
from .models import Artist, Track, RoyaltyRecord, Payment

admin.site.register(Artist)
admin.site.register(Track)
admin.site.register(RoyaltyRecord)
admin.site.register(Payment)
