from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()
@register.filter
def display_rest_info(value, autoescape=None):
	result = '<tr>\n\t<td><a href="/cs215/hello/browse/' + value.name +'/">' + value.name + '</a></td>'
	result += '<td>' + str(value.street_address) + '</td><td>' + str(value.combined) +'</td>'
	result += '<td>' + str(value.health_inspection_status) + '</td><td>' + str(value.food_quality) + '</td>'
	result += '<td>' + str(value.cleanliness) + '</td><td>' + str(value.atmosphere) + '</td><td>' + str(value.wait_time) + '</td>'
	result += '</tr>'
	return mark_safe(result)
display_rest_info.needs_autoescape = True

@register.filter
def display_comment(value, user_name,autoescape=None):
	result = '<tr>'
        result += '<td><a href="/cs215/hello/profile/' + value.author.username+ '">'+value.author.username+'</a></td>'
 	result += '<td>'
	if user_name == value.author.username:
		result += '<a href="/cs215/hello/edit_comment/' + str(value.pk) + '">' + value.comment + '</a>'
	else:
		result += value.comment
	result += '<td>'
	result += '<td>'+ str(value.combined)+'</td>'
 	result += '<td>'+ str(value.food_quality) +'</td>'
 	result += '<td>'+ str(value.cleanliness) +'</td>'
 	result += '<td>'+ str(value.atmosphere)+'</td>'
 	result += '<td>'+ str(value.wait_time) +'</td>'
 	result += '</tr>'
	return mark_safe(result)
display_comment.needs_autoescape = True
display_comment.needs_user_name = True

@register.filter
def display_rest_table_header(value, autoescape=None):
	result =  '<tr><th>Name</th><th width="200px">Address</th><th>Combined</th><th>HI Status</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th></tr>'
	return mark_safe(result)
display_rest_table_header.needs_autoescape = True

@register.filter
def display_comment_table_header(value, autoescape=None):
	result = ' <tr><th>Author</th><th width="300px">Comment</th><th>Combined</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th></tr>'
	return mark_safe(result)
display_comment_table_header.needs_autoescape = True

