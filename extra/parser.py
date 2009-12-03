#!/usr/bin/python
# coding=ascii

'''
The html to xml parsing tool used alongside the scraper to get data for SHIRPI
'''

import xml.etree.cElementTree as ET
from BeautifulSoup import BeautifulSoup
import ntpath
import pprint
import glob
import time

class location():
	def __init__(self, name=None, address=None, inspection_type=None,
	municipality=None, RHA=None, reports=None):
		self.name = name
		self.address = address
		self.inspection_type = inspection_type
		self.municipality = municipality
		self.RHA = RHA 
		self.reports = reports
		
	def display(self):
		print self.name
		print self.address
		print self.municipality
		print self.RHA
		for report in self.reports:
			report.display()
		print ""


class report():
	def __init__(self, date=None, priority=None, inspection_type = None, items=None):
		self.date = date
		self. priority = priority
		self.inspection_type = inspection_type
		self.items = items
	
	def display(self):
		print "Rep. ", self.date
		print "  ", self.priority
		print "  ", self.inspection_type
		for value in self.items:
			print "\t-", value
		

def xml_barf(data):
	xml = ET.Element("reports")
	
	for listing in data:
		ET.SubElement(xml, "location", 
			name = listing.name, 
			address = listing.address, 
			municipality = listing.municipality,
			RHA = listing.RHA
		)
		
		for report in listing.reports:
			ET.SubElement(xml, "report", 
				type = report.inspection_type, 
				date = report.date, 
				priority = report.priority
			)
			
			for value in report.items:
				ET.SubElement(xml, "item").text = value
	
	return xml
	
def main():
	
	data = []
	
	# Parse each file within reports/
	# Note that each report is assumed to be stored within its own file.
	for file in glob.glob( ntpath.join("reports/", '*.html') ):
		html_data = BeautifulSoup(open(file, 'r'))
		new_report = location()
		
		# Retrieve required information from each HTML report
		new_report.name = html_data.find("td", { "class" : "a20" }).div.string
		new_report.address = html_data.find("td", { "class" : "a30" }).div.string
		new_report.municipality = html_data.find("td", { "class" : "a40" }).div.string
		new_report.RHA = html_data.find("td", { "class" : "a50" }).div.string
		
		
		new_report.reports = []
		for inner_data in html_data('html'):
			items = []
			for item in inner_data.findAll("td", { "class" : "a76" }):
				if hasattr(item.div, 'string'): # all divs named 'string'
					split_item = item.div.string.split(' - ')
					items.append(split_item[0])
					
			new_report.reports.append(report(
				inner_data.find("td", { "class" : "a22" }).div.string,  # date
				inner_data.find("td", { "class" : "a42" }).div.string,	# priority
				inner_data.find("td", { "class" : "a32" }).div.string,	# inspection type
				items))							# items array
			
		new_report.display()
		data.append(new_report)
	
	print "parsed. generating xml."	
	# Prettify XML file and save to disk
	open('output.xml', 'w').write(BeautifulSoup(ET.tostring(xml_barf(data))).prettify())
		
			

if __name__ == "__main__":
	main()
