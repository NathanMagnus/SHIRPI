from django.db import models
from django.contrib.auth.models import User

choices = (('0', 0), ('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5))

class Location(models.Model):
	city = models.CharField(max_length="50")
	province = models.CharField(max_length="50")
	country = models.CharField(max_length="50")
	rha = models.CharField(max_length="200")
	municipality = models.CharField(max_length="100")
	def __unicode__(self):
		return "%s, %s" % (self.city, self.rha)		

class Chain(models.Model):
	regex = models.CharField(max_length="50")
	def __unicode__(self):
		return "%s" % (self.regex)

class Restaurant(models.Model):
	location = models.ForeignKey(Location)
	address = models.CharField(max_length="75")
	address_simple = models.CharField(max_length="75")
	name = models.CharField(max_length="50")
	
	health_report_status = models.IntegerField(default=0)
	combined = models.FloatField(default = "0", choices=choices)
	combined_count = models.IntegerField(default=0)
	cleanliness = models.FloatField(default = "0", choices=choices)
	cleanliness_count = models.IntegerField(default=0)
	food_quality = models.FloatField(default = "0", choices=choices)
	food_quality_count = models.IntegerField(default=0)
	atmosphere = models.FloatField(default = "0", choices=choices)
	atmosphere_count = models.IntegerField(default=0)
	wait_time = models.FloatField(default = "0", choices=choices)
	wait_time_count = models.IntegerField(default=0)
	
	visible = models.BooleanField(default=True)
	chain = models.ForeignKey(Chain, null=True)
	
	def __unicode__(self):
		return "%s - %s" % (self.name, self.address)

class Comment(models.Model):
	id = models.IntegerField(primary_key = True)
	restaurant = models.ForeignKey(Restaurant)
	author = models.ForeignKey(User)
	comment = models.TextField(default = "", blank=True)
	combined = models.FloatField(default = "0", choices=choices)
	cleanliness = models.FloatField(default = "0", choices=choices)
	food_quality = models.FloatField(default = "0", choices=choices)
	atmosphere = models.FloatField(default = "0", choices=choices)
	wait_time = models.FloatField(default = "0", choices=choices)
        created = models.DateTimeField()
        last_modified = models.DateTimeField()
	ip = models.IPAddressField()

class Favourite(models.Model):
	restaurant = models.ForeignKey(Restaurant)
	user = models.ForeignKey(User)
	rank = models.IntegerField()
	def __unicode__(self):
		return "%s. %s" % (self.rank, self.restaurant)

class HealthInspectionItem(models.Model):
	id = models.IntegerField(primary_key=True, unique=True)
	number = models.CharField(max_length="10")
	short_description = models.CharField(max_length="200")
	description = models.TextField()
	severity = models.IntegerField()
	def __unicode__(self):
		return "%s" % (self.number)

class HealthReport(models.Model):
	date = models.DateField()
	health_inspection_score = models.IntegerField(default=0)
	restaurant = models.ForeignKey(Restaurant)
	priority = models.CharField(max_length="30")
	type = models.CharField(max_length="30")
	items = models.ManyToManyField(HealthInspectionItem, null=True)
	def __unicode__(self):
		return "%s %s %s" % (self.restaurant.name, self.health_inspection_score, self.date)

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	show_first_name = models.BooleanField(default=False)
	show_last_name = models.BooleanField(default=False)
	show_email = models.BooleanField(default=False)
	city = models.CharField(max_length="100", null=True)
	province = models.CharField(max_length="100", null=True)
	country = models.CharField(max_length="100", null=True)
	address = models.CharField(max_length="100", null=True)
