import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

# display a favourite
@register.filter
def display_favourite( favourite, autoescape = None ):

	# enclosing div for styling
	result = "<div class='restaurant "
	if favourite.restaurant.health_report_status > CRITICAL_VAL:
		result += "critical"
	elif favourite.restaurant.health_report_status > MODERATE_VAL:
		result += "moderate"
	else:
		result += "low"
	result += "'>\n"

	# display the info and link
	result += "<h4>" + str(favourite.rank) + "</h4>\n"
	result += "<h3 class='name'><a href=\"/cs215/shirpi/view/" + urllib.quote_plus(favourite.restaurant.name)+ "/" + urllib.quote_plus(favourite.restaurant.address) + "/\">" + str(favourite.restaurant.name) + "</a></h3>\n"
	result += "<h3>" + str(favourite.restaurant.address) + "</h3>\n"
	result += "</div>\n"
	return mark_safe(result)

display_favourite.needs_autoescape = True
display_favourite.needs_category = True

# display a fourite and allow editting
@register.filter
def display_favourite_edit( favourite, count, autoescape = None ):
	# count will be 0 based
	count = count + 1

	#
	result = "<div id='favourite' class='"
	if favourite.restaurant.health_report_status > CRITICAL_VAL:
		result += "critical"
	elif favourite.restaurant.health_report_status > MODERATE_VAL:
		result += "moderate"
	else:
		result += "low"
	result += "'>"

	# display info, link, delete option and current rank
	result += "<h4 class='delete'><a href=\"/cs215/shirpi/delete_favourite/" + urllib.quote_plus(favourite.restaurant.name) + "/" + urllib.quote_plus(favourite.restaurant.address) + "/\">Del</a></h4>\n"
	result += "<h4><select name=\"" + favourite.restaurant.name + "\">\n"
	for i in range(1, count):
		result += "<option"
		if i == favourite.rank:
			result += " selected='selected'"
		result += ">" + str(i) + "</option>"
	result += "</select></h4>\n"
	result += "<h3 class='name'><a href=\"/cs215/shirpi/view/" + urllib.quote_plus(favourite.restaurant.name) + "/" + urllib.quote_plus(favourite.restaurant.address) + "/\">" + str(favourite.restaurant.name) + "</a></h3>\n"
	result += "<h4>" + str(favourite.restaurant.address) + "</h4>\n"
	result += "</div>"
	return mark_safe(result)

display_favourite.needs_autoescape = True
display_favourite.needs_count = True


