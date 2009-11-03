from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_favourite_set(set, category, autoescape=None):
	result = "<table style=\"border-collapse: collapse;\">"
	result += "<caption>Favourites</caption>"
	result += "<tr><th style=\"width: 40px;\">Rank</th><th>Name</th><th>Address</th></tr>"
	for favourite in set:
		result += "<tr class=\""
		if favourite.restaurant.health_report_status > 5:
			result+="critical"
		elif favourite.restaurant.health_report_status > 0:
			result += "moderate"
		else:
			result += "good"
		result += "\">"
		result += "<td>" + str(favourite.rank) + "</td><td>"
		result += "<a href=\"/cs215/SHIRPI/browse/" +favourite.restaurant.name+ "/" +favourite.restaurant.address+ "/\">" + str(favourite.restaurant.name) + "</a></td>"
		result += "<td>" + str(favourite.restaurant.address) + "</td>"
		result += "</tr>"
	result += "</table>";
	return mark_safe(result)
display_favourite_set.needs_autoescape = True
display_favourite_set.needs_category = True


#display a group of restaurants in a table
@register.filter
def display_favourite_set_edit(set, category, autoescape=None):
	count = len(set) +1
	options = ""
	result = "<form name=\"edit_favourite\">"
	result += "<table style=\"border-collapse: collapse;\">"
	result += "<caption>Favourites</caption>"
	result += "<tr><th style=\"width: 40px;\">Rank</th><th>Name</th><th>Address</th></tr>"
	for favourite in set:
		result += "<tr class=\""
		if favourite.restaurant.health_report_status > 5:
			result+="critical"
		elif favourite.restaurant.health_report_status > 0:
			result += "moderate"
		else:
			result += "good"
		result += "\">"
		result += "<td><select name=\"" +str(favourite.rank)+ "\">"
		for i in range(1, count):
			result += "<option"
			if i == favourite.rank:
				result += " selected=\"selected\""
			result += ">" + str(i) + "</option>"
		result += "</select></td>"
		result += "<td><a href=\"/cs215/SHIRPI/browse/" +favourite.restaurant.name+ "/" +favourite.restaurant.address+ "/\">" + str(favourite.restaurant.name) + "</a></td>"
		result += "<td>" + str(favourite.restaurant.address) + "</td>"
		result += "</tr>"
	result += "</table>";
	return mark_safe(result)
display_favourite_set.needs_autoescape = True
display_favourite_set.needs_category = True


