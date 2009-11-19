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
	result +="	<div class='type'><a href='"+page+"?order_by=combined'>Combined Score</a></div>"
	result +="	<div class='type'><a href='"+page+"?order_by=cleanliness'>Cleanliness</a></div>"
	result +="	<div class='type'><a href='"+page+"?order_by=food_quality'>Food Quality</a></div>"
	result +="	<div class='type'><a href='"+page+"?order_by=atmosphere'>Atmosphere</a></div>"
	result +="	<div class='type'><a href='"+page+"?order_by=wait_time'>Wait Time</a></div>"
	result +="	<h4>Exclude By</h4>"
	result +="	<div class='type'><a href='"+page+"?exclude_by=good'>Good</a></div>"
	result +="	<div class='type'><a href='"+page+"?exclude_by=moderate'>Moderate</a></div>"
	result +="	<div class='type'><a href='"+page+"?exclude_by=critical'>Critical</a></div>"
	result +="	</div>"
	return mark_safe(result)
