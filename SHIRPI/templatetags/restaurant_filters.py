import urllib
from cgi import escape
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

'''
Function	: display_restaurant
Description	: generate the html to display one restaurant
Parameter(s)	: restaurant - the restaurant to display
Return		: string of html to display one restaurant
'''
@register.filter
def display_restaurant( restaurant ):
	# prevent division by 0
	if restaurant.cleanliness_count<1:
		restaurant.cleanliness_count=1
	if restaurant.combined_count<1:
		restaurant.combined_count = 1
	if restaurant.food_quality_count<1:
		restaurant.food_quality_count=1
	if restaurant.atmosphere_count<1:
		restaurant.atmosphere_count = 1
	if restaurant.wait_time_count<1:
		restaurant.wait_time_count =1 

	# enclosing div
	result = "<div class='restaurant "
	if restaurant.health_report_status >= CRITICAL_VAL:
        	result+="critical"
	elif restaurant.health_report_status >= MODERATE_VAL:
		result += "moderate"
	else:
		result += "low"	
	
	# url escape name and address
	name = urllib.quote_plus(restaurant.name.replace("/", "%2F"))
	address = urllib.quote_plus(restaurant.address.replace("/", "%2F"))

	# display the information
	result += "'>\n"
	result += "<h4 class='name'><a href=\"/cs215/shirpi/view/" + name +"/" + address + "\">" + escape(restaurant.name) + "</a></h4>"
	result +="<h4 class='address'>" + escape(restaurant.address) + "</h4>"
	result += "<ul class='starset'>" + display_stars(restaurant.wait_time/restaurant.wait_time_count) + "</ul>"
	result +="<ul class='restaurant_info'>"
	result += "<li><h4>" + str(restaurant.health_report_status) +"</h4></li>"
	result += "<li><h4>" + str(round(restaurant.combined/restaurant.combined_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.food_quality/restaurant.food_quality_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.cleanliness/restaurant.cleanliness_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.atmosphere/restaurant.atmosphere_count,1)) + "</h4></li>"
	result +="</ul>"
	result += "</div>"
	
	return mark_safe(result)


@register.filter	
def display_stars(value):
	"""
	Generates series of stars (max 5) for given float.
		Full stars only displayed for whole numbers.
		Half stars displayed for decimal .5 to .9
	Parameters: value - float to reprent as stars
	Returns: <li> (must incase within <ul>)
	"""
	
	result = ""
	
	if value == 0:
		result += "<li></li>"
	elif value < 1:
		result += "<li class='astar ahalfstar'></li>"
	else:
		for i in range(1, 5):
			if int(value) / i >= 1:
				result += "<li class='astar'></li>"
		
		if value >= 5:
			result += "<li class='astar'></li>"
			
		elif value % int(value) >= 0.5:
			result += "<li class='astar ahalfstar'></li>"
		
	return mark_safe(result)

@register.filter
def display_class(restaurant):
	"""
	Displays textual class of restaurant
	Paramater: restaurant to be displayed
	"""
	
	if restaurant.health_report_status >= CRITICAL_VAL:
		return mark_safe("critical")
	
	elif restaurant.health_report_status >= MODERATE_VAL:
		return mark_safe("moderate")
	
	else:
		return mark_safe("low")
