import xml.etree.cElementTree as et
import django

for event, elem in et.iterparse("reports.xml"):
	if elem.tag == "location": #get the element
		print (elem.attrib.get("rha"))
		print (elem.attrib.get("name"))
		print (elem.attrib.get("address"))
		print (elem.attrib.get("municipality"))
		#return	
	if elem.tag == "report":
		print (elem.attrib.get("date"))
		print (elem.attrib.get("priority"))
		print (elem.attrib.get("type"))
	if elem.tag == "item":
		print elem.text.lstrip().rstrip()
	elem.clear() 
