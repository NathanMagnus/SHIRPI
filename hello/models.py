from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

#categories for restaurants
class HICategory(models.Model):
	category = models.CharField(max_length=20, primary_key=True)
	min_value = models.FloatField()
	max_value = models.FloatField()
	def __unicode__(self):
		return "%s: %s - %s" % (self.category, self.min_value, self.max_value)
class Location(models.Model):
	countryChoices = (
		(u'CA', u'Canada'),
		(u'US', u'United States'),
	)
	cityChoices = (
		(u'Regina', u'Regina'),
		(u'Saskatoon', u'Saskatoon'),
	)
	regionChoices = (
		(u'Regina/QuAppelle', u'Regina/Qu\'Appelle'),
	)
	city = models.CharField(max_length=50, choices=cityChoices)
	region = models.CharField(max_length=50, choices=regionChoices, primary_key=True)
	province = models.CharField(max_length=2, choices=((u'SK',u'Saskatchewan'),))
	country = models.CharField(max_length=3, choices=countryChoices)
	def __unicode__(self):
		return "%s - %s, %s, %s"%(self.region, self.city, self.province, self.country)


class RegistrationForm(forms.Form):
	query = Location.objects.all()
	username = forms.CharField(max_length=30, label="Username:")
	password = forms.CharField(max_length=100, label="Password:", widget=forms.PasswordInput())
	password_again = forms.CharField(max_length=100, label="Password (again):", widget=forms.PasswordInput())
	first_name = forms.CharField(max_length=30, label="First Name")
	last_name = forms.CharField(max_length=30, label="Last Name")
	email = forms.EmailField(min_length=5, max_length=50)
	street_address = forms.CharField(max_length=75)
	location = forms.ModelChoiceField(queryset=query, empty_label=None)

class Restaurant(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	location = models.ForeignKey(Location)	
	visible = models.BooleanField()
	street_address = models.CharField(max_length=50)
	health_inspection_status = models.IntegerField(default=0)
	combined = models.FloatField(default=0)
	cleanliness = models.FloatField(default=0)
	food_quality = models.FloatField(default=0)
	atmosphere = models.FloatField(default=0)
	wait_time = models.FloatField(default=0)
	comment_count = models.IntegerField(default=0)
	def __unicode__(self):
		return self.name

class RestaurantAdmin(admin.ModelAdmin):
	fields = ['name', 'location', 'street_address', 'visible']
	list_display = ('name', 'location', 'street_address', 'visible')

class CommentForm(forms.Form):
	comment = forms.CharField(widget=forms.Textarea(), required=False)
	food_quality = forms.FloatField(label="Food Quality", required=False)
	cleanliness = forms.FloatField(required=False)
	#service = forms.FloatField(label="Quality of Service:", required=False)
	atmosphere = forms.FloatField(required=False)
	wait_time = forms.FloatField(label="Wait Time", required=False)
	
class Comment(models.Model):
	comment = models.TextField()
	author = models.ForeignKey(User)
	restaurant = models.ForeignKey(Restaurant)
	combined = models.FloatField()
	cleanliness = models.FloatField()
	food_quality = models.FloatField()
	atmosphere = models.FloatField()
	wait_time = models.FloatField()
	id = models.IntegerField(primary_key = True, unique=True)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'comment', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')	
	search_fields = ['comment', 'restaurant']

class HealthReport(models.Model):
	date = models.DateTimeField()
	health_inspection_score = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant)

class UserProfile(models.Model):
	street_address = models.CharField(max_length=75)
	location = models.ForeignKey(Location)
	user = models.ForeignKey(User, unique=True)
	def __unicode__(self):
		return "%s" % (self.user.username)

class Favourite(models.Model):
	user = models.ForeignKey(User)
	restaurant = models.ForeignKey(Restaurant)
	position = models.IntegerField()
	
	
