from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_favourite(favourite, autoescape=None):
	result = "<div class='favourite "
	if favourite.restaurant.health_report_status > 5:
		result+="critical"
	elif favourite.restaurant.health_report_status > 0:
		result += "moderate"
	else:
		result += "good"
	result += "'>"
	result += "<h4>" + str(favourite.rank) + "</h4>"
	result += "<h3 class='name'><a href='/cs215/shirpi/browse/" +favourite.restaurant.name+ "/" +favourite.restaurant.address+ "/'>" + str(favourite.restaurant.name) + "</a></h3>"
	result += "<h3>" + str(favourite.restaurant.address) + "</h3>"
	result += "</div>"
	return mark_safe(result)
display_favourite.needs_autoescape = True
display_favourite.needs_category = True


#display a group of restaurants in a table
@register.filter
def display_favourite_edit(favourite, count, autoescape=None):
	result = "<div id='favourite' class='"
	if favourite.restaurant.health_report_status > 5:
		result+="critical"
	elif favourite.restaurant.health_report_status > 0:
		result += "moderate"
	else:
		result += "good"
	result += "'>"
	result += "<h4 class='delete'><a href='/cs215/shirpi/delete_favourite/" + favourite.restaurant.name + "/" + favourite.restaurant.address + "/'>Del</a></h4>"
	result += "<h4><select name='" +favourite.restaurant.name+ "'>"
	for i in range(1, count):
		result += "<option"
		if i == favourite.rank:
			result += " selected='selected'"
		result += ">" + str(i) + "</option>"
	result += "</select></h4>"
	result += "<h3 class='name'><a href='/cs215/shirpi/browse/" +favourite.restaurant.name+ "/" +favourite.restaurant.address+ "/'>" + str(favourite.restaurant.name) + "</a></h3>"
	result += "<h4>" + str(favourite.restaurant.address) + "</h4>"
	return mark_safe(result)
display_favourite.needs_autoescape = True
display_favourite.needs_count = True


