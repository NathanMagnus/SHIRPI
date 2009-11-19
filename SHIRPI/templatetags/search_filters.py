import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *
from project.SHIRPI.templatetags import sort_filters

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_search_field(page, autoescape=None):
	result ="	<div id='search'>"
	result +="	<label for='restaurant_name'>Restaurant Name: </label><input type='text' name='restaurant_name' id='restaurant_name' /><br />"
	result +="	<label for='restaurant_address'>Restaurant Address: </label><input type='text' name='restaurant_address' id='restaurant_address' /><br />"
	result +="	<label for='upper_limit'>Upper Limit: </label><input type='text' name='upper_limit' id='upper_limit' />"
	result +="	<label for='lower_limit'>Lower Limit: </label><input type='text' name='lower_limit' id='lower_limit' />"
	result +="	</div>"
	return mark_safe(result)
