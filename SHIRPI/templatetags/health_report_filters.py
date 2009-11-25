from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

'''
Function	: display_health_report
Description	: generate the html for one health report
Parameter(s)	: report - the report to have the html generated for
Return		: string of html to display one health report
'''
@register.filter
def display_health_report( report ):

	#enclosing div
	result = "<div class='health_report'>\n"

	# #display the date
	result += "<h3 class='report_date'>" + str(report.date.strftime("%A, %B %d %Y")) + "</h3>\n"

	# display each item in the report
	result += "<ul name='report_items'>\n"
	if report.items.count() >0:
		for item in report.items.all():
			result += "<li class='report_item'>" + item.description + "</li>\n"
	else:
		result += "<li class='report_item'>None</li>\n"
	result += "</ul>"
	result += "</div>\n"
	return mark_safe(result)
