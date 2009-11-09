from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display the info of one restaurant
@register.filter
def display_restaurant(restaurant, autoescape=None):
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
	result = "<div class='restaurant "
	if restaurant.restaurant.health_report_status > 5:
        	result+="critical"
	elif restaurant.restaurant.health_report_status > 0:
		result += "moderate"
	else:
		result += "good"						
	restul += "'>\n"
	result += "<h4 class='name'><a href=\"/cs215/shirpi/browse/" + restaurant.name +"/" + restaurant.address + "\">" + restaurant.name + "</a></h3>"
	result +="<h4 class='address'>" + str(restaurant.address) + "</h3>"
	result +="<ul class='restaurant_info'>"
	result += "<li><h4>" + str(restaurant.health_report_status) +"</h4></li>"
	result += "<li><h4>" + str(round(restaurant.combined/restaurant.combined_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.food_quality/restaurant.food_quality_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.cleanliness/restaurant.cleanliness_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.atmosphere/restaurant.atmosphere_count,1)) + "</h4></li>"
	result += "<li><h4>" + str(round(restaurant.wait_time/restaurant.wait_time_count,1)) + "</h4></li>"
	result +="</ul>"
	result += "</div>"
	return mark_safe(result)
display_restaurant.needs_autoescape = True
