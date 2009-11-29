import urllib
from django import template
from django.utils.html import conditional_escape, escape
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

	# display label and input for form, populate with current GET values if possible
	
	try:
		name = escape(request.GET.get('restaurant_name', 'Location Name'))
		address = escape(request.GET.get('restaurant_address', 'Street / Address'))
		lower_limit = escape(request.GET.get('lower_limit', ""))
		upper_limit = escape(request.GET.get('upper_limit', ""))
		sort_by = escape(request.GET.get('sort_by', 'name'))
		sort_direction =  escape(request.GET.get('type', 'asc'))
	except:
		name = 'Location Name'
		address = 'Street / Address'
		lower_limit = ''
		upper_limit = ''
		sort_by = 'name'
		sort_direction = 'asc'
	
	
	# This is for display purposes. Easier to handle here than with javascript
	if name == '':
		name = 'Location Name'
	if address == '':
		address = 'Street / Address'
	
	
	result +="<input type='text' name='restaurant_name' id='restaurant_name' value='" + name + "' " + \
		"onblur=\"if (this.value == '') this.value='Location Name';\" onfocus=\"if (this.value == 'Location Name') this.value='';\"/>\n"
	
	result +="<input type='text' name='restaurant_address' id='restaurant_address' value='" + address + "' " + \
		"onblur=\"if (this.value == '') this.value='Street / Address';\" onfocus=\"if (this.value == 'Street / Address') this.value='';\"/>\n"
	
	result +="<input type='text' name='lower_limit' id='lower_limit' value='" + lower_limit + "'/>\n"
	
	result +="<input type='text' name='upper_limit' id='upper_limit' value='" + upper_limit + "'/>\n"
	
	result +="<input type='hidden' name='sort_by' value='" + sort_by + "' />\n"
	
	result +="<input type='hidden' name='type' value='" + sort_direction + "' />\n"
	result +="</div>\n"
	
	
	return mark_safe(result)
