from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

# display a health report
@register.filter
def display_health_report( report, autoescape = None ):

	#enclosing div
	result = "<div class='health_report'>\n"

	# #display the date
	result += "<h3 class='report_date'>" + report.date + "</h3>\n"

	# display each item in the report
	result += "<ul name='report_items'>\n"
	if report.len() >0:
		for item in report.items.all():
			result += "<li class='report_item'>" + item.description + "</li>\n"
	else:
		result += "<li class='report_item'>None</li>\n"
	result += "</ul>"
	result += "</div>\n"
	return mark_safe(result)
display_health_report.needs_autoescape = True
