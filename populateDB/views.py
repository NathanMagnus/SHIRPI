import xml.etree.cElementTree as et
from project.SHIRPI.models import *
import django
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

def populateMaster():
	# This section needs to be separate and with further admin panel accessibility.
	# Further, it needs an overhaul to allow for more content.
	items = ["Potentially hazardous foods and perishable foods must be stored at 4oC/40oF or below Hazardous foods must be thawed in a refrigerator or under cold, running water."] 
	items.append('<b>Temperatures</b> Cook foods to an internal temperature of: a) 63oC (145oF) or above for: eggs (if prepared for immediate service); medium rare beef and veal steaks and roasts; b) 68oC (155oF) or above for: game farm meat products; c) 70oC (158oF) for: fish; d) 71oC (160oF) or above for: ground beef/pork/veal; food made with ground beef/pork/veal, e.g. sausages, meatballs; pork chops, ribs and roasts; e) 74oC (165oF) or above for: ground chicken/turkey; food made with ground chicken/turkey or mixtures containing poultry, meat, fish, or eggs; chicken and turkey breasts, legs, thighs and wings; stuffing (inside a carcass); stuffed pasta; hot dogs; leftovers; egg dishes (if not prepared as specified in 2a); and stuffed fish; f) 85oC (185oC) or above for: chicken and turkey, whole bird. Reheat foods rapidly to an internal temperature of 74oC (165oF) prior to serving. Hot Holding must maintain an internal temperature of 60oC (140oF) or higher.')
	items.append('<b>Storage Containers</b> Foods must be stored in food grade containers, properly labeled and protected from contamination at all times.')
	items.append('<b>Hand Washing</b> Hand washing must be properly done at appropriate times and intervals. An accessible, plumbed hand basin with hot and cold running water, soap in a dispenser and single-use paper towels in wall-mounted dispensers are required in food preparation areas. Hand washing Procedure: a) Wet hands and exposed arms (at least up to wrist) with warm running water; b) Apply liquid soap; c) Vigorously rub together wet surfaces for at least 20 seconds, lathering at least up to wrist; d) Use a nailbrush under fingernails and other very dirty areas; e) Thoroughly rinse with clean, warm water running from wrists to fingertips; f) Apply soap and lather vigorously again; g) Rinse hands and wrists thoroughly; h) Dry hands with a single-use paper towel; and i) Use paper towel to turn off tap.')
	items.append('<b>Employee Hygiene</b> Good personal hygiene must be practiced at all times. Food handlers with infectious or contagious diseases (or symptoms) should not work. ')
	items.append('<b>Potential Contamination</b> Foods must be protected from contamination at all times.')
	items.append('<b>Dish Washing Procedures</b> Proper dish washing procedures must be followed. Mechanical washing: dishwashers must be National Sanitation Foundation (NSF) approved or equivalent, designed to wash at 60oC (140oF) and utilize an approved sanitizing agent. Manual washing: (wash/rinse/sanitize in a three-compartment sink): first compartment - clean hot water 44oC (111oF) with detergent; second compartment - clean hot water 44oC (111oF); third compartment - approved sanitizing method.')
	items.append('<b>Food and Water Source</b> Food, water and ice must be from an approved source and must also be wholesome, free from damage or spoilage and transported under proper temperatures, where applicable.')
	items.append('place holder for 9')

	items.append('<b>Food Storage</b> Food must be protected from contamination during storage, preparation, display, service and transport. No food is to be stored on the floor unless it is in an approved container. The lowest shelf is to be high enough to allow easy cleaning of the floor.')
	items.append('<b>Thermometer Access</b> An accurate, metal-stemmed (food-grade) probe thermometer must be available to monitor temperatures of potentially hazardous foods.')
	items.append('<b>Dish Washing Facilities</b> Approved dish washing facilities must be installed and properly maintained. An adequate supply of cleaning supplies, chemicals, etc. must be available at all times. \'Clean-in-place\' equipment must be washed and sanitized according to manufacturers instructions.')
	items.append('<b>Garbage Containers</b> An adequate number of approved, covered garbage containers must be provided at all food preparation areas. Containers are to be kept clean and the contents removed at least daily. Garbage storage must be of an approved design with a lid that seals. It must be kept clean and free of vermin and serviced as required.')
	items.append('<b>Vermin</b> All restaurants are to be free of vermin')
	items.append('<b>Building Conditions</b> Floors, walls and ceilings of all rooms in which food is stored, prepared or served or in which dishes, utensils and equipment are washed or stored should be kept clean and in good repair.')
	items.append('<b>Building Conditions</b> Approved plumbing must be installed and properly maintained to prevent food contamination.  Light shields or shatterproof bulbs are to be provided in every room in which food is prepared or stored. Unless otherwise approved, every restaurant is to have a ventilation system that prevents the accumulation of odours, smoke, grease/oils and condensation.')
	severities = ["2", "3", "2", "2", "2", "2", "3", "3", "1000", "2", "1", "2", "1", "4", "1", "1"]
	for i in range(1,17):

		try:
			item = HealthInspectionItem.objects.get(number=i)
		except HealthInspectionItem.DoesNotExist:	
			item = HealthInspectionItem()
			item.number =i
			item.severity = severities[i-1]
		item.description = items[i-1]
		item.save()
		
def populate(request, password):
	if password != "Popul8IT123!":
		return HttpResponseRedirect('/cs215/shirpi')
	existing=0
	new = 0
	populateMaster()
	for event, elem in et.iterparse("/home/cs215/project/populateDB/reports.xml"):
		if elem.tag == "location":
			#get/make the appropriate restaurant
			try:
				rest = Restaurant.objects.get(name=elem.attrib.get("name"), address = elem.attrib.get("address"))
			except Restaurant.DoesNotExist:
				rest = Restaurant()
				rest.name = elem.attrib.get("name")
				rest.address = elem.attrib.get("address")
				rest.visible = True
				rest.health_report_status=0
				#get/make the appropriate location if rest doesn't exist
				try:
					loc = Location.objects.get(rha=elem.attrib.get("rha"), municipality = elem.attrib.get("municipality"))
				except Location.DoesNotExist:
					loc = Location()
					loc.region = elem.attrib.get("rha")
					loc.municipality = elem.attrib.get("municipality")
					loc.city = "Regina"
					loc.province = "Saskatchewan"
					loc.country = "Canada"
					loc.save()
				rest.location = loc
				rest.save()
			#find each report
			for report in elem.findall("report"):
				#get/make the appropriate report
				try:
					rep = HealthReport.objects.get(date=report.attrib.get("date"), restaurant=rest)
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
					rest.health_report_status = score_total
					rest.save()
					rep.save()

	reports = HealthReport.objects.filter()
	return render_to_response('populateDB/populate.html', {'reports': reports, 'new': new, 'existing': existing})
