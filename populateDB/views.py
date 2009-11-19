import xml.etree.cElementTree as et
from project.SHIRPI.models import *
import django
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe


def populateMaster():
	# This section needs to be separate and with further admin panel accessibility.
	# Further, it needs an overhaul to allow for more content.
	# Kyle is all talk. DO IT don't complain about it
	items = [
		{'short_description': 'Improper storage of perishable foods', 
			'description': "Potentially hazardous foods and perishable foods must be stored at 4oC/40oF or below Hazardous foods must be thawed in a refrigerator or under cold, running water.",
			'severity': 3
			},
		{'short_description': 'Temperatures', 
			'description': 'Temperatures Cook foods to an internal temperature of: a) 63oC (145oF) or above for: eggs (if prepared for immediate service)\n<br />medium rare beef and veal steaks and roasts\n<br />b) 68oC (155oF) or above for: game farm meat products\n<br />c) 70oC (158oF) for: fish\n<br />d) 71oC (160oF) or above for: ground beef/pork/veal\n<br />food made with ground beef/pork/veal, e.g. sausages, meatballs\n<br />pork chops, ribs and roasts\n<br />e) 74oC (165oF) or above for: ground chicken/turkey\n<br />food made with ground chicken/turkey or mixtures containing poultry, meat, fish, or eggs\n<br />chicken and turkey breasts, legs, thighs and wings\n<br />stuffing (inside a carcass)\n<br />stuffed pasta\n<br />hot dogs\n<br />leftovers\n<br />egg dishes (if not prepared as specified in 2a)\n<br />and stuffed fish\n<br />f) 85oC (185oC) or above for: chicken and turkey, whole bird. Reheat foods rapidly to an internal temperature of 74oC (165oF) prior to serving. Hot Holding must maintain an internal temperature of 60oC (140oF) or higher.',
			'severity': 1
			},
		{'short_description': 'Storage Containers',
			'description': 'Foods must be stored in food grade containers, properly labeled and protected from contamination at all times.',
			'severity': 2
			},
		{'short_description': 'Hand Washing',
			'description': 'Hand washing must be properly done at appropriate times and intervals. An accessible, plumbed hand basin with hot and cold running water, soap in a dispenser and single-use paper towels in wall-mounted dispensers are required in food preparation areas. Hand washing Procedure: a) Wet hands and exposed arms (at least up to wrist) with warm running water\n<br />b) Apply liquid soap\n<br />c) Vigorously rub together wet surfaces for at least 20 seconds, lathering at least up to wrist\n<br />d) Use a nailbrush under fingernails and other very dirty areas\n<br />e) Thoroughly rinse with clean, warm water running from wrists to fingertips\n<br />f) Apply soap and lather vigorously again\n<br />g) Rinse hands and wrists thoroughly\n<br />h) Dry hands with a single-use paper towel\n<br />i) Use paper towel to turn off tap.',
			'severity': 2
			},
		{'short_description': 'Employee Hygiene',
			'description': 'Good personal hygiene must be practiced at all times. Food handlers with infectious or contagious diseases (or symptoms) should not work. ',
			'severity': 2
			},
		{'short_description': 'Potential Contamination',
			'description': 'Foods must be protected from contamination at all times.',
			'severity': 3
			},
		{'short_description': 'Dish Washing Procedures',
			'description': 'Proper dish washing procedures must be followed. Mechanical washing: dishwashers must be National Sanitation Foundation (NSF) approved or equivalent, designed to wash at 60oC (140oF) and utilize an approved sanitizing agent. Manual washing: (wash/rinse/sanitize in a three-compartment sink): first compartment - clean hot water 44oC (111oF) with detergent\n<br />second compartment - clean hot water 44oC (111oF)\n<br />third compartment - approved sanitizing method.',
			'severity': 3
			},
		{'short_description': 'Food and Water Source',
			'description': 'Food, water and ice must be from an approved source and must also be wholesome, free from damage or spoilage and transported under proper temperatures, where applicable.',
			'severity': 2
			},
		{'short_description': 'placeholder for 9', 
			'description': 'place holder for 9',
			'severity': 1
			},
		 {'short_description': 'Food Storage', 
			'description': 'Food must be protected from contamination during storage, preparation, display, service and transport. No food is to be stored on the floor unless it is in an approved container. The lowest shelf is to be high enough to allow easy cleaning of the floor.',
			'severity': 2
			},
		{'short_description': 'Thermometer Access',
			'description': 'An accurate, metal-stemmed (food-grade) probe thermometer must be available to monitor temperatures of potentially hazardous foods.',
			'severity': 2
			},
		{'short_description': 'Dish Washing Facilities',
			'description': 'Approved dish washing facilities must be installed and properly maintained. An adequate supply of cleaning supplies, chemicals, etc. must be available at all times. \'Clean-in-place\' equipment must be washed and sanitized according to manufacturers instructions.',
			'severity': 3
			},
		{'short_description': 'Garbage Containers',
			'description': 'An adequate number of approved, covered garbage containers must be provided at all food preparation areas. Containers are to be kept clean and the contents removed at least daily. Garbage storage must be of an approved design with a lid that seals. It must be kept clean and free of vermin and serviced as required.',
			'severity': 1
			},
		{'short_description': 'Vermin',
			'description': 'All restaurants are to be free of vermin',
			'severity': 5
			},
		{'short_description': 'Building Conditions',
			'description': 'Floors, walls and ceilings of all rooms in which food is stored, prepared or served or in which dishes, utensils and equipment are washed or stored should be kept clean and in good repair.',
			'severity': 1
			},
		{'short_description': 'Building Conditions',
			'description': 'Approved plumbing must be installed and properly maintained to prevent food contamination.  Light shields or shatterproof bulbs are to be provided in every room in which food is prepared or stored. Unless otherwise approved, every restaurant is to have a ventilation system that prevents the accumulation of odours, smoke, grease/oils and condensation.',
			'severity': 1
			}
		]

	for i in range(0,16):
		item = items[i]
		try:
			dbItem = HealthInspectionItem.objects.get(number=i+1)
		except HealthInspectionItem.DoesNotExist:	
			dbItem = HealthInspectionItem()
			dbItem.number =i+1
			dbItem.severity = item['severity']
		dbItem.description = item['description']
		dbItem.short_description = item['short_description']
		dbItem.save()
		
def createAnonymous():
	try:
		User.objects.get(username="Anonymous")
	except User.DoesNotExist:
		anonymous = User.objects.create_user('Anonymous', 'none@none.com', '`1234567890-=~!@#$%^&*()_+QAZwsxEDCrfvTGByhnUJMik,OL.p;/[]')
		anonymous.save()

def populate(request, password):
	if password != "Popul8IT123!":
		return HttpResponseRedirect('/cs215/shirpi')
	reg = re.compile('(\d+)')
	existing=0
	new = 0
	populateMaster()
	createAnonymous()
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
						item_text = reg.search(item_text).group(1)
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
