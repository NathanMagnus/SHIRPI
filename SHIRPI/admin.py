from django.contrib import admin
from SHIRPI.models import *

class LocationAdmin(admin.ModelAdmin):
	list_display = ('city', 'province', 'country', 'rha', 'municipality')
	search_fields = ['city', 'province', 'rha']
	fields = ['city', 'province', 'country', 'rha']

class RestaurantAdmin(admin.ModelAdmin):
	list_display = ('name', 'address', 'location', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time', 'chain', 'health_report_status', 'visible')
	search_fields = ['name', 'address', 'location__rha']
	fields = ['name', 'address', 'location', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time', 'chain', 'health_report_status', 'visible']

class CommentAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'author', 'comment', 'combined', 'cleanliness', 'food_quality', 'wait_time')
	search_fields = ['author', 'restaurant', 'comment']
	fields = ['author', 'restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'wait_time']

class FavouriteAdmin(admin.ModelAdmin):
	list_display=('user', 'restaurant', 'rank')
	search_fields = ['user', 'restaurant']
	fields = ['user', 'restaurant', 'rank']

class HealthInspectionItemAdmin(admin.ModelAdmin):
	list_display = ('number', 'short_description', 'severity', 'description')
	search_fields = ['description', 'short_description']
	fields = ['number', 'short_description', 'description', 'severity']

class HealthReportAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'date', 'type', 'priority', 'health_inspection_score')
	search_fields = ['restaurant', 'date']
	fields = ['restaurant', 'date', 'type', 'priority', 'health_inspection_score']

class ChainAdmin(admin.ModelAdmin):
	list_display = ('regex',)
	search_fields = ['regex']
	fields = ['regex']

admin.site.register(Location, LocationAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(HealthInspectionItem, HealthInspectionItemAdmin)
admin.site.register(HealthReport, HealthReportAdmin)
admin.site.register(Chain, ChainAdmin)
