import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *
from project.SHIRPI.templatetags import sort_filters

register = template.Library()

'''
Function	: display_search_field
Description	: generate the html for the search field
Parameter(s)	: request - the HttpRequest for the page
Return		: string containing html for the search form
'''
@register.filter
def display_search_field( request ):
	# enclosing div
	result ="<div id='search'>\n"

	# display label and input for form, populate with current GET values
	result +="<label for='restaurant_name'>Name:</label><input type='text' name='restaurant_name' id='restaurant_name' value='" + request.GET.get('restaurant_name', "") + "'/>\n"
	result +="<label for='restaurant_address'>Address:</label><input type='text' name='restaurant_address' id='restaurant_address' value='" + request.GET.get('restaurant_address', "") + "' /><br />\n"
	result +="<label for='lower_limit'>Lower Limit:</label><input type='text' name='lower_limit' id='lower_limit' value='" + request.GET.get('lower_limit', "") + "'/>\n"
	result +="<label for='upper_limit'>Upper Limit:</label><input type='text' name='upper_limit' id='upper_limit' value='" + request.GET.get('upper_limit', "") + "'/>\n"
	result +="<input type='hidden' name='sort_by' value='" + request.GET.get('sort_by', 'name') + "' />\n"
	result +="<input type='hidden' name='type' value='" + request.GET.get('type', 'asc')  + "' />\n"
	result +="</div>\n"
	return mark_safe(result)
