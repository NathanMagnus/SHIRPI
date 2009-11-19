import urllib
from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_sort_field(page, autoescape=None):
	result ="<form name='sort' id='sort_form'>"
	result +=
	"
		<div id='sort'>
		<h4>Sort By</h4>
		<div class='type'><a href='"+page+"?order_by=combined'>Combined Score</a></div>
		<div class='type'><a href='"+page+"?order_by=cleanliness'>Cleanliness</a></div>
		<div class='type'><a href='"+page+"?order_by=food_quality'>Food Quality</a></div>
		<div class='type'><a href='"+page+"?order_by=atmosphere'>Atmosphere</a></div>
		<div class='type'><a href='"+page+"?order_by=wait_time'>Wait Time</a></div>
		<h4>Exclude By</h4>
		<div class='type'><a href='"+page+"?exclude_by=good'>Good</a></div>
		<div class='type'><a href='"+page+"?exclude_by=moderate'>Moderate</a></div>
		<div class='type'><a href='"+page+"?exclude_by=critical'>Critical</a></div>
		</div>
	"
	return mark_safe(result)
