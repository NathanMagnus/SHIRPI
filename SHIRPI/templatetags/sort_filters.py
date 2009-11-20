import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_sort_field(request, autoescape=None):
	sorts = [('combined', "Combined Scores"), ('cleanliness', "Cleanliness"), ('food_quality', "Food Quality"), ('atmosphere', "Atmosphere")]
	get = request.GET.copy()
	result ="	<div id='sort'>"

	result +="	<h4>Sort By</h4>"
	result +="	<ul>"
	for type, verbose in sorts:
		get['sort_by'] = type
		result +="<li class='type'><a href='?"+ get.urlencode() +"'>" + verbose + "</a></li>"
	result +="	</ul>"
	return mark_safe(result)
