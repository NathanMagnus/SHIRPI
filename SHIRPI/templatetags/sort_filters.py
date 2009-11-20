import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_sort_field(request, autoescape=None):
	result ="	<div id='sort'>"

	result +="	<h4>Sort By</h4>"
	result +="	<div class='type'><a href='combined'>" + request.GET.items() + "</a></div>"
	result +="	<div class='type'><a href='cleanliness'>Cleanliness</a></div>"
	result +="	<div class='type'><a href='food_quality'>Food Quality</a></div>"
	result +="	<div class='type'><a href='atmosphere'>Atmosphere</a></div>"
	result +="	<div class='type'><a href='wait_time'>Wait Time</a></div>"
	result +="	</div>"
	return mark_safe(result)
