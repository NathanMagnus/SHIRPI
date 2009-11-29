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
	# display label and input for form, populate with current GET values if possible
	result = ''
	
	try:
		name = escape(request.GET.get('restaurant_name', 'Location Name'))
		address = escape(request.GET.get('restaurant_address', 'Street / Address'))
		lower_limit = escape(request.GET.get('lower_limit', "0"))
		upper_limit = escape(request.GET.get('upper_limit', "100"))
		sort_by = escape(request.GET.get('sort_by', 'name'))
		sort_direction =  escape(request.GET.get('type', 'asc'))
	except:
		name = 'Location Name'
		address = 'Street / Address'
		lower_limit = '0'
		upper_limit = '100'
		sort_by = 'name'
		sort_direction = 'asc'
	
	
	# This is for display purposes. Easier to handle here than with javascript
	if name == '':
		name = 'Location Name'
	if address == '':
		address = 'Street / Address'
	
	
	result += "<input type='text' name='restaurant_name' id='restaurant_name' value='" + name + "' " + \
		"onblur=\"if (this.value == '') this.value='Location Name';\" onfocus=\"if (this.value == 'Location Name') this.value='';\"/>\n"
	
	result += "<input type='text' name='restaurant_address' id='restaurant_address' value='" + address + "' " + \
		"onblur=\"if (this.value == '') this.value='Street / Address';\" onfocus=\"if (this.value == 'Street / Address') this.value='';\"/>\n"
	
	
	# Dropdown menus.
	# TODO: Make this presentable.
	
	# Integer handling for dropdowns
	if not lower_limit.isdigit():
		lower_limit = 0
	if not upper_limit.isdigit():
		upper_limit = 100
	
	# lower_limit dropdown
	result += "<select name='lower_limit' id='lower_limit'>\n"
	result += "<option class='low' "
	if int(lower_limit) < MODERATE_VAL:
		result += "selected='selected' "
	result += "value='low'>Low</option>\n"
	
	result += "<option class='moderate' "
	if int(lower_limit) < CRITICAL_VAL and int(lower_limit) >= MODERATE_VAL:
		result += "selected='selected' "
	result += "value='moderate'>Moderate</option>\n"
	
	result += "<option class='critical' "
	if int(lower_limit) >= CRITICAL_VAL:
		result += "selected='selected' "
	result += "value='critical'>Critical</option>\n"
	result += "</select>"
	
	# upper_limit dropdown
	result += "<select name='upper_limit' id='upper_limit'>\n"
	result += "<option class='low' "
	if int(upper_limit) < MODERATE_VAL:
		result += "selected='selected' "
	result += "value='low'>Low</option>\n"
	
	result += "<option class='moderate' "
	if int(upper_limit) < CRITICAL_VAL and int(upper_limit) >= MODERATE_VAL:
		result += "selected='selected' "
	result += "value='moderate'>Moderate</option>\n"
	
	result += "<option class='critical' "
	if int(upper_limit) >= CRITICAL_VAL:
		result += "selected='selected' "
	result += "value='critical'>Critical</option>\n"
	result += "</select>"
	
	
	result += "<input type='hidden' name='sort_by' value='" + sort_by + "' />\n"
	
	result += "<input type='hidden' name='type' value='" + sort_direction + "' />\n"
	
	result += "<input type='submit' name='Submit' value='Search' id='search_sort_submit'/>"
	print "Filter Lower: " + repr(lower_limit)
	print "Filter Upper: " + repr(upper_limit)
	
	
	return mark_safe(result)
