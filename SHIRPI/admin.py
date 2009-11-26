# set up how django admin handles models
from django.contrib import admin
from SHIRPI.models import *

'''
Each of the classes within this file are used to define the django admin interface for a specific model.
'''

# admin page for locations
class LocationAdmin(admin.ModelAdmin):
	list_display = ('city', 'province', 'country', 'rha')
	search_fields = ['city', 'province', 'rha']
	fields = ['city', 'province', 'country', 'rha']

# admin page for restaurants
class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'postal_code', 'address_searchable', 'location', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time','health_report_status', 'visible')
	search_fields = ['name', 'address', 'location__rha', 'postal_code']
	fields = ['name', 'address', 'address_searchable', 'location', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time', 'health_report_status', 'visible', 'postal_code']

# admin page for comments
class CommentAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'author', 'comment', 'combined', 'cleanliness', 'food_quality', 'wait_time')
	search_fields = ['author', 'restaurant', 'comment', 'ip']
	fields = ['author', 'restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'wait_time', 'ip', 'created']

# admin page for favourites
class FavouriteAdmin(admin.ModelAdmin):
	list_display=('user', 'restaurant', 'rank')
	search_fields = ['user', 'restaurant']
	fields = ['user', 'restaurant', 'rank']

# admin page for health inspections items
class HealthInspectionItemAdmin(admin.ModelAdmin):
	list_display = ('number', 'short_description', 'severity', 'description')
	search_fields = ['description', 'short_description']
	fields = ['number', 'short_description', 'description', 'severity']

# admin page for health reports
class HealthReportAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'date', 'type', 'priority', 'health_inspection_score')
	search_fields = ['restaurant', 'date']
	fields = ['restaurant', 'date', 'type', 'priority', 'health_inspection_score']

# register all the admin pages
admin.site.register(Location, LocationAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(HealthInspectionItem, HealthInspectionItemAdmin)
admin.site.register(HealthReport, HealthReportAdmin)
