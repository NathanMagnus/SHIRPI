import urllib
import re
import string
from cgi import escape

from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm, ProfileForm
from project.SHIRPI.settings import *

from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

'''
Function	: index
Description	: the main page for SHIRPI
Parameter(s)	: request - HttpRequest
Return 		: HttpResponse
'''
def index(request):
	#get critical, moderate and low reports
	Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by('-health_report_status', '-combined').all()[:10]
	Low = Restaurant.objects.filter(health_report_status__lte=LOW_VAL).order_by('-health_report_status', '-combined').all()[:10]

	#render the index page
	return render_to_response("SHIRPI/index.html", {'Critical':Critical, 'Moderate':Moderate,'Low':Low}, RequestContext(request))

'''
Function	: browse
Description	: determine what restaurants are to b edisplayed when browsing/searching/sorting
Parameter(s)	: restaurant_name - the name to be searched for/displayed
		: restaurant_address - the address to be searched for/displayed
		: api_flag - if this is an api call or not
Return 		: HttpResponse
'''
def browse(request, restaurant_name = None, restaurant_address = None, api_flag = None):
	# determine the restaurant_name and restaurant_address
	# any get information will override the parameters passed by the url
	restaurant_name = request.GET.get("restaurant_name", restaurant_name)
	restaurant_address = request.GET.get("restaurant_address", restaurant_address)

	# set upper and lower limit based upon the GET information
	lower_limit = request.GET.get('lower_limit', "0")
	upper_limit = request.GET.get('upper_limit', "100")

	# get order and type information
	order = request.GET.get('sort_by', 'name_clean').lower()
	type = request.GET.get('type', 'asc').lower()
	
	# if descending put the - in front, otherwise nothing
	if type == "desc":
		type = "-"
	else:
		type = ""

	# process the order options
	valid_order = False

	# use the model fields for ordering
	options = Restaurant._meta
	for option in options.fields:
		if order == option.name:
			valid_order=True
			break

	# default is name
	if order == "" or not valid_order:
		type = ""
		order = "name"

	# done this way so that browse/ works properly
	if restaurant_name == None:
		restaurant_name = ""
	if restaurant_address == None:
		restaurant_address = ""

	# remove % encoding from url and strip punctuation
	restaurant_name = re.sub(r'[^\w\s]', '', urllib.unquote_plus(restaurant_name).lower())
	restaurant_address = re.sub(r'[^\w\s]', '', urllib.unquote_plus(restaurant_address).lower())
	
	# if they want all, set appropriate variable to blank
	if restaurant_name == "all":
		restaurant_name = ""
	if restaurant_address == "all":
		restaurant_address = ""

	# determine the upper limit based upon the english constants
	# these correspond with the groupings on the index page
	if upper_limit == "critical":
		upper_limit = CRITICAL_VAL+1
	elif upper_limit == "moderate":
		upper_limit = MODERATE_VAL+1
	elif upper_limit == "low":
		upper_limit = LOW_VAL+1
	elif not upper_limit.isdigit():
		upper_limit=9999
	else:
		upper_limit = int(upper_limit) + 1

	if lower_limit == "critical":
		lower_limit = CRITICAL_VAL
	elif lower_limit == "moderate":
		lower_limit = MODERATE_VAL
	elif lower_limit == "low":
		lower_limit = LOW_VAL
	elif not lower_limit.isdigit():
		lower_limit = 0

	
	# Query Database
	# the blank string parameters defined above will filter ALL
	try:
		results = Restaurant.objects.filter(name_clean__icontains=restaurant_name, address_clean__icontains=restaurant_address, health_report_status__gte=lower_limit, health_report_status__lt=upper_limit).order_by(type + order, '-health_report_status')
	except Restaurant.DoesNotExist:
		error = "No results."
	
	# Browse Page Display
	
	# if it isn't an api call
	if api_flag == None:
		# if there is only one result, render the view response page
		if len(results) == 1:
			restaurant = results[0]
			
			# Let's have it so that all views are done with the same URL. this eliminates duplicate code
			# TODO: Perhaps this escaping should be helper function somewhere
			restaurant.name = escape(urllib.quote_plus(restaurant.name.replace("/", "%2F")))
			restaurant.address = escape(urllib.quote_plus(restaurant.address.replace("/", "%2F")))
			return HttpResponseRedirect("/cs215/shirpi/view/" + restaurant.name + "/" + restaurant.address)
			
		# if there are no matches, error
		elif len(results) == 0:
			return render_to_response("SHIRPI/error.html", {'error':"No matches found"}, RequestContext(request))
		else:
			return render_to_response("SHIRPI/browse.html", {'restaurants': results, 'request': request}, RequestContext(request))
	
	# API Display
	else:
		display_type = request.GET.get('display')
		MySpecialApiData = []
		for location in results:
			if display_type == "full":
				report_results = HealthReport.objects.filter(restaurant=location)
			else:
				report_results = None
			MySpecialApiData.append({ 'location': location, 'reports': report_results })
		
		context = { 'results': MySpecialApiData, 'display_type': display_type }
		return render_to_response("SHIRPI/api.xml", context, RequestContext(request),  mimetype='application/xml')

