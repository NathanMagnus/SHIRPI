import urllib
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

'''
Function	: escape_url
Description	: escape a string so its safe in the url 
Parameter(s)	: value - the string to be escaped
Return		: string that is safe to put into a url
'''
@register.filter
def escape_url( value ):

	result = urllib.quote_plus(value).replace("/", "%2F")
	
	return mark_safe(result)
