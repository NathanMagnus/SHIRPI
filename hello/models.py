from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms

#categories for restaurants
class HICategory(forms.Form):
	category = forms.CharField(max_length=20)
	min_value = forms.DecimalField()
	max_value = forms.DecimalField()

#login form
class LoginForm(forms.Form):
	username = forms.CharField(max_length=30, label="Username:")
	password = forms.CharField(max_length=100, label="Password:", widget=forms.PasswordInput())

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
	region = models.CharField(max_length=50, choices=regionChoices)
	province = models.CharField(max_length=2, choices=((u'SK',u'Saskatchewan'),))
	country = models.CharField(max_length=3, choices=countryChoices)
	def __unicode__(self):
		return "%s - %s, %s, %s"%(self.region, self.city, self.province, self.country)
class RegistrationForm(forms.Form):
	query = Location.objects.all()
	username = forms.CharField(max_length=30, label="Username:")
	password = forms.CharField(max_length=100, label="Password:", widget=forms.PasswordInput())
	passwordAgain = forms.CharField(max_length=100, label="Password (again):", widget=forms.PasswordInput())
	firstName = forms.CharField(max_length=30)
	lastName = forms.CharField(max_length=30)
	email = forms.EmailField(min_length=5, max_length=50)
	street_address = forms.CharField(max_length=75)
	location = forms.ModelChoiceField(queryset=query, empty_label=None)

class ReviewForm(forms.Form):
	review = forms.TextInput()
	combined = forms.IntegerField()
	cleanliness = models.ChoiceField(choices=['5','4','3','2','1')
	food_quality = models.ChoiceField(choices=['5','4','3','2','1')
	atmostphere = models.ChoiceField(choices=['5','4','3','2','1')
	wait_time = models.DecimalField()
	

class Restaurant(models.Model):
	name = models.CharField(max_length=100, primary_key=True)
	location = models.ForeignKey(Location)	
	visible = models.BooleanField()
	street_address = models.CharField(max_length=50)
	health_inspection_status = models.IntegerField()
	def __unicode__(self):
		return self.name

class Review(models.Model):
	review = models.TextField()
	restaurant = models.ForeignKey(Restaurant)
	combined = models.DecimalField()
	cleanliness = models.DecimalField()
	food_quality = models.DecimalField()
	atmosphere = models.DecimalField()
	wait_time = models.DecimalField()

class RestaurantAdmin(admin.ModelAdmin):
	fields = ['name', 'location', 'street_address', 'visible']
	list_display = ('name', 'location', 'street_address', 'visible')

class ReviewAdmin(admin.ModelAdmin):
	list_display = ('restaurant', 'review', 'combined', 'cleanliness', 'food_quality', 'atmosphere', 'wait_time')	
	search_fields = ['review']

class HealthReport(models.Model):
	health_inspection_score = models.IntegerField()
	restaurant = models.ForeignKey(Restaurant)

class UserProfile(models.Model):
	street_address = models.CharField(max_length=75)
	location = models.ForeignKey(Location)
	user = models.ForeignKey(User, unique=True)
	def __unicode__(self):
		return "%s" % (self.user.username)
