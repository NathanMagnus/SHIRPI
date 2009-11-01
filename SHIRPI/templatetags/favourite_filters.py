from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_favourite_set(set, category, autoescape=None):
	result = "<table>"
	result += "<tr><th>Rank</th><th>Name</th><th>Address</th></tr>"
	for favourite in set:
		result += "<tr>"
		result += "<td>" + str(favourite.rank) + "</td><td>"
		result += "<a href=\"/cs215/SHIRPI/browse/" +favourite.restaurant.name+ "/" +favourite.restaurant.address+ "/\">" + str(favourite.restaurant.name) + "</a></td>"
		result += "<td>" + str(favourite.restaurant.address) + "</td>"
		result += "</tr>"
	result += "</table>";
	return mark_safe(result)
display_favourite_set.needs_autoescape = True
display_favourite_set.needs_category = True
