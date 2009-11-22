import re
import urllib
import xml.etree.cElementTree as et
from project.SHIRPI.models import *
import django
from django.template import RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

def populate(request):
	mode = urllib.unquote_plus(request.GET.get('mode', ""))
	password = urllib.unquote_plus(request.GET.get('password', ""))

	error = "Bad Password"
	if password == "Popul8IT123!":
		error = "Success"
		if mode == "reports":
			return populate_reports()
		elif mode == "items":
			populate_items()
		elif mode == "anonymous":
			create_anonymous()
		else:
			error = "Bad mode"
	return render_to_response("SHIRPI/error.html", {'error': error}, RequestContext(request))

def populate_items():
	from project.populateDB.items import *
	for item in items:
		try:
			dbItem = HealthInspectionItem.objects.get(number=item['number'])
		except HealthInspectionItem.DoesNotExist:	
			dbItem = HealthInspectionItem()
			dbItem.number =item['number']
			dbItem.severity = item['severity']
		dbItem.description = item['description']
		dbItem.short_description = item['short_description']
		dbItem.save()
		
def create_anonymous():
	try:
		User.objects.get(username="Anonymous")
	except User.DoesNotExist:
		anonymous = User.objects.create_user('Anonymous', 'none@none.com', '`1234567890-=~!@#$%^&*()_+QAZwsxEDCrfvTGByhnUJMik,OL.p;/[]')
		anonymous.save()

def populate_reports():
	reg = re.compile('(\d+)')
	existing=0
	new = 0
	create_anonymous()
	for event, elem in et.iterparse("/home/cs215/project/populateDB/reports.xml"):
		if elem.tag == "location":
			#get/make the appropriate restaurant
			try:
				rest = Restaurant.objects.get(name__iexact=elem.attrib.get("name"), address__iexact = elem.attrib.get("address"))
			except Restaurant.DoesNotExist:
				rest = Restaurant()
				rest.name = elem.attrib.get("name")
				rest.address = elem.attrib.get("address")
				rest.visible = True
				rest.health_report_status=0
				#get/make the appropriate location if rest doesn't exist
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
				rest.location = loc
				rest.save()
			#find each report
			first = True
			for report in elem.findall("report"):
				#get/make the appropriate report
				try:
					rep = HealthReport.objects.get(date=report.attrib.get("date"), restaurant=rest)
					first = False
					existing = existing+1
				except HealthReport.DoesNotExist:
					new = new+1
					rep = HealthReport()
					rep.date = report.attrib.get("date")
					rep.priority = report.attrib.get("priority")
					rep.type = report.attrib.get("type")
					rep.restaurant = rest
					rep.save()
					#add each item for this report
					score_total=0
					for item in report.findall("item"):
						item_text = item.text.lstrip().rstrip()
						item = HealthInspectionItem.objects.get(number=item_text)
						rep.items.add(item)
						score_total = item.severity + score_total
					rep.health_inspection_score = score_total
					if first:
						first = False
						rest.health_report_status = score_total
						rest.save()
					rep.save()

	reports = HealthReport.objects.filter()
	return render_to_response('populateDB/populate.html', {'reports': reports, 'new': new, 'existing': existing})
