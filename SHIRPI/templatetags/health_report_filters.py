from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def display_health_report( report ):
	'''
	Function	: display_health_report
	Description	: generate the html for one health report
	Parameter(s)	: report - the report to have the html generated for
	Return		: string of html to display one health report
	'''

	#enclosing div
	result = "<div id='r" + report.date.strftime("%B-%d-%Y") + "' class='health_report'>\n"

	# #display the date
	result += "<h3 class='report_date'>" + str(report.date.strftime("%A, %B %d %Y")) + "</h3>\n"

	# display each item in the report
	result += "<ul class='report_items'>\n"
	if report.items.count() >0:
		for item in report.items.all():
			result += "<li class='report_item'>" + item.number + ". " + item.short_description
			result += "<br />" + item.description + "</li>\n"
	else:
		result += "<li class='report_item'>None</li>\n"
	result += "</ul>"
	result += "</div>\n"
	return mark_safe(result)

@register.filter
def display_health_report_list_element( report ):
	'''
	Function	: display_health_report_list_element
	Description	: generate a <li> for one health report. Used for psudo ajaxing.
	Parameter(s)	: report - the report to have the <li> generated for
	Return		: string of <li> to display one health report
	'''
	
	result = "<li><a href='#' onclick=\"display_report('" + display_health_report_handle(report) + "'); return false;\">" + str(report.date.strftime("%B %d %Y")) + "</a></li>"
	return mark_safe(result)

@register.filter
def display_health_report_handle( report ):
	'''
	Function	: display_health_report_handle
	Description	: generate a date-based handle for use as XHTML id
	Parameter(s)	: report - the report to have the handle generated for
	Return		: string of handle to display for health report
	'''
	
	result = "r" + report.date.strftime("%B-%d-%Y")
	return mark_safe(result)