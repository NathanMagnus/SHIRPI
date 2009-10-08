from django.contrib import admin
from hello.models import *

class LocationAdmin(admin.ModelAdmin):
        list_display = ('region', 'city', 'province', 'country')


class RestaurantAdmin(admin.ModelAdmin):
        fields = ['name', 'location', 'street_address', 'health_inspection_status', 'visible']
        list_display = ('name', 'location', 'street_address', 'visible')

class ReviewAdmin(admin.ModelAdmin):
        list_display = ('restaurant', 'review', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')
        search_fields = ['review']

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile)
admin.site.register(HealthReport)
#admin.site.register(HICategory)
