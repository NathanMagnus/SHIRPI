# Create your views here.
import urllib
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm, ProfileForm
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
	Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by('-health_report_status', '-combined').all()[:10]
	#render the index page
	return render_to_response("SHIRPI/index.html", {'Critical':Critical, 'Moderate':Moderate,'Good':Good}, RequestContext(request))

#browsing restaurants
def browse(request, restaurant_name = None, restaurant_address = None, api_flag = None):
	# TODO: Seriously consider exclusively using GETs for input instead of view parameters
	
	# Prepare strings for database query
	if restaurant_name == None:
		restaurant_name = ""
	if restaurant_address == None:
		restaurant_address = ""
		
	restaurant_name = urllib.unquote_plus(restaurant_name).lower()
	restaurant_address = urllib.unquote_plus(restaurant_address).lower()
	
	if restaurant_name == "all":
		restaurant_name = ""
	if restaurant_address == "all":
		restaurant_address = ""
	
	range_low = request.GET.get('lrange')	# escape this?	
	range_high = request.GET.get('hrange')	
	# here so that user can search for all good restaurants on albert street
	# or all mcdonalds that are good, etc
	if restaurant_name == "good" or restaurant_address == "good":
		range_low = GOOD_VAL	
		range_high = GOOD_VAL+1
	elif restaurant_name == "critical" or restaurant_address == "critical":
		range_low = CRITICAL_VAL
		range_hight = 99999
	elif restaurant_name == "moderate" or restaurant_address == "moderate":
		range_low = MODERATE_VAL
		range_high = CRITICAL_VAL
	if restaurant_name == "good" or restaurant_name == "moderate" or restaurant_name=="critical":
		restaurant_name = ""
	if restaurant_address == "good" or restaurant_address == "moderate" or restaurant_address=="critical":
		restaurant_address = ""
	
	# Query Database
	# ACTUAL RANGE EXCLUSION SHOULD BE DONE AFTER THIS
	try:
		results = Restaurant.objects.filter(name__icontains=restaurant_name, address__icontains=restaurant_address)
		if range_low != None and range_high!=None:
			results = results.filter(health_report_status__gte=range_low, health_report_status__lt=range_high)
	except Restaurant.DoesNotExist:
		error = "No results."
	
	# Standard browse
	if api_flag == None:
		if len(results) == 1:
			restaurant = results[0]
			#get the reports
			reps = HealthReport.objects.filter(restaurant=restaurant)
			#get the comments
			comments = Comment.objects.filter(restaurant=restaurant)[0:5]
			#render the page
			return render_to_response("SHIRPI/view.html", {'restaurant': restaurant, 'reps':reps, 'comments': comments}, RequestContext(request))
		elif len(results) == 0:
			return render_to_response("SHIRPI/browse.html", {'error':"No matches found"}, RequestContext(request))
		else:
			return render_to_response("SHIRPI/browse.html", {'restaurants': results}, RequestContext(request))
	
	else:
		display_type = request.GET.get('display') # escaping required?
		context = { 'results': results, 'reports': HealthReport.objects.all(), 'display_type': display_type }
		return render_to_response("SHIRPI/api.xml", context, RequestContext(request),  mimetype='application/xml')

def view_restaurant(request, restaurant_name, restaurant_address):
	try:
		restaurant = Restaurant.objects.get(name__iexact=urllib.unquote_plus(restaurant_name), address__iexact=urllib.unquote_plus(restaurant_address))
		reports = HealthReport.objects.filter(restaurant=restaurant)
		comments = Comment.objects.filter(restaurant=restaurant)
		return render_to_response("SHIRPI/view_restaurant.html", {'restaurant': restaurant, 'reports': reports, 'comments': comments}, RequestContext(request))
	except Restaurant.DoesNotExist:
		return HttpResponseRedirect("/cs215/SHIRPI/browse.html")

def view_profile(request, user_name):
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/view_profile.html', {'error': "No user with username '" + user_name +"'"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	comments = Comment.objects.filter(author=user_to_view)
	return render_to_response('SHIRPI/view_profile.html', {'user_to_view': user_to_view, 'favourites': favourites, 'comments': comments}, RequestContext(request))	

def edit_profile(request):
	user = request.user
#	if user.is_authenticated():
	if request.method == "POST":
		form = ProfileForm(request.POST)
		if form.is_valid() and form.cleaned_data['new_password'] == form.cleaned_data['password_again'] and user.check_password(form.cleaned_data['old_password']):
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['new_password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			return render_to_response('SHIRPI/edit_profile.html', {'form': form, 'message': "Changes completed"}, RequestContext(request))
	else:
		form = ProfileForm(initial={'email': request.user.email})
		return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))
	return render_to_response('SHIRPI/edit_profile.html', {'error':"You are not logged in"}, RequestContext(request)) 
