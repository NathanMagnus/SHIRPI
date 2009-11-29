import urllib
from django import template
from django.utils.html import conditional_escape, escape
from django.utils.safestring import mark_safe

from project.SHIRPI.settings import *
from project.SHIRPI.templatetags import sort_filters

register = template.Library()

'''
Function	: display_search_field
Description	: generate the html for the search field
Parameter(s)	: request - the HttpRequest for the page
Return		: string containing html for the search form
'''
@register.filter
def display_search_field( request ):
	# enclosing div
	result ="<div id='search'>\n"

	# display label and input for form, populate with current GET values
	result +="<input type='text' name='restaurant_name' id='restaurant_name' value='" + escape(request.GET.get('restaurant_name', "Location Name")) + "' " + \
		"onblur=\"if (this.value == '') this.value='Location Name';\" onfocus=\"if (this.value == 'Location Name') this.value='';\" " + \
		"onsubmit=\"if (this.value == 'Location Name') this.value='';\"/>\n"
	
	result +="<input type='text' name='restaurant_address' id='restaurant_address' value='" + escape(request.GET.get('restaurant_address', "Street / Address")) + "' " + \
		"onblur=\"if (this.value == '') this.value='Street / Address';\" onfocus=\"if (this.value == 'Street / Address') this.value='';\"/>\n"
	
	result +="<input type='text' name='lower_limit' id='lower_limit' value='" + escape(request.GET.get('lower_limit', "")) + "'/>\n"
	
	result +="<input type='text' name='upper_limit' id='upper_limit' value='" + escape(request.GET.get('upper_limit', "")) + "'/>\n"
	
	result +="<input type='hidden' name='sort_by' value='" + escape(request.GET.get('sort_by', 'name')) + "' />\n"
	
	result +="<input type='hidden' name='type' value='" + escape(request.GET.get('type', 'asc'))  + "' />\n"
	result +="</div>\n"
	
	#<input type="text" size="17" name="searchstr" value="Torrents" onblur="if (this.value == '') this.value='Torrents';" onfocus="if (this.value == 'Torrents') this.value='';" accesskey="t"/>
	
	return mark_safe(result)
