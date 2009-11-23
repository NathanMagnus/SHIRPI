# Create your views here.
import urllib
from project.SHIRPI.models import *
from project.SHIRPI.forms import CommentForm 

from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

#create a comment
def comment(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)
	#see if the restaurant exists
	try:
		restaurant = Restaurant.objects.get(name__iexact = restaurant_name, address__iexact = restaurant_address)
	except Restaurant.DoesNotExist: #if it doesn't exist, error
		return render_to_response('SHIRPI/error.html', {'error':"The restaurant you are trying to comment on does not exist"}, RequestContext(request))
	form = CommentForm() #create the comment form and render
	return render_to_response('SHIRPI/comment.html', {'restaurant':restaurant, 'form':form}, RequestContext(request))

def save_edit(request, comment_id):
	if request.method=="POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			try:
				comment = Comment.objects.get(id=comment_id)
				if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
					return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	
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
				comment.ip = request.META['REMOTE_ADDR']

				restaurant.cleanliness = restaurant.cleanliness + comment.cleanliness
				restaurant.food_quality = restaurant.food_quality + comment.food_quality
				restaurant.atmosphere = restaurant.atmosphere + comment.atmosphere
				restaurant.wait_time = restaurant.wait_time + comment.wait_time
				restaurant.combined = restaurant.combined + comment.combined

				#save updates
				restaurant.save()
				comment.save()

				#forward to the restaurant browse
				return HttpResponseRedirect("/cs215/shirpi/browse/"+urllib.quote_plus(restaurant.name)+"/"+urllib.quote_plus(restaurant.address)+"/")

			#comment doesn't exist, error
			except Comment.DoesNotExist:
				pass
	return render_to_response('SHIRPI/error.html', {'error': "Comment does not exist"}, RequestContext(request))	
#save a comment
def save(request, restaurant_name, restaurant_address):
	restaurant_name = urllib.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)
	#if the form was submitted
	if request.method=="POST":
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
			if cleanliness>0:
				restaurant.cleanliness_count = restaurant.cleanliness_count + 1
				comment.cleanliness = cleanliness
				restaurant.cleanliness = restaurant.cleanliness + cleanliness
			if food_quality>0:
				restaurant.food_quality_count = restaurant.food_quality_count +1
				comment.food_quality = food_quality
				restaurant.food_quality = restaurant.food_quality + food_quality
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
			if (comment.combined > 0):
				restaurant.combined_count = restaurant.combined_count + 1
			restaurant.combined = restaurant.combined + comment.combined

			#set datetime
			comment.created = datetime.now()
			comment.last_modified = datetime.now()
			comment.ip = request.META['REMOTE_ADDR']
			#save everything
			restaurant.save()
			comment.save()
	#render response
	return HttpResponseRedirect("/cs215/shirpi/browse/"+urllib.quote_plus(restaurant_name) + "/" + urllib.quote_plus(restaurant_address)+"/")

def edit_comment(request, comment_id):
	comment_id = urllib.unquote_plus(comment_id) #done to prevent attacks
	try:
		comment = Comment.objects.get(id=comment_id)
		if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
			return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	
		form = CommentForm(initial={'comment': comment.comment, 'cleanliness': int(comment.cleanliness), 'atmosphere': int(comment.atmosphere), 'wait_time': int(comment.wait_time), 'food_quality': int(comment.food_quality)})
		return render_to_response('SHIRPI/edit_comment.html', {'form': form, 'comment':comment}, RequestContext(request))
	except Comment.DoesNotExist:
		return render_to_response('SHIRPI/error.html', {'error': "That comment does not exist"}, RequestContext(request))

def view_comments(request, restaurant_name, restaurant_address):
	restaurant_name = urllilb.unquote_plus(restaurant_name)
	restaurant_address = urllib.unquote_plus(restaurant_address)
	try:
		comments = Comment.objects.filter(restaurant__name__iexact = restaurant_name, restaurant__address__iexact = restaurant_address)
	except Comment.DoesNotExist:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	return render_to_response('SHIRPI/view_comments.html', {'comments': comments}, RequestContext(request))

def delete_comment(request, comment_id):
	comment_id = urllib.unquote_plus(comment_id) #prevent attacks
	try:
		comment = Comment.objects.get(id=comment_id)	
		if request.user != comment.author and not request.user.has_perm("SHIRPI.comment"):
			return render_to_response('SHIRPI/error.html', {'error': "You are not the author of this comment"}, RequestContext(requet))	

		restaurant = comment.restaurant
		
		restaurant.cleanliness = restaurant.cleanliness - comment.cleanliness
		if comment.cleanliness > 0:
			restaurant.cleanliness_count = restaurant.cleanliness_count -1

		restaurant.atmosphere = restaurant.atmosphere - comment.atmosphere
		if comment.atmosphere > 0:
			restaurant.atmosphere_count = restaurant.atmosphere_count -1
		
		restaurant.food_quality = restaurant.food_quality - comment.food_quality
		if comment.food_quality > 0:
			restaurant.food_quality_count = restaurant.food_quality_count -1
		
		restaurant.wait_time = restaurant.wait_time - comment.wait_time
		if comment.wait_time > 0:
			restaurant.wait_time_count = restaurant.wait_time_count -1

		restaurant.combined = restaurant.combined - comment.combined
		if comment.combined > 0:
			restaurant.combined_count = restaurant.combined_count -1
		
		restaurant.save()
		comment.delete()
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	except Comment.DoesNotExist:
		return HttpResponseRedirect(request.META['HTTP_REFERER'])

