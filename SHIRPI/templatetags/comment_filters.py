import urllib
from datetime import datetime, date
from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

from restaurant_filters import display_stars

register = template.Library()

'''
Function	: display_comment
Description	: display a comment
Parameter(s)	: value - the comment to be displayed
		: user - the user accessing this page
Return		: string containing the html for one comment
'''
@register.filter
def display_comment( value, user ):
	# TODO: Destory this ridiculous abuse of filters and properly expand template

	result = "<div class='comment_header'><h3 class='timestamp'>" 
	result += "<a href='#" + urllib.quote_plus(str(value.id)) + "' name ='" + str(value.id) + "'>" + str(value.last_modified.strftime("%B %d, %Y")) + "</a>"
	result += "</h3>\n"
	

	result += "<h3 class='username'>"
	# if the author isn't the anonymous user, display a link to their profile
	if value.author.username != "Anonymous":
	        result += "<a href='/cs215/shirpi/view_profile/" + urllib.quote_plus(value.author.username.replace("/", "%2F"))+ "/'>"
		result += value.author.username
		result += "</a>"
	else:
		result += "Anonymous"

	result += "</h3>"
	
		# if the current user is the author or an admin, let them delete the post
	if user.username == value.author.username or user.has_perm("SHIRPI.comment"):
		result += "<h4 class='delete'><a href='/cs215/shirpi/delete_comment/" + str(value.id) + "'>Delete</a></h4>"
	
	result += "</div>\n"
	
	# display the information for the comment
	result += "<div class='comment_attributes'>"		

	if value.food_quality > 0:
		result += "<h4>Food Quality</h4><ul>" + display_stars(value.food_quality) + "</ul>\n"
	
	if value.cleanliness > 0:
		result += "<h4>Cleanliness</h4><ul>" + display_stars(value.cleanliness) + "</ul>\n"
	
	if value.atmosphere > 0:
		result += "<h4>Atmosphere</h4><ul>" + display_stars(value.atmosphere)+ "</ul>\n"
	
	if value.wait_time > 0:
		result += "<h4 class='comment_overall'>Overall</h4><ul>" + display_stars(value.wait_time) + "</ul>\n"
		
	result += "</div>\n"
	
	# display comment and Generate link to edit comment
	result += "<div class='comment_body'>"

	# again, if author or admin, allow to edit
	if user.username == value.author.username or user.has_perm("SHIRPI.comment"):
		result += "<a href='/cs215/shirpi/edit_comment/" + urllib.quote_plus(str(value.pk).replace("/", "%2F") )+ "/'>" + escape(value.comment) + "</a>"
	else:
		result += escape(value.comment)

	result += "</div>\n"
	return mark_safe(result)

display_comment.needs_user = True

