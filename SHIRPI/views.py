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
	
	range_low = request.GET.get('lrange')
	range_high = request.GET.get('hrange')	
	# here so that user can search for all good restaurants on albert street
	# or all mcdonalds that are good, etc
	
	# I do not understand why you are doing all of this. We should be using GET methods for
	# handeling these parameters. What if a person wanted to search for 'good' in the name?
	# I intended for ?lrange and ?hrange to be used in this manner and set them just above.
	# I also thought I would be possible to have an range spanning multipe HI groups
	# For example, a result set including moderate and criticals. or goods and moderates
	#	(good and critical exclusively seems strange and not easy to do at all)
	if restaurant_name == "good" or restaurant_address == "good":
		range_low = GOOD_VAL	
		range_high = GOOD_VAL+1
	elif restaurant_name == "critical" or restaurant_address == "critical":
		range_low = CRITICAL_VAL
		range_high = 99999
	elif restaurant_name == "moderate" or restaurant_address == "moderate":
		range_low = MODERATE_VAL
		range_high = CRITICAL_VAL
	if restaurant_name == "good" or restaurant_name == "moderate" or restaurant_name=="critical":
		restaurant_name = ""
	if restaurant_address == "good" or restaurant_address == "moderate" or restaurant_address=="critical":
		restaurant_address = ""
	
	# Consider modifying the above to something similar to:
	'''
		lower_limit = request.GET.get('lrange')
		upper_limit = request.GET.get('hrange')	# perhaps use better GET names
		
		if upper_limit == "critical":
			range_high = 9999
			
			if lower_limit == "moderate":
				range_low = MODERATE_VAL
			elif lower_limit == "good":
				range_low = GOOD_VAL
			else:
				range_low = CRITICAL_VAL
		
		elif upper_limit == "moderate":
			range_high = CRITICAL_VAL
			
			if lower_limit == "good":
				range_low = GOOD_VAL
			else:
				range_low = MODERATE_VAL
		
		elif upper_limit == "good"
			range_high = GOOD_VAL+1
			range_low = GOOD_VAL
			
			
	'''
	
	# Query Database
	# ACTUAL RANGE EXCLUSION SHOULD BE DONE AFTER THIS
	try:
		results = Restaurant.objects.filter(name__icontains=restaurant_name, address__icontains=restaurant_address)
		if range_low != None and range_high != None:
			results = results.filter(health_report_status__gte=range_low, health_report_status__lt=range_high)
	except Restaurant.DoesNotExist:
		error = "No results."
	
	# Browse Page Display
	if api_flag == None:
		if len(results) == 1:
			restaurant = results[0]
			#get the reports
			reps = HealthReport.objects.filter(restaurant=restaurant)
			#get the comments
			comments = Comment.objects.filter(restaurant=restaurant)[0:5]
			#render the page
			return render_to_response("SHIRPI/view_restaurant.html", {'restaurant': restaurant, 'reps':reps, 'comments': comments}, RequestContext(request))
		elif len(results) == 0:
			return render_to_response("SHIRPI/browse.html", {'error':"No matches found"}, RequestContext(request))
		else:
			return render_to_response("SHIRPI/browse.html", {'restaurants': results}, RequestContext(request))
	
	# API Display
	else:
		display_type = request.GET.get('display')
		MySpecialApiData = []
		for location in results:	# disgusting loop solves problems
			if display_type == "full":
				report_results = HealthReport.objects.filter(restaurant=location)
			MySpecialApiData.append({ 'location': location, 'reports': report_results })
		
		context = { 'results': MySpecialApiData, 'display_type':  }
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
