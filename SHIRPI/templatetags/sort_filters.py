import urllib
from django import template
from django.utils.html import conditional_escape
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
	sorts = [('name', "Name", "ASC"), ('address_searchable', "Street", "ASC"), ('combined', "Combined Scores", "DESC"), ('cleanliness', "Cleanliness", "DESC"), ('food_quality', "Food Quality", "DESC"), ('atmosphere', "Atmosphere", "DESC"), ('wait_time', "Wait Time", "DESC")]
	get = request.GET.copy()

	# enclosing div
	result ="<div id='sort'>\n"
	result +="<h4>Sort By</h4>\n"
	result +="<ul id='sort_by'>\n"

	# for each type of sort
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
		result +="<li class='type'><a href='?"+ get.urlencode() +"'>" + verbose + "</a></li>\n"
	result +="</ul>\n"
	return mark_safe(result)
