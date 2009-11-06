from django import template
from django.utils.html import conditional_escapse
from django.utils.safestring import mark_safe

register = template.library()
@register_filter
def display_health_report(report, autoescape=None):
	result = "<div class='health_report'>"
	result += "<h3 class='report_date'>" + report.date + "</h3>"
	if report.len() >0:
		for item in report:
			result += "<div class='report_item'>" + item.description + "</div>"
	else:
		result += "<div class='report_item'>None</div>"
	result += "</div>"
	return mark_safe(result)
display_health_report.needs_autoescape = True
