from django import template
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()

#display a group of restaurants in a table
@register.filter
def display_restaurant_set(set, category, autoescape=None):
	#start table
	result = "<table class=\"" + category + " restaurant_set\">"
	result += "<caption>" + category.capitalize() + "</caption>"
	result += "<tr>" + display_restaurant_table_header(set) + "</tr>"
	#display info for each restaurant in the set
	for rest in set:
		result += "<tr>" + display_restaurant_info(rest) + "</tr>"
	#end table and return resulting table
	result += "</table>"
	return mark_safe(result)
display_restaurant_set.needs_autoescape = True
display_restaurant_set.needs_category = True

#display the info of one restaurant
@register.filter
def display_restaurant_info(value, autoescape=None):
	if value.cleanliness_count<1:
		value.cleanliness_count=1
	if value.combined_count<1:
		value.combined_count = 1
	if value.food_quality_count<1:
		value.food_quality_count=1
	if value.atmosphere_count<1:
		value.atmosphere_count = 1
	if value.wait_time_count<1:
		value.wait_time_count =1 
	result = '\n\t<td><a href="/cs215/SHIRPI/browse/' + value.name +'/' + value.address + '">' + value.name + '</a></td>'
	result += '<td>' + str(value.address) + '</td><td>' + str(value.health_report_status) +'</td>'
	result += '<td>' + str(value.combined/value.combined_count) + '</td><td>' + str(value.food_quality/value.food_quality_count) + '</td>'
	result += '<td>' + str(value.cleanliness/value.cleanliness_count) + '</td><td>' + str(value.atmosphere/value.atmosphere_count) + '</td><td>' + str(value.wait_time/value.wait_time_count) + '</td>'
	return mark_safe(result)
display_restaurant_info.needs_autoescape = True

#display a group of comments in a table
@register.filter
def display_comment_set(set, user_name, autoescape=None):
	#start the table
	result = ""
	
	result += "<div id='comment_set'>\n"
	result += "<h2>Comments</h2>\n"
	#result += <tr>"" + display_comment_table_header(set, user_name) + "</tr>\n"
	
	#put the information for each comment into the table
	for comment in set:
		result += "<div class='comment'>\n" + display_comment(comment, user_name) + "</	div>\n"
	#end the table and return it
	result += "</div>"
	
	return mark_safe(result)
display_comment_set.needs_autoescape=True
display_comment_set.needs_user_name = True

#display one comment
@register.filter
def display_comment(value, user_name,autoescape=None):

	result = "<h3 class='timestamp'>" 
	result += "<a href='#" + str(value.id) + "' name ='" + str(value.id) + "'>" + str(value.last_modified) + "</a>"	#Anchor position can be better set when layout is more mature
	#anyone ever tell you that you are petty? Do something productive instead of complaining
	result += "</h3>\n"

	result += "<h3 class='username'>"
	if value.author.username != "Anonymous":
	        result += "<a href='/cs215/SHIRPI/view_profile/" + value.author.username + "/'>" #ALWAYS ADD TRAILING SLASHES
		result += value.author.username
		result += "</a>"
	else:
		result += "Anonymous"
	result += "</h3>\n"
	
	
	result += "<ul class='comment_attributes'>"		
	result += '<li><h4>Combined</h4>'+ str(value.combined)+'</li>\n'
 	result += '<li><h4>Food Quality</h4>'+ str(value.food_quality) +'</li>\n'
 	result += '<li><h4>Cleanliness</h4>'+ str(value.cleanliness) +'</li>\n'
 	result += '<li><h4>Atmosphere</h4>'+ str(value.atmosphere)+'</li>\n'
 	result += '<li><h4>Wait Time</h4>'+ str(value.wait_time) +'</li>\n'
	result += "</ul>\n"
	
	#Display comment and Generate link to edit comment, kinda.
	result += "<div class='comment_body'>"
	if user_name == value.author.username:
		result += '<a href="/cs215/SHIRPI/edit_comment/' + str(value.pk) + '">' + value.comment + "</a>"
	else:
		result += value.comment
	result += "</div>\n"
	
	return mark_safe(result)
display_comment.needs_autoescape = True
display_comment.needs_user_name = True

#display restaurant title row
@register.filter
def display_restaurant_table_header(value, autoescape=None):
	result =  '<th>Name</th><th width="200px">Address</th><th>HI Status</th><th>Combined</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th>'
	return mark_safe(result)
display_restaurant_table_header.needs_autoescape = True

#display comment title row
@register.filter
def display_comment_table_header(value, autoescape=None):
	result = '<th>Author</th><th width="300px">Comment</th><th>Combined</th><th>Food Quality</th><th>Cleanliness</th><th>Atmosphere</th><th>Wait Time</th>'
	return mark_safe(result)
display_comment_table_header.needs_autoescape = True

