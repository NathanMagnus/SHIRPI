# Create your views here.
from django.shortcuts import *
from django.http import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, forms
from django.contrib.auth import login as djlogin
from django.contrib.auth import logout as djlogout
from hello.models import *
from django.views.generic.simple import direct_to_template
from django import forms
from django.http import HttpResponseRedirect
try:
	CRIT_VAL = HICategory.objects.get(category="Critical").max_value
except HICategory.DoesNotExist:
	CRIT_VAL = 9
try:
	MOD_VAL = HICategory.objects.get(category="Moderate").max_value
except HICategory.DoesNotExist:
	MOD_VAL = 2
try:
	GOOD_VAL =  HICategory.objects.get(category="Good").max_value
except HICategory.DoesNotExist:
	GOOD_VAL = 0


def save(request, rest_name):
	try:
#Set up comment info and save in db
		#if the comment already exists, select it
		try:
			comment = Comment.objects.get(id = rest_name)
			count = 1
			rest_name = comment.restaurant.name #change the rest name so that restaurant can be selected
		except:#otherwise, new comment
			comment = Comment()
			count =0
		try:  #if the user is authenticated, they are the author
			request.user.is_authenticated()
			comment.author = User.objects.get(username = request.user.username)
		except User.DoesNotExist:#otherwise anonymous auther
			comment.author = User.objects.get(username="Anonymous")
		comment.restaurant = Restaurant.objects.get(name=rest_name)
		rest = comment.restaurant
		#update rest stats
		rest.cleanliness = rest.cleanliness - float(comment.cleanliness) + float(request.POST['cleanliness'])
		rest.food_quality = rest.food_quality - float(comment.food_quality)+float(request.POST['food_quality'])
		rest.atmosphere = rest.atmosphere - float(comment.atmosphere) +float(request.POST['atmosphere'])
		rest.wait_time = rest.wait_time - float(comment.wait_time) + float(request.POST['wait_time'])
		rest.comment_count = int(rest.comment_count) + int(count)
		
		rest.combined = rest.combined - float(comment.combined)
		comment.comment = request.POST['comment']
		comment.cleanliness = request.POST['cleanliness']
		comment.food_quality = request.POST['food_quality']
		comment.atmosphere = request.POST['atmosphere']
		comment.wait_time = request.POST['wait_time']
		comment.combined = float(comment.cleanliness)+ float(comment.food_quality) + float(comment.atmosphere) - float(comment.wait_time)
		
		rest.combined = rest.combined + float(comment.combined)
		rest.save()
		comment.save()
#set up restaurant info and save in db

	except Restaurant.DoesNotExist:
		return HttpResponseRedirect('/cs215/hello/')
	return HttpResponseRedirect('/cs215/hello/browse/'+rest_name+'/')

def index(request):
	MAXSHOW = 10
	crit = Restaurant.objects.filter(health_inspection_status__gte=CRIT_VAL)[0:MAXSHOW]
	mod = Restaurant.objects.filter(health_inspection_status__gte=MOD_VAL).filter(health_inspection_status__lt=CRIT_VAL)[0:MAXSHOW]
	good = Restaurant.objects.filter(health_inspection_status__lte=GOOD_VAL)[0:MAXSHOW]
	return render_to_response('hello/index.html', {'user': request.user, 'Critical': crit, 'Moderate': mod, 'Good': good})

def comment(request, rest_name):
	form = CommentForm(request.POST)
	rest = Restaurant.objects.get(name=rest_name)
	return render_to_response('hello/comment.html', {'rest':rest, 'form': form, 'user': request.user})

def login(request):
	login_template = 'registration/login.html'
	form = AuthenticationForm()
#	form = LoginForm(request.POST)
	if request.method == 'POST':
		user = authenticate(username=request.POST['username'], password=request.POST['password'])
		return djlogin(request, user)
	return render_to_response(login_template, {'error': "Login failed", 'next': '/cs215/hello/', 'user': request.user})

def logout(request):
#	form = LoginForm(request.POST)
	djlogout(request)
	return direct_to_template(request, 'hello/index.html')

def browse(request, rest_name):
	try:
		rest = Restaurant.objects.get(name=rest_name)
		comments = Comment.objects.filter(restaurant = rest)
		return render_to_response('hello/browse.html', {'rest': rest, 'comments': comments, 'user': request.user})
	except Restaurant.DoesNotExist:
		crit = Restaurant.objects.filter(health_inspection_status__gte=CRIT_VAL)
		mod = Restaurant.objects.filter(health_inspection_status__gte=MOD_VAL).filter(health_inspection_status__lt=CRIT_VAL)
		good = Restaurant.objects.filter(health_inspection_status__lte=GOOD_VAL)
		if rest_name == "All":	
			return render_to_response('hello/browse.html', {'user': request.user, 'Critical': crit, 'Moderate': mod, 'Good': good})
		elif rest_name == "Good":
			return render_to_response('hello/browse.html', {'user': request.user, 'Good': good})
		elif rest_name == "Moderate":
			return render_to_response('hello/browse.html', {'user': request.user, 'Moderate': mod})
		elif rest_name == "Critical":
			return render_to_response('hello/browse.html', {'user': request.user, 'Critical': crit})
		else:
			return render_to_response('hello/browse.html', {'error': "Restaurant " +rest_name +" does not exist.", 'user': request.user})

def register(request):
	error = None	
	rform = RegistrationForm()
	if request.method == "POST":
		rform = RegistrationForm(request.POST)
		if rform.is_valid() and request.POST['password'] == request.POST['password_again']: #if the form is valid, see if they can be signed up
			try:
				user_exists = User.objects.get(username=request.POST['username'])
				return render_to_response('hello/register.html', {'rform': rform, 'user': request.user, 'error': "Username already exists"})
			except User.DoesNotExist:
				new_user = User.objects.create_user(request.POST['username'], request.POST['email'],request.POST['password'])
				new_user.first_name = request.POST['first_name']
				new_user.last_name = request.POST['last_name']
				new_user.save()
				user = authenticate(username=new_user.username, password=request.POST['password'])
				djlogin(request, user)
				return HttpResponseRedirect('/cs215/hello/profile/' + request.POST['username'] + '/')
		else:
			error = "Registration form had one or more invalid fields"
	return render_to_response('hello/register.html', {'rform': rform, 'user': request.user, 'error': error})

def userProfile(request, user_name):
	u = User.objects.get(username = user_name)
	comments = Comment.objects.filter(author = u)
	favourites = Favourite.objects.filter(user = u)
	profile = User.objects.get(username = user_name)
	return render_to_response('hello/profile.html', {'user': request.user, 'myprofile':user_name==request.user.username, 'favourites': favourites, 'profile':profile, 'comments':comments})

def edit_favourites(request):
	favourites = Favourite.objects.filter(user__username=request.user.username)
	return render_to_response('hello/edit_favourites.html', {'favourites': favourites, 'user': request.user})

def edit_comment(request, comment_id):
	comment = Comment.objects.get(id=comment_id)
	if request.user != comment.author:
		return HttpResponseRedirect('/cs215/hello');
	form = CommentForm(initial={'comment':comment.comment, 'food_quality': comment.food_quality, 'cleanliness': comment.cleanliness, 'atmosphere': comment.atmosphere, 'wait_time': comment.wait_time})
	return render_to_response('hello/edit_comment.html', {'comment': comment, 'form':form})
