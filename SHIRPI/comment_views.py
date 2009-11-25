# Create your views here.
import urllib
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm 

from datetime import datetime, date, timedelta
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

'''
Function	: comment
Description	: View for the comment page. Creates the form and gets appropriate restaurant
Parameter(s)	: request - The Http Request
		: restaurant_name - the name of the restaurant being commented on (passed through url)
		: restaurant_address - the address of the restaurant being commented on (passed through url)
Return		: HttpResponse for the appropriate template
'''

def comment( request, restaurant_name, restaurant_address ):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)

	if request.user.is_authenticated():
		user = request.user
		ip = None
	else:
		user = User.objects.get( username = "Anonymous" )
		ip = request.META['REMOTE_ADDR']

	#see if the restaurant exists or error
	try:
		restaurant = Restaurant.objects.get(name__iexact = restaurant_name, address__iexact = restaurant_address)
		if ip == None:
			comment_set = Comment.objects.filter(author__username = user.username, restaurant = restaurant).order_by('-created')[:1]
		else:
			comment_set = Comment.objects.filter(author__username = user.username, restaurant = restaurant, ip = ip).order_by('-created')[:1]
		if len(comment_set) > 0:
			comment = comment_set[0]
			if comment.created + timedelta(days=1) > datetime.now():
				return render_to_response('SHIRPI/error.html', {'error': "You can only comment on a restaurant once per day"}, RequestContext(request))

	except Restaurant.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error':"The restaurant you are trying to comment on does not exist"}, RequestContext(request))
	except Comment.DoesNotExist:
		pass


	# create comment form and render
	form = CommentForm()
	return render_to_response('SHIRPI/comment.html', {'restaurant':restaurant, 'form':form}, RequestContext(request))

'''
Function	: update_values
Description	: Update restaurant values and counts appropriately
Parameter(s)	: restaurant - Restaurant object that is to be editted
		: comment - the Comment object that contains the new values
		: method - integer (-1 or 1) indicating whether the new values are to be subtracted or added to the restaurant object
Return		: None
'''
def update_values(restaurant, comment, method):
	
	'''
		For all cases: Update the restaurnat value, if the comment had a count of greater than 0
		then update the count for the appropriate field in the restaurant
	'''
	restaurant.cleanliness = restaurant.cleanliness + method * comment.cleanliness
	if comment.cleanliness>0:
		restaurant.cleanliness_count = restaurant.cleanliness_count + method * 1
	
	restaurant.food_quality = restaurant.food_quality + method * comment.food_quality
	if comment.food_quality>0:
		restaurant.food_quality_count = restaurant.food_quality_count + method * 1
	
	restaurant.atmosphere = restaurant.atmosphere + method * comment.atmosphere
	if comment.atmosphere>0:
		restaurant.atmosphere_count = restaurant.atmosphere_count + method * 1

	restaurant.wait_time = restaurant.wait_time + method * comment.wait_time
	if comment.wait_time>0:
		restaurant.wait_time_count = restaurant.wait_time_count + method * 1
	
	restaurant.combined = restaurant.combined + method * comment.combined
	if comment.combined>0:
		restaurant.combined_count = restaurant.combined_count + method * 1
	restaurant.save()

'''
Function	: save_edit 
Description	: save the edits done to a comment
Parameter(s)	: request - the HttpRequest
		: comment_id - id of the comment that is being modified
Return		: HttpResponse (error template if error or redirect to the restaurant being commented on)
'''
def save_edit(request, comment_id):
	# if a form has been submitted
	if request.method=="POST":
		# if the form is valid
		form = CommentForm(request.POST)
		if form.is_valid():
			# try to get the old comment
			try:
				comment = Comment.objects.get(id=comment_id)
				# if this user isn't the author, error
				if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
					return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	
				restaurant = comment.restaurant

				# subtract old comment info from the restaurant totals
				update_values(restaurant, comment, -1)
			
				#put in comment info
				comment.comment = form.cleaned_data['comment']
				comment.cleanliness = form.cleaned_data['cleanliness']
				comment.food_quality = form.cleaned_data['food_quality']
				comment.atmosphere = form.cleaned_data['atmosphere']
				comment.wait_time = form.cleaned_data['wait_time']
				comment.combined = comment.cleanliness + comment.food_quality + comment.atmosphere - comment.wait_time
				comment.ip = request.META['REMOTE_ADDR']

				# update restaurant totals with new values
				update_values(restaurant, comment, 1)

				# save comment
				comment.save()

				#forward to the restaurant browse
				return HttpResponseRedirect("/cs215/shirpi/view/"+urllib.quote_plus(restaurant.name)+"/"+urllib.quote_plus(restaurant.address)+"/")

			#comment doesn't exist, error
			except Comment.DoesNotExist:
				return render_to_response('SHIRPI/error.html', {'error': "Comment does not exist"}, RequestContext(request))	

		# render the comment edit page 
		return render_to_response('SHIRPI/edit_comment.html', {'form': form}, RequestContext(request))

