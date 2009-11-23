import urllib
from datetime import datetime, date
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display one comment
@register.filter
def display_comment( value, user, autoescape = None ):

	result = "<h3 class='timestamp'>" 
	result += "<a href='#" + urllib.quote_plus(str(value.id)) + "' name ='" + str(value.id) + "'>" + str(value.last_modified.ctime()) + "</a>"
	result += "</h3>\n"
	
	# if the current user is the author or an admin, let them delete the post
	if user.username == value.author.username or user.has_perm("SHIRPI.comment"):
		result += "<h4 class='delete'><a href='/cs215/shirpi/delete_comment/" + str(value.id) + "'>Delete</a></h4>"
	result += "<h3 class='username'>"

	# if the author isn't the anonymous user, display a link to their profile
	if value.author.username != "Anonymous":
	        result += "<a href='/cs215/shirpi/view_profile/" + urllib.quote_plus(value.author.username) + "/'>"
		result += value.author.username
		result += "</a>"
	else:
		result += "Anonymous"

	result += "</h3>\n"
	
	# display the information for the comment
	result += "<ul class='comment_attributes'>"		
	result += "<li><h4>Combined</h4>" + str(value.combined) + "</li>\n"
 	result += "<li><h4>Food Quality</h4>" + str(value.food_quality) + "</li>\n"
 	result += "<li><h4>Cleanliness</h4>" + str(value.cleanliness) + "</li>\n"
 	result += "<li><h4>Atmosphere</h4>" + str(value.atmosphere)+ "</li>\n"
 	result += "<li><h4>Wait Time</h4>" + str(value.wait_time) + "</li>\n"
	result += "</ul>\n"
	
	# display comment and Generate link to edit comment
	result += "<div class='comment_body'>"

	# again, if author or admin, allow to edit
	if user.username == value.author.username or user.has_perm("SHIRPI.comment"):
		result += "<a href='/cs215/shirpi/edit_comment/" + urllib.quote_plus(str(value.pk)) + "/'>" + value.comment + "</a>"
	else:
		result += value.comment

	result += "</div>\n"
	return mark_safe(result)

display_comment.needs_autoescape = True
display_comment.needs_user = True

