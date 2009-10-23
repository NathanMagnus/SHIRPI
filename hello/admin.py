from django.contrib import admin
from hello.models import *



class LocationAdmin(admin.ModelAdmin):
        list_display = ('region', 'city', 'province', 'country')
	search_fields = ['street_address']

class RestaurantAdmin(admin.ModelAdmin):
        fields = ['name', 'location', 'street_address', 'health_inspection_status', 'visible']
        list_display = ('name', 'location', 'street_address', 'visible')
	search_fields = ['name', 'street_address']

class CommentAdmin(admin.ModelAdmin):
        list_display = ('restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')
        search_fields = ['comment', 'author__username']

class HIItemAdmin(admin.ModelAdmin):
	fields = ['number', 'severity', 'description']
	list_display=('number', 'severity', 'description')

class HealthReportAdmin(admin.ModelAdmin):
	fields = ['restaurant', 'date', 'priority', 'type', 'items', 'health_inspection_score']
	list_display= ('restaurant', 'date', 'priority', 'type', 'health_inspection_score')
	search_fields = ['restaurant__name']

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserProfile)
admin.site.register(HealthReport, HealthReportAdmin)
admin.site.register(HICategory)
admin.site.register(Favourite)
#admin.site.register(HIItemMaster, HIItemMasterAdmin)
admin.site.register(HIItem, HIItemAdmin)
