from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display the info of one restaurant
@register.filter
def display_restaurant(value, autoescape=None):
	if value.cleanliness_count<1:
		value.cleanliness_count=1
	if value.combined_count<1:
		value.combined_count = 1
	if value.food_quality_count<1:
		value.food_quality_count=1
	if value.atmosphere_count<1:
		value.atmosphere_count = 1
	if value.wait_time_count<1:
		value.wait_time_count =1 
	result = "<div class='restaurant'>\n"
	result += "<h3 class='name'><a href='/cs215/shirpi/browse/" + value.name +"/" + value.address + "'>" + value.name + "</a></h3>"
	result +="<h3 class='address'>" + str(value.address) + "</h3>"
	result += "<h4>" + str(value.health_report_status) +"</h4>"
	result += "<h4>" + str(value.combined/value.combined_count) + "</h4>"
	result += "<h4>" + str(value.food_quality/value.food_quality_count) + "</h4>"
	result += "<h4>" + str(value.cleanliness/value.cleanliness_count) + "</h4>"
	result += "<h4>" + str(value.atmosphere/value.atmosphere_count) + "</h4>"
	result += "<h4>" + str(value.wait_time/value.wait_time_count) + "</h4>"
	result += "</div>"
	return mark_safe(result)
display_restaurant.needs_autoescape = True
