import urllib
import time
import re
import string
from datetime import datetime, date, time
import xml.etree.cElementTree as et
from project.SHIRPI.models import *
import django
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
# file containing the item information
from project.populateDB.items import *



'''
Function	: populate
Description	: determine what type of population is to be done and call the appropriate function
Parameter(s)	: request - HttpRequest
Return		: HttpResponse
'''
def populate(request):

	# get the mode and password from GET
	mode = urllib.unquote_plus(request.GET.get('mode', ""))
	password = urllib.unquote_plus(request.GET.get('password', ""))

	# check the password
	error = "Bad Password"
	if password == "Popul8IT123!":
		error = "Success"
		# check the mode
		if mode == "reports":
			 # return the value of populate_reports which is a http response
			return populate_reports(request)
		elif mode == "items":
			populate_items()
		elif mode == "anonymous":
			create_anonymous()
		else:
			error = "Bad mode"
	#render the error or success
	return render_to_response("SHIRPI/error.html", {'error': error}, RequestContext(request))

'''
Function	: populate_items
Description	: populate the default Health Inspection Item information
Parameter(s)	: None
Return		: None
'''
def populate_items():
	# populate each item
	for item in items:
		try:
			# if it already exists, do nothing
			dbItem = HealthInspectionItem.objects.get(number=item['number'])
		except HealthInspectionItem.DoesNotExist:
			# otherwise add it
			dbItem = HealthInspectionItem()
			dbItem.number =item['number']
			dbItem.severity = item['severity']

		# update the descriptions
		dbItem.description = item['description']
		dbItem.short_description = item['short_description']

		# save changes
		dbItem.save()

'''
Function	: create_anonymous
Description	: create the anonymous user
Parameter(s)	: None
Return		: None 	
'''
def create_anonymous():
	# if Anonymous already exists, don't do anything, otherwise create it
	try:
		User.objects.get(username="Anonymous")
	except User.DoesNotExist:
		anonymous = User.objects.create_user('Anonymous', 'none@none.com', '`1234567890-=~!@#$%^&*()_+QAZwsxEDCrfvTGByhnUJMik,OL.p;/[]')
		anonymous.save()

'''
Function	: populate_reports
Description	: populate the db with the reports from the reports file
		: reports file must be "/home/cs215/project/populateDB/reports.xml" and have the proper format
Parameter(s)	: request - a HttpRequest used to call this function
Return 		: HttpResponse
'''
def populate_reports(request):
	# keep a count of the number of new reports and duplicates
	existing=0
	new = 0

	# create the anonymous user
	create_anonymous()

	# actually look at the xml now
	for event, elem in et.iterparse("/home/cs215/project/populateDB/reports.xml"):
		if elem.tag == "location":
			name = elem.attrib.get("name")
			
			address = elem.attrib.get("address")
			address_searchable = re.sub("^\d+\s|\s\d+\s|\s\d+$", " ", address.translate(string.maketrans("",""), string.punctuation)).strip().lower() # easier to read than some of the one liners in this project
			
			# get/make the appropriate restaurant
			try:
				rest = Restaurant.objects.get(name__iexact=name, address__iexact = address)
			except Restaurant.DoesNotExist:
				rest = Restaurant()
				rest.name = name
				rest.address = address
				rest.address_searchable = address_searchable
				rest.visible = True
				rest.health_report_status=0
				# get/make the appropriate location if the restaurant doesn't exist
				rha = elem.attrib.get("rha")
				# City, Province POS COD
				re_results = re.match(r'(?P<city>^\w+), (?P<province>\w+) (?P<postal_code>\w+)', elem.attrib.get('municipality'))
				city = re_results.group('city')
				province = re_results.group('province')
				country = "Canada"
				postal_code = re_results.group('postal_code')

				try:
					loc = Location.objects.get(rha__iexact=rha)
				except Location.DoesNotExist:
					loc = Location()
					loc.rha = rha
					loc.city = city
					loc.province = province
					loc.country = country
					loc.save()
				
				rest.postal_code = postal_code
				# assign the location and save the restaurant
				rest.location = loc
				rest.save()

			# find each report, first one is always the most recent so keep track of which one is first
			first = True
			for report in elem.findall("report"):
				# get/make the appropriate report
				
				date_key = datetime.strptime( report.attrib.get("date"), "%A, %B %d, %Y" )
				date_key = date(date_key.year, date_key.month, date_key.day) # convert to date object

				try:
					rep = HealthReport.objects.get(date=date_key, restaurant=rest)
					first = False
					existing = existing+1
					
				except HealthReport.DoesNotExist:
					new = new+1
					rep = HealthReport()
					rep.date = date_key
					rep.priority = report.attrib.get("priority")
					rep.type = report.attrib.get("type")
					rep.restaurant = rest
					rep.save()
				
					# add each item for this report
					score_total=0
					for item in report.findall("item"):
						item_text = item.text.lstrip().rstrip()
						item = HealthInspectionItem.objects.get(number=item_text)
						rep.items.add(item)
						score_total = item.severity + score_total
					rep.health_inspection_score = score_total
					
					# if it is the first report, set the appropriate restaurants health_report_status
					if first:
						first = False
						rest.health_report_status = score_total
						rest.save()

					# save the report
					rep.save()

	# get all reports and render
	reports = HealthReport.objects.filter()
	return render_to_response('populateDB/populate.html', {'reports': reports, 'new': new, 'existing': existing}, RequestContext(request))
