import urllib
from project.SHIRPI.models import *
from django.db.models import Max
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


'''
Function        : add_favourite
Description     : add a favourite to the user's favourite list
Parameter(s)    : request - HttpRequest
                : restaurant_name - the name of the restaurant to be added to the favourites
		: restaurant_address - the address of the restaurant to be added to the favourites
Return          : HttpResponse
'''
def add_favourite(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	rsetaurant_address = urllib.unquote_plus(restaurant_address)

	#if the user is not authenticated, just send them back to the browse page they were on
	if not request.user.is_authenticated():
		return HttpResponseRedirect('/cs215/shirpi/view/' + urllib.quote_plus(restaurant_name) + '/' + urllib.quote_plus(restaurant_address) + '/')

	#get the restaurant that is being added or send back to browse page if it doesn't exist
	try:
		restaurant = Restaurant.objects.get(name__iexact=restaurant_name, address__iexact = restaurant_address)
	except Restaurant.DoesNotExist:
		return HttpResponseRedirect('/cs215/shirpi/view/' + urllib.quote_plus(restaurant_name) + '/' + urllib.quote_plus(restaurant_address) + '/')

	#see if the favourite already exists for this user, if it does, do nothing, otherwise add the favourite
	try:
		favourite = Favourite.objects.get(restaurant=restaurant, user__username = request.user.username)
	except Favourite.DoesNotExist:
		# get all preexisting favourites for the user
		rank_set = Favourite.objects.filter(user__username = request.user.username).aggregate(Max('rank'))

		# determine the rank of this favourite
		if rank_set['rank__max'] == None:
			rank = 1 
		else:
			rank = rank_set['rank__max'] + 1
		favourite = Favourite()
		favourite.user = User.objects.get(username=request.user.username)
		favourite.restaurant = restaurant
		favourite.rank = rank
		favourite.save()

	return HttpResponseRedirect('/cs215/shirpi/view_favourites/' + request.user.username + '/')

'''
Function        : view_favourites
Description     : display the users favourites
Parameter(s)    : request - HttpRequest
                : user_name - the username of the user whose favourites are to be displayed
Return          : HttpResponse
'''
def view_favourites(request, user_name):
	user_name = urllib.unquote_plus(user_name)

	# get the user
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error': "User does not exist"}, RequestContext(request))

	# get the users favourites
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	
	return render_to_response('SHIRPI/view_favourites.html', {'favourites':favourites, 'user_to_view': user_to_view}, RequestContext(request))

'''
Function        : edit_favourites
Description     : edit the users favourites
Parameter(s)    : request - HttpRequest
Return          : HttpResponse
'''
def edit_favourites(request):

	# if the form was posted
	if request.method=="POST":
		# get the favourites for the user
		favourites = Favourite.objects.filter(user__username = request.user.username)

		# for each of these favourites, update the rank according to the form
		for favourite in favourites:
			favourite.rank = request.POST[favourite.restaurant.name]
			favourite.save()
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')


'''
Function        : delete_favourite
Description     : delete a favourite from the users favourites
Parameter(s)    : request - HttpResponse
                : restaurant_name - the name of the restaurant to be removed from the favourites
		: restaurant_address - the address of the restaurant to be removed from the favourites
Return          : HttpResponse
'''
def delete_favourite(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)
	try:
		# make sure the favourite exists
		favourite = Favourite.objects.get(user__username = request.user.username, restaurant__name__iexact = restaurant_name, restaurant__address__iexact = restaurant_address)

		# record its rank and delete it
		rank = favourite.rank
		favourite.delete()

		# get the rest of the favourites and update them
		favourites = Favourite.objects.filter(user__username = request.user.username, rank__gt = rank).order_by('rank')
		for favourite in favourites:
			favourite.rank = favourite.rank - 1
			favourite.save()
	except Favourite.DoesNotExist:
		pass
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')
