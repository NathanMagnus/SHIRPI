import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

# display a group of restaurants in a table
@register.filter
def display_sort_field(request, autoescape=None):
	# the possible sorts
	sorts = [('name', "Name"), ('address_searchable', "Street"), ('combined', "Combined Scores"), ('cleanliness', "Cleanliness"), ('food_quality', "Food Quality"), ('atmosphere', "Atmosphere"), ('wait_time', "Wait Time")]
	get = request.GET.copy()

	# enclosing div
	result ="<div id='sort'>\n"
	result +="<h4>Sort By</h4>\n"
	result +="<ul id='sort_by'>\n"

	# for each type of sort
	for type, verbose in sorts:
		# default is descending
		get['type'] = "DESC"
		
		# if it is what is currently being sorted by
		if request.GET.get('sort_by', '') == type:
			# swap type of sort
			if request.GET.get('type', '') == "DESC":
				get['type'] = "ASC"
		# add sort_by to the GET parameters
		get['sort_by'] = type
		result +="<li class='type'><a href='?"+ get.urlencode() +"'>" + verbose + "</a></li>\n"
	result +="</ul>\n"
	return mark_safe(result)
