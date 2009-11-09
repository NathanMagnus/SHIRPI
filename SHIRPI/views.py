# Create your views here.
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm 

from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import logout as djlogout
from django.views.generic.simple import direct_to_template
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

GOOD_VAL = 0
MODERATE_VAL = 1
CRITICAL_VAL = 5

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
	#if they inputted "All" for the restaurant name and address
	if restaurant_name.lower()=="all" and restaurant_address.lowercase=="all":
		#find all critical, moderate and good restauratns
		Critical = Restaurant.objects.filter(health_report_status__gte=CRITICAL_VAL).order_by("-health_report_status")
		Moderate = Restaurant.objects.filter(health_report_status__lt=CRITICAL_VAL).filter(health_report_status__gte=MODERATE_VAL).order_by("-health_report_status")
		Good = Restaurant.objects.filter(health_report_status__lte=GOOD_VAL).order_by("-health_report_status")
		#render the response
		return render_to_response("SHIRPI/browse.html", {'Critical':Critical, 'Moderate':Moderate, 'Good': Good, 'user':request.user})
	#if they want all restaurants with a certain address
	elif restaurant_name.lowercase=="all":
		try:
			chain = Restaurant.objects.filter(address__contains=restaurant_address)
		except Restaurant.DoesNotExist:
			error = "Restaurant with that address does not exist"
	#if they want a restaurant based on name
	elif restaurant_address.lowercase=="all":
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
		
	#if there was an error, this is because they are trying to get a restaurant that doesn't exist
#	except Restaurant.DoesNotExist:
#		try:
#			#see if the restaurant is a chain/has multipel locations
#			chain = Restaurant.objects.filter(name=restaurant_name)
#			#if it is a restaurant name with multiple locations, render it
#		except Restaurant.DoesNotExist: #if it isn't a restaurant "search"
#			chain = Restaurant.objects.filter(name__contains=restaurant_name)
#		if(len(chain)>0):
#			return render_to_response("SHIRPI/browse.html", {'chain': chain, 'user':request.user})
		return render_to_response("SHIRPI/browse.html", {'error':error}, RequestContext(request))
	else:
		return render_to_response("SHIRPI/browse.html", {'chain': chain}, RequestContext(request))

#user login
# These two functions are no longer needed.
def login(request):
	#set login template
        login_template = 'registration/login.html'
        form = AuthenticationForm()
	#if they submitted the form, authenticate and login
        if request.method == 'POST':
                user = authenticate(username=request.POST['username'], password=request.POST['password'])
                return djlogin(request, user)
#logout
def logout(request):
	#log them out, simple as that
	djlogout(request)
	return HttpResponseRedirect('/cs215/shirpi/');

#create a comment
def comment(request, restaurant_name, restaurant_address):
	#see if the restaurant exists
	try:
		restaurant = Restaurant.objects.get(name = restaurant_name, address = restaurant_address)
	except Restaurant.DoesNotExist: #if it doesn't exist, error
		return render_to_response('SHIRPI/comment.html', {'error':"The restaurant you are trying to comment on does not exist"}, RequestContext(request))
	form = CommentForm() #create the comment form and render
	return render_to_response('SHIRPI/comment.html', {'restaurant':restaurant, 'form':form}, RequestContext(request))

def save_edit(request, comment_id):
	if request.method=="POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			try:
				comment = Comment.objects.get(id=comment_id)
				restaurant = comment.restaurant
				#subtact old total
				restaurant.cleanliness = comment.restaurant.cleanliness - comment.cleanliness
				restaurant.food_quality = comment.restaurant.food_quality - comment.food_quality
				restaurant.atmosphere = comment.restaurant.atmosphere - comment.atmosphere
				restaurant.wait_time = comment.restaurant.wait_time - comment.wait_time
				restaurant.combined = comment.restaurant.combined - comment.combined
			
				#put in new total
				comment.comment = form.cleaned_data['comment']
				comment.cleanliness = form.cleaned_data['cleanliness']
				comment.food_quality = form.cleaned_data['food_quality']
				comment.atmosphere = form.cleaned_data['atmosphere']
				comment.wait_time = form.cleaned_data['wait_time']
				comment.combined = comment.cleanliness + comment.food_quality + comment.atmosphere - comment.wait_time

				restaurant.cleanliness = restaurant.cleanliness + comment.cleanliness
				restaurant.food_quality = restaurant.food_quality + comment.food_quality
				restaurant.atmosphere = restaurant.atmosphere + comment.atmosphere
				restaurant.wait_time = restaurant.wait_time + comment.wait_time
				restaurant.combined = restaurant.combined + comment.combined

				#save updates
				restaurant.save()
				comment.save()

				#forward to the restaurant browse
				return HttpResponseRedirect('/cs215/shirpi/browse/' + restaurant.name + '/' + restaurant.address + '/')

			#comment doesn't exist, error
			except Comment.DoesNotExist:
				return render_to_response('SHIRPI/comment.html', {'error': "Comment does not exist"}, RequestContext(requet))	

