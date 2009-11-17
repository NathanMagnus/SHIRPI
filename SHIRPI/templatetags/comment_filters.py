import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display one comment
@register.filter
def display_comment(value, user_name,autoescape=None):

#	result = "<div class='comment'>\n"
	result = "<h3 class='timestamp'>" 
	result += "<a href='#" + urllib.quote_plus(str(value.id)) + "' name ='" + urllib.quote_plus(str(value.id)) + "'>" + str(value.last_modified) + "</a>"	#Anchor position can be better set when layout is more mature
	#anyone ever tell you that you are petty? Do something productive instead of complaining
	result += "</h3>\n"

	result += "<h3 class='username'>"
	if value.author.username != "Anonymous":
	        result += "<a href='/cs215/shirpi/view_profile/" + urllib.quote_plus(value.author.username) + "/'>" #ALWAYS ADD TRAILING SLASHES
		result += value.author.username
		result += "</a>"
	else:
		result += "Anonymous"
	result += "</h3>\n"
	
	
	result += "<ul class='comment_attributes'>"		
	result += "<li><h4>Combined</h4>"+ str(value.combined)+"</li>\n"
 	result += "<li><h4>Food Quality</h4>"+ str(value.food_quality) +"</li>\n"
 	result += "<li><h4>Cleanliness</h4>"+ str(value.cleanliness) +"</li>\n"
 	result += "<li><h4>Atmosphere</h4>"+ str(value.atmosphere)+"</li>\n"
 	result += "<li><h4>Wait Time</h4>"+ str(value.wait_time) +"</li>\n"
	result += "</ul>\n"
	
	#Display comment and Generate link to edit comment, kinda.
	result += "<div class='comment_body'>"
	if user_name == value.author.username:
		result += "<a href='/cs215/shirpi/edit_comment/" + urllib.quote_plus(str(value.pk)) + "/'>" + value.comment + "</a>" #always add trailing slashes eh kyle? Miss one here? jerk
	else:
		result += value.comment
	result += "</div>\n"
#	result += "</div>"
	
	return mark_safe(result)
display_comment.needs_autoescape = True
display_comment.needs_user_name = True

