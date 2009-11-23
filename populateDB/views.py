import urllib
import time
from datetime import datetime, date, time
import xml.etree.cElementTree as et
from project.SHIRPI.models import *
import django
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

# main populate function, calls the appropriate helper function
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
			populate_reports()

			# get all reports and render
			reports = HealthReport.objects.filter()
			return render_to_response('populateDB/populate.html', {'reports': reports}, RequestContext(request))
		elif mode == "items":
			populate_items()
		elif mode == "anonymous":
			create_anonymous()
		else:
			error = "Bad mode"
	#render the error or success
	return render_to_response("SHIRPI/error.html", {'error': error}, RequestContext(request))

# populate the items
def populate_items():
	# file containing the item information
	from project.populateDB.items import *

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

# create the anonymous user
def create_anonymous():
	# if Anonymous already exists, don't do anything, otherwise create it
	try:
		User.objects.get(username="Anonymous")
	except User.DoesNotExist:
		anonymous = User.objects.create_user('Anonymous', 'none@none.com', '`1234567890-=~!@#$%^&*()_+QAZwsxEDCrfvTGByhnUJMik,OL.p;/[]')
		anonymous.save()

# populate the db with the reports
def populate_reports():
	# keep a count of the number of new reports and duplicates
	existing=0
	new = 0

	# create the anonymous user
	create_anonymous()

	# actually look at the xml now
	for event, elem in et.iterparse("/home/cs215/project/populateDB/reports.xml"):
		if elem.tag == "location":
			# get/make the appropriate restaurant
			try:
				rest = Restaurant.objects.filter(name__iexact=elem.attrib.get("name"), address__iexact = elem.attrib.get("address"))
			except Restaurant.DoesNotExist:
				rest = Restaurant()
				rest.name = elem.attrib.get("name")
				rest.address = elem.attrib.get("address")
				rest.visible = True
				rest.health_report_status=0
				# get/make the appropriate location if the restaurant doesn't exist
				try:
					loc = Location.objects.get(rha__iexact=elem.attrib.get("rha"), municipality__iexact = elem.attrib.get("municipality"))
				except Location.DoesNotExist:
					loc = Location()
					loc.rha = elem.attrib.get("rha")
					loc.municipality = elem.attrib.get("municipality")
					loc.city = "Regina"
					loc.province = "Saskatchewan"
					loc.country = "Canada"
					loc.save()
				
				# assign the location and save the restaurant
				rest.location = loc
				rest.save()

			# find each report, first one is always the most recent so keep track of which one is first
			first = True
			for report in elem.findall("report"):
				# get/make the appropriate report
				date_key = datetime.strptime( report.attrib.get("date"), "%A, %B %d, %Y" )
				try:
					rep = HealthReport.objects.filter(date=date_key, restaurant=rest)
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
