from django.contrib import admin
from hello.models import *

class LocationAdmin(admin.ModelAdmin):
        list_display = ('region', 'city', 'province', 'country')


class RestaurantAdmin(admin.ModelAdmin):
        fields = ['name', 'location', 'street_address', 'health_inspection_status', 'visible']
        list_display = ('name', 'location', 'street_address', 'visible')

class CommentAdmin(admin.ModelAdmin):
        list_display = ('restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')
        search_fields = ['comment']

class HIItemMasterAdmin(admin.ModelAdmin):
	fields = ['number', 'severity', 'description']
	list_display=('number', 'severity', 'description')

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile)
admin.site.register(HealthReport)
admin.site.register(HICategory)
admin.site.register(Favourite)
admin.site.register(HIItemMaster, HIItemMasterAdmin)
admin.site.register(HIItem)