'''
Function	: view_restaurant
Description	: view the information from a specific restaurant
Parameter(s)	: request - HttpRequest
		: restaurant_name - the name of the restaurant to display
		: restaurant_address - the address of the restaurant to display
Return 		: HttpResponse
'''
def view_restaurant(request, restaurant_name, restaurant_address):
	try:
		# get the restaurant, reports associated with that restaurant and comments
		restaurant = Restaurant.objects.get(name__iexact=urllib.unquote_plus(restaurant_name), address__iexact=urllib.unquote_plus(restaurant_address))
		reports = HealthReport.objects.filter(restaurant=restaurant)
		comments = Comment.objects.filter(restaurant=restaurant).order_by('-created')[0:5]
		form = CommentForm()


		commentable = True
		if request.user.is_authenticated():
			user = request.user
			ip = None
		else:
			user = User.objects.get( username = "Anonymous" )
			ip = request.META['REMOTE_ADDR']

		#context defined here so that isn't ugly
		context = {'restaurant': restaurant, 'reports': reports, 'comments': comments}
'''
		if ip == None:
			comment_set = Comment.objects.filter(author__username = user.username, restaurant = restaurant).order_by('-created')[:1]
		else:
			comment_set = Comment.objects.filter(author__username = user.username, restaurant = restaurant, ip = ip).order_by('-created')[:1]

		if len(comment_set) > 0:
			comment = comment_set[0]
			print str(comment_set)
	#		if comment.created + timedelta(days=1) <= datetime.now():
	#			context['form'] = form
	#	else:
	#		context['form'] = form

		print str(context)
'''
		return render_to_response("SHIRPI/view_restaurant.html", context, RequestContext(request))
	except Restaurant.DoesNotExist:
		# redirect 
		return HttpResponseRedirect("/cs215/shirpi/")

'''
Function	: view_profile
Description	: get and display the information on a user
Parameter(s)	: request - HttpRequest
		: user_name - the user whose information is to be viewed
Return 		: 
'''
def view_profile(request, user_name):
	# clean the username
	user_name = urllib.unquote_plus(user_name)

	# get the user from the DB or display error page
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error': "No user with username '" + user_name +"'"}, RequestContext(request))

	# get the favourites and comments for this user
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	comments = Comment.objects.filter(author=user_to_view)

	# render
	context = {'user_to_view': user_to_view, 'favourites': favourites, 'comments': comments}
	return render_to_response('SHIRPI/view_profile.html', context, RequestContext(request))	

# edit the current user's profile
'''
Function	: edit_profile
Description	: for the user to edit their profile
Parameter(s)	: request - HttpRequest
Return 		: HttpResponse
'''
def edit_profile(request):
	user = request.user

	# if the user isn't logged in, error
	if not user.is_authenticated():
		return render_to_response('SHIRPI/error.html', {'error': "You are not logged in"}, RequestContext(request))

	# if the edit form has been submitted
	if request.method == "POST":
		# ensure it is valid and process it
		form = ProfileForm(request.POST)
		if form.is_valid():
			if form.cleaned_data['new_password'] != form.cleaned_data['password_again']:
				return render_to_response('SHIRPI/edit_profile.html', {'message': "New passwords do not match"}, RequestContext(request))
			if user.check_password(form.cleaned_data['old_password']) != True:
				return render_to_response('SHIRPI/edit_profile.html', {'message': "Incorrect password"}, RequestContext(request))
			user.email = form.cleaned_data['email']
			if form.cleaned_data['new_password']!="":
				user.set_password(form.cleaned_data['new_password'])
			user.first_name = form.cleaned_data['first_name']
			user.last_name = form.cleaned_data['last_name']
			user.save()
			return render_to_response('SHIRPI/edit_profile.html', {'form': form, 'message': "Changes completed"}, RequestContext(request))

		# error if the form isn't valid
		else:
			return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))

	# otherwise render the page with the edit form
	form = ProfileForm(initial={'email': request.user.email, 'first_name': request.user.first_name, 'last_name': request.user.last_name})
	return render_to_response('SHIRPI/edit_profile.html', {'form': form}, RequestContext(request))
