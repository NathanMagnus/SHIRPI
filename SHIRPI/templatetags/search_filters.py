import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_search_field(page, autoescape=None):
	result ="<form name='search' id='search_form' method='get'>"
	result +="	<div id='search'>"
	result +="	<label for='restaurant_name'>Restaurant Name: </label><input type='text' name='restaurant_name' id='restaurant_name' /><br />"
	result +="	<label for='restaurant_address'>Restaurant Address: </label><input type='text' name='restaurant_address' id='restaurant_address' /><br />"
	result +="	</div>"
	result +="	<input type='submit' name='submitSearch' value='Search' />"
	result += "</form>"
	return mark_safe(result)
