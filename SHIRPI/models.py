from django.db import models
from django.contrib.auth.models import User

from project.SHIRPI.settings import *

# choices for the ratings (0 - 5)
choices = (('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5))

'''
Class		: Location
Description	: Databse model for a location (city, province, country, rha)
'''
class Location(models.Model):
	city = models.CharField(max_length="50")
	province = models.CharField(max_length="50")
	country = models.CharField(max_length="50")
	rha = models.CharField(max_length="200")
	def __unicode__(self):
		return "%s, %s" % (self.city, self.rha)		

'''
Class		: Restaurant
Description	: Database model that contains all information about the restaurants ratings
		: location information and if it is visible
'''
class Restaurant(models.Model):
	location = models.ForeignKey(Location)
	address = models.CharField(max_length="75")
	address_clean = models.CharField(max_length="75")
	postal_code = models.CharField(max_length="8")
	name = models.CharField(max_length="50")
	name_clean = models.CharField(max_length="50")
	
	health_report_status = models.IntegerField(default=0)

	# ratings and the number of ratings that have been made for a specific metric
	combined = models.FloatField(default = "0", choices=choices)
	combined_count = models.IntegerField(default=0)
	cleanliness = models.FloatField(default = "0", choices=choices)
	cleanliness_count = models.IntegerField(default=0)
	food_quality = models.FloatField(default = "0", choices=choices)
	food_quality_count = models.IntegerField(default=0)
	atmosphere = models.FloatField(default = "0", choices=choices)
	atmosphere_count = models.IntegerField(default=0)
	overall = models.FloatField(default = "0", choices=choices)
	overall_count = models.IntegerField(default=0)
	
	visible = models.BooleanField(default=True)

	# how this should be represented when outputted as a string
	def __unicode__(self):
		return "%s - %s" % (self.name, self.address)
		
	def get_hi_class(self):
		# Returns Restaurant severity as string
		if self.health_report_status >= CRITICAL_VAL:
			return 'critical'
		elif self.health_report_status >= MODERATE_VAL:
			return 'moderate'
		else:
			return 'low'
		
	def get_scores(self):
		# Returns Restaurant scores as labelled dictionary
		
		# Catch division by zero
		try: health_report_status = self.health_report_status
		except: health_report_status = 0
		
		try: combined = self.combined / self.combined_count
		except: combined = 0
	
		try: food_quality = self.food_quality / self.food_quality_count
		except: food_quality = 0
		
		try: cleanliness = self.cleanliness / self.cleanliness_count
		except: cleanliness = 0
		
		try: atmosphere = self.atmosphere / self.atmosphere_count
		except: atmosphere = 0
		
		try: overall = self.overall / self.overall_count
		except: overall = 0
		
		
		return {'health_report_status': health_report_status,
			'combined': combined,
			'food_quality': food_quality,
			'cleanliness': cleanliness,
			'atmosphere': atmosphere,
			'overall': overall}


'''
Class		: Comment
Description	: Database model for a user comment
'''
class Comment(models.Model):
	id = models.IntegerField(primary_key = True)
	restaurant = models.ForeignKey(Restaurant)

	author = models.ForeignKey(User)

	comment = models.TextField(default = "", blank=True)
	combined = models.FloatField(default = "0", choices=choices)
	cleanliness = models.FloatField(default = "0", choices=choices)
	food_quality = models.FloatField(default = "0", choices=choices)
	atmosphere = models.FloatField(default = "0", choices=choices)
	overall = models.FloatField(default = "0", choices=choices)

	created = models.DateTimeField()
        last_modified = models.DateTimeField()

	ip = models.IPAddressField()

'''
Class		: Favourite
Description	: Database model for a users favourites
'''
class Favourite(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	user = models.ForeignKey(User)
	rank = models.IntegerField()
	def __unicode__(self):
		return "%s. %s" % (self.rank, self.restaurant)

'''
Class		: HealthInspectionItem
Description	: Database model for an item that could appear on a health inspection reprot
'''
class HealthInspectionItem(models.Model):
	id = models.IntegerField(primary_key=True, unique=True)
	number = models.CharField(max_length="10")
	short_description = models.CharField(max_length="200")
	description = models.TextField()
	severity = models.IntegerField()
	def __unicode__(self):
		return "%s" % (self.number)

'''
Class		: HealthReport
Description	: Database model for a Health report
'''
class HealthReport(models.Model):
	date = models.DateField()
	health_inspection_score = models.IntegerField(default=0)
	restaurant = models.ForeignKey(Restaurant)
	priority = models.CharField(max_length="30")
	type = models.CharField(max_length="30")
	items = models.ManyToManyField(HealthInspectionItem, null=True)
	def __unicode__(self):
		return "%s %s %s" % (self.restaurant.name, self.health_inspection_score, self.date)
