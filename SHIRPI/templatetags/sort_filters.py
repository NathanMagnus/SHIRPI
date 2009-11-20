import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

# display a group of restaurants in a table
# KYLE - If you dont' like it, rewrite it because thats all you do anyways
@register.filter
def display_sort_field(request, autoescape=None):
	sorts = [('combined', "Combined Scores"), ('cleanliness', "Cleanliness"), ('food_quality', "Food Quality"), ('atmosphere', "Atmosphere")]
	get = request.GET.copy()

	result ="<div id='sort'>\n"
	result +="<h4>Sort By</h4>\n"
	result +="<ul id='sort_by'>\n"
	for type, verbose in sorts:
		if request.GET.get('sort_by', "") == type:
			if get.get('type', "") == "ASC":
				get['type'] = "DESC"
			else:
				get['type'] = "ASC"
		result +="<li class='type'><a href='?"+ get.urlencode() +"'>" + verbose + "</a></li>\n"
	result +="</ul>\n"
	return mark_safe(result)