#save a comment
def save(request, restaurant_name, restaurant_address):
	#if the form was submitted
	if request.method=="POST":
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():
			#determine if restaurant exists
			try:
				restaurant = Restaurant.objects.get(name=restaurant_name, address=restaurant_address)
			except Restaurant.DoesNotExist:
				return render_to_response('SHIRPI/comment.html', {'error': "Restaurant or comment does not exist"}, RequestContext(request))
				#create the new comment and associate to the restaurant
			comment = Comment()
			comment.restaurant = restaurant
			#try to attach an author, if that fails make the author Anonymous
			try:
				author = User.objects.get(username=request.user.username)
			except User.DoesNotExist:
				author = User.objects.get(username="Anonymous")
			comment.author = author
	
			cleanliness = comment_form.cleaned_data['cleanliness']
			food_quality = comment_form.cleaned_data['food_quality']
			atmosphere = comment_form.cleaned_data['atmosphere']
			wait_time = comment_form.cleaned_data['wait_time']

			#assign the comment
			comment.comment = comment_form.cleaned_data['comment']
	
			#update the restaurant info and comment info/count
			if cleanliness>0:
				restaurant.cleanliness_count = restaurant.cleanliness_count + 1
				comment.cleanliness = cleanliness
				restaurant.cleanliness = restaurant.cleanliness + cleanliness
			if food_quality>0:
				restaurant.food_quality_count = restaurant.food_quality_count +1
				comment.food_quality = food_quality
				restaurant.food_quality = restaurant.food_quality = food_quality
			if atmosphere>0:
				restaurant.atmosphere_count = restaurant.atmosphere_count +1
				comment.atmosphere = atmosphere
				restaurant.atmosphere = restaurant.atmosphere + atmosphere
			if wait_time>0:
				restaurant.wait_time_count = restaurant.wait_time_count + 1
				comment.wait_time = wait_time
				restaurant.wait_time = restaurant.wait_time + wait_time
			comment.combined = atmosphere + food_quality + cleanliness - wait_time
			#update the comined info/count
			restaurant.combined_count = restaurant.combined_count + 1
			restaurant.combined = restaurant.combined + comment.combined

			#set datetime
			comment.created = datetime.now()
			comment.last_modified = datetime.now()
			#save everything
			restaurant.save()
			comment.save()
	#render response
	return HttpResponseRedirect('/cs215/shirpi/browse/' + restaurant_name + "/" + restaurant_address + "/")

#add the favourite to the user
def add_favourite(request, restaurant_name, restaurant_address):
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
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/view_favourites.html', {'error': "User does not exist"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view)
	
	return render_to_response('SHIRPI/view_favourites.html', {'favourites':favourites, 'user_to_view': user_to_view}, RequestContext(request))

def view_profile(request, user_name):
	try:
		user_to_view = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return render_to_response('SHIRPI/view_profile.html', {'error': "No user with username '" + user_name +"'"}, RequestContext(request))
	favourites = Favourite.objects.filter(user=user_to_view).order_by('rank')
	comments = Comment.objects.filter(author=user_to_view)
	return render_to_response('SHIRPI/view_profile.html', {'user_to_view': user_to_view, 'favourites': favourites, 'comments': comments}, RequestContext(request))	


def edit_comment(request, comment_id):
	try:
		comment = Comment.objects.get(id=comment_id)
		form = CommentForm(initial={'comment': comment.comment, 'cleanliness': int(comment.cleanliness), 'atmosphere': int(comment.atmosphere), 'wait_time': int(comment.wait_time), 'food_quality': int(comment.food_quality)})
		return render_to_response('SHIRPI/edit_comment.html', {'form': form, 'comment':comment}, RequestContext(request))
	except Comment.DoesNotExist:
		return render_to_response('SHIRPI/edit_comment.html', {'error': "That comment does not exist"}, RequestContext(request))

def view_comments(request, restaurant_name, restaurant_address):
	try:
		comments = Comment.objects.filter(restaurant__name = restaurant_name, restaurant__address = restaurant_address)
	except Comment.DoesNotExist:
		return HttpResponseRedirect('/cs215/shirpi/browse/' + restaurant_name + '/' + restaurant_address +'/')
	return render_to_response('SHIRPI/view_comments.html', {'comments': comments}, RequestContext(request))


def edit_favourites(request):
	if request.method=="POST":
		favourites = Favourite.objects.filter(user__username = request.user.username)
		for favourite in favourites:
			favourite.rank = request.POST[favourite.restaurant.name]
			favourite.save()
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')


def delete_favourite(request, restaurant_name, restaurant_address):
	try:
		favourite = Favourite.objects.get(user__username = request.user.username, restaurant__name = restaurant_name, restaurant__address = restaurant_address)
		favourite.delete()
	except Favourite.DoesNotExist:
		pass
	return HttpResponseRedirect('/cs215/shirpi/view_profile/' + request.user.username + '/')
