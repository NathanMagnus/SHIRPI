# Create your views here.
import urllib
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm 
from project.SHIRPI.settings import *

from datetime import datetime
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

#main page
def index(request):
	#get critical, moderate and good reports
	Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by('-health_report_status').all()[:10]
	Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by('-health_report_status').all()[:10]
	Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by('-health_report_status').all()[:10]
	#render the index page
	return render_to_response("SHIRPI/index.html", {'user':request.user, 'Critical':Critical, 'Moderate':Moderate,'Good':Good})

#browsing restaurants
def browse(request, restaurant_name, restaurant_address):
	restaurant_name = restaurant_name.urllib.unquote_plus()
	restaurant_address = restaurant_address.urllib.unquote_plus()
	#if they inputted "All" for the restaurant name and address
	if restaurant_name.lower()=="all" and restaurant_address.lower()=="all":
		#find all critical, moderate and good restauratns
		Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by("-health_report_status")
		Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by("-health_report_status")
		Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by("-health_report_status")
		#render the response
		return render_to_response("SHIRPI/browse.html", {'Critical':Critical, 'Moderate':Moderate, 'Good': Good, 'user':request.user})
	#if they want all restaurants with a certain address
	elif restaurant_name.lower()=="all":
		try:
			chain = Restaurant.objects.filter(address__contains=restaurant_address)
		except Restaurant.DoesNotExist:
			error = "Restaurant with that address does not exist"
	#if they want a restaurant based on name
	elif restaurant_address.lower()=="all":
		try:
			chain = Restaurant.objects.filter(name__contains=restaurant_name)
		except Restaurant.DoesNotExist:
			error = "Restaurant name containing that sequence does not exist"
	else:
		try:
			chain = Restaurant.objects.filter(name__contains=restaurant_name, address__contains=restaurant_address)
		except Restaurant.DoesNotExist:
			error = "Restauarnt with that name and address does not exist"
	if len(chain)==1:
		restaurant = chain[0]
		#get the reports
		reps = HealthReport.objects.filter(restaurant=restaurant)
		#get the comments
		comments = Comment.objects.filter(restaurant=restaurant)[0:5]
		#render the page
		return render_to_response("SHIRPI/browse.html", {'restaurant': restaurant, 'reps':reps, 'user':request.user, 'comments': comments})
	elif len(chain)==0:
		return render_to_response("SHIRPI/browse.html", {'error':error}, RequestContext(request))
	else:
		return render_to_response("SHIRPI/browse.html", {'chain': chain}, RequestContext(request))

def view_profile(request, user_name):
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/view_profile.html', {'error': "No user with username '" + user_name +"'"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	comments = Comment.objects.filter(author=user_to_view)
	return render_to_response('SHIRPI/view_profile.html', {'user_to_view': user_to_view, 'favourites': favourites, 'comments': comments}, RequestContext(request))	

def edit_profile(request):
	if request.user.is_authenticated():
		form = ProfileForm()
		return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))
	return render_to_response('SHIRPI/edit_profile.html', {'error':"You are not logged in"}, RequestContext(request)) 
