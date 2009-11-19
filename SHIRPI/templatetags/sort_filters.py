import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_sort_field(page, autoescape=None):
	result ="	<div id='sort'>"


	result +="	<h4>Sort By</h4>"
	result +="	<div class='type'><input type='radio' value='combined'>Combined Score</a></div>"
	result +="	<div class='type'><input type='radio' value='cleanliness'>Cleanliness</a></div>"
	result +="	<div class='type'><input type='radio' value='food_quality'>Food Quality</a></div>"
	result +="	<div class='type'><input type='radio' value='atmosphere'>Atmosphere</a></div>"
	result +="	<div class='type'><input type='radio' value='wait_time'>Wait Time</a></div>"
	result +="	</div>"
	return mark_safe(result)