'''
Function	: save
Description	: Save a comment
Parameter(s)	: request - HttpRequest
		: restaurant_name - name of the restaurant being commented on
		: restaurant_address - address of the restaurant being commented on
Return		: HttpResponse
'''
def save(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)

	#if the form was submitted properly
	if request.method=="POST":
		
		#determine if the form is valid
		comment_form = CommentForm(request.POST)
		if comment_form.is_valid():

			#determine if restaurant exists
			try:
				restaurant = Restaurant.objects.get(name__iexact=restaurant_name, address__iexact=restaurant_address)
			except Restaurant.DoesNotExist:
				return render_to_response('SHIRPI/error.html', {'error': "Restaurant or comment does not exist"}, RequestContext(request))
			
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
			comment.cleanliness = cleanliness
			comment.food_quality = food_quality
			comment.atmosphere = atmosphere
			comment.wait_time = wait_time
			comment.combined = atmosphere + food_quality + cleanliness - wait_time

			# add the new values to the restaurant
			update_values(restaurant, comment, 1)

			#set datetime
			comment.created = datetime.now()
			comment.last_modified = datetime.now()
			comment.ip = request.META['REMOTE_ADDR']
			
			#save everything
			restaurant.save()
			comment.save()
	
	#render response
	return HttpResponseRedirect("/cs215/shirpi/view/"+urllib.quote_plus(restaurant_name) + "/" + urllib.quote_plus(restaurant_address)+"/")

'''
Function	: edit_comment
Description	: save the changes to a comment
Parameter(s)	: request - HttpRequest
		: comment_id - the comment to be editted
Return		: HttpResponseRedirect
'''
def edit_comment(request, comment_id):
	
	# anything passed through the url is a potential problem - unquote the comment_id
	comment_id = urllib.unquote_plus(comment_id)

	# get the comment, check that the logged in user is the author then render the edit form
	# any error in this process will return the appropriate error message on the error template
	try:
		comment = Comment.objects.get(id=comment_id)

		if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
			return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	

		form = CommentForm(initial={'comment': comment.comment, 'cleanliness': int(comment.cleanliness), 'atmosphere': int(comment.atmosphere), 'wait_time': int(comment.wait_time), 'food_quality': int(comment.food_quality)})

		return render_to_response('SHIRPI/edit_comment.html', {'form': form, 'comment':comment}, RequestContext(request))

	except Comment.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error': "That comment does not exist"}, RequestContext(request))

'''
Function	: view_comments
Description	: display comments
Parameter(s)	: request - HttpRequest
		: restaurant_name - name of the restaurant for which the comments are to be displayed
		: restaurant_address - address of the restaurant for which the comments are to be displayed
Return		: HttpResponse
'''
def view_comments(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)

	# get the comments or redirect to the referer page
	try:
		comments = Comment.objects.filter(restaurant__name__iexact = restaurant_name, restaurant__address__iexact = restaurant_address).order_by('created')
	except Comment.DoesNotExist:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

	# render the comments page
	return render_to_response('SHIRPI/view_comments.html', {'comments': comments}, RequestContext(request))

'''
Function	: delete_comment
Description	: delete a comment from the database permanently
Parameter(s)	: request - HttpRequest
		: comment_id - the id of the comment to be deleted
Return		: HttpResponse
'''
def delete_comment(request, comment_id):
	# prevent any issues due to comment id value
	comment_id = urllib.unquote_plus(comment_id)

	try:
		# get the comment
		comment = Comment.objects.get(id=comment_id)	

		# if this user doesn't have permission to remove the comment, redirect them to error page
		if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
			return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	

		# get the restaurant and update the values
		restaurant = comment.restaurant
		update_values(restaurant, comment, -1)

		# delete the comment
		comment.delete()

		# redirect to referer
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	except Comment.DoesNotExist:
		# if this comment doesn't exist, redirect to referer
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

