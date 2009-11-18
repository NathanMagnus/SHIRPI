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
	return render_to_response("SHIRPI/index.html", {'user':request.user, 'Critical':Critical, 'Moderate':Moderate,'Good':Good})

#browsing restaurants
def browse(request, restaurant_name = None, restaurant_address = None, api_flag = None):
	# TODO: Seriously consider exclusively using GETs for input instead of view parameters
	
	# TODO: Remove this at leisure. This is to be depreciated by better sorting methods. Only useful on main page.
	#if they inputted "All" for the restaurant name and address
	#if restaurant_name.lower()=="all" and restaurant_address.lower()=="all":
	#	#find all critical, moderate and good restauratns
	#	Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by("-health_report_status", "-combined")
	#	Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by("-health_report_status", "-combined")
	#	Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by("-health_report_status", "-combined")
	#	#render the response
	#	return render_to_response("SHIRPI/browse.html", {'Critical':Critical, 'Moderate':Moderate, 'Good': Good, 'user':request.user})
	
	
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
	
	# Query Database
	try:
		results = Restaurant.objects.filter(name__icontains=restaurant_name, address__icontains=restaurant_address)
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
			return render_to_response("SHIRPI/browse.html", {'restaurant': restaurant, 'reps':reps, 'user':request.user, 'comments': comments})
		elif len(results) == 0:
			return render_to_response("SHIRPI/browse.html", {'error':"No matches found"}, RequestContext(request))
		else:
			return render_to_response("SHIRPI/browse.html", {'chain': results}, RequestContext(request))
	
	else:
		display_type = request.GET.get('display') # escaping required?
		context = { 'results': results, 'reports': HealthReport.objects.all(), 'display_type': display_type }
		return render_to_response("SHIRPI/api.xml", context, RequestContext(request),  mimetype='application/xml')

		
	

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
	if user.is_authenticated():
		if request.method == "POST":
			form = ProfileForm(request.POST)
			if form.is_valid() and form.cleaned_data['new_password'] == form.cleaned_data['password_again'] and user.check_password(form.cleaned_data['new_password']:
				user.email = form.cleaned_data['email']
				user.set_password(form.cleaned_data['new_password']
		else:
			form = ProfileForm()
			form.email = request.user.email
			form.address = request.user.address
			return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))
	return render_to_response('SHIRPI/edit_profile.html', {'error':"You are not logged in"}, RequestContext(request)) 
