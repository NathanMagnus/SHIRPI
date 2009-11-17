# Create your views here.
import urllib
from project.SHIRPI.models import *

from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


#add the favourite to the user
def add_favourite(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	rsetaurant_address = urllib.unquote_plus(restaurant_address)
	#if the user is not authenticated, just send them back to the browse page they were on
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/cs215/shirpi/browse/' + restaurant_name + '/' + restaurant_address + '/')
	#get the restaurant that is being added or send back to browse page if it doesn't exist
	try:
		restaurant = Restaurant.objects.get(name=restaurant_name, address = restaurant_address)
	except Restaurant.DoesNotExist:
		return HttpResponseRedirect('/cs215/shirpi/browse/' + restaurant_name + '/' + restaurant_address + '/')

	#see if the favourite already exists for this user, if it does, do nothing, otherwise add the favourite
	try:
		favourite = Favourite.objects.get(restaurant=restaurant, user__username = request.user.username)
	except Favourite.DoesNotExist:
		#get all preexisting favourites for the user
		users_favourites = Favourite.objects.filter(user__username = request.user.username).order_by("-rank")
		rank = len(users_favourites)+1
		favourite = Favourite()
		favourite.user = User.objects.get(username=request.user.username)
		favourite.restaurant = restaurant
		favourite.rank = rank
		favourite.save()
	return HttpResponseRedirect('/cs215/shirpi/view_favourites/' + request.user.username + '/')

def view_favourites(request, user_name):
	user_name = urllib.unquote_plus(user_name)
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/view_favourites.html', {'error': "User does not exist"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view)
	
	return render_to_response('SHIRPI/view_favourites.html', {'favourites':favourites, 'user_to_view': user_to_view}, RequestContext(request))

def edit_favourites(request):
	if request.method=="POST":
		favourites = Favourite.objects.filter(user__username = request.user.username)
		for favourite in favourites:
			favourite.rank = request.POST[favourite.restaurant.name]
			favourite.save()
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')


def delete_favourite(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)
	try:
		favourite = Favourite.objects.get(user__username = request.user.username, restaurant__name = restaurant_name, restaurant__address = restaurant_address)
		favourite.delete()
	except Favourite.DoesNotExist:
		pass
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')
