import urllib
from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

'''
Function	: display_sort_options
Description	: generate the html for the sort options
Parameter(s)	: request - the HttpRequest for the page
Return		: string of the html for the search options
'''
@register.filter
def display_sort_options(request):
	# the possible sorts
	# Form: type (name in database and passed through url), verbose (representative text for display), default sorting type
	sorts = [('name_clean', "Name", "ASC"),
		('address_clean', "Street", "ASC"),
		('address', "Address", "ASC"),
		('combined', "Combined Scores", "DESC"),
		('cleanliness', "Cleanliness", "DESC"),
		('food_quality', "Food Quality", "DESC"),
		('atmosphere', "Atmosphere", "DESC"),
		('wait_time', "Wait Time", "DESC")]
	get = request.GET.copy()

	# enclosing div
	result ="<div id='sort'>\n"
	result +="<ul>\n"
	
	
	# Construct list of 
	for type, verbose, default in sorts:
		# default is descending
		get['type'] = default
		
		# if it is what is currently being sorted by
		if request.GET.get('sort_by', '') == type:
			# swap type of sort
			if request.GET.get('type', default) == "DESC":
				get['type'] = "ASC"
			else:
				get['type'] = "DESC"
		
		# add sort_by to the GET parameters
		get['sort_by'] = type
		result +="<li><a id='" + type + "' href='?"+ escape(get.urlencode()) +"'>" + verbose + "</a></li>\n"
		
	result +="</ul>\n"
	result +="</div>\n"
	return mark_safe(result)
