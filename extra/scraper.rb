require 'watir'
require 'fileutils'


reports = {}

handles = {
	:municipality => "ctl00_ContentPlaceHolder1_rvReport_ctl00_ctl05_ctl00",
	:location => "ctl00_ContentPlaceHolder1_rvReport_ctl00_ctl07_ctl00",
	:reports => "ctl00_ContentPlaceHolder1_rvReport_ctl00_ctl09_ctl00",
	:view_button => "ctl00_ContentPlaceHolder1_rvReport_ctl00_ctl00",
	:report_frame => "ReportFramectl00_ContentPlaceHolder1_rvReport"
}

# Folder preparation and manipulation
begin
	FileUtils.rm_rf('reports_old')
	FileUtils.move('reports', 'reports_old')	# backup of previous execution
	FileUtils.mkdir('reports')
rescue
	puts "Error accessing reports directories: " +$!
	exit 1
end

# Watir initialization
browser = Watir::Browser.new
browser.speed = :fast
browser.goto('http://orii.health.gov.sk.ca/rhaReport.aspx?RHA=4')

# Municipality manaully set. Must be valid.
# TODO: Consider expanding service to multiple municiplaties & automation
municipality = "Regina"
browser.select_list(:id, handles[:municipality]).set(municipality)
reports[municipality] = {}

# get all premises names as array
locations = browser.select_list(:id, handles[:location]).getAllContents
locations.delete_at(0) # NOTE: the ruby delete_ operation RETURNS the REMOVED VALUE and modifies the array 

# TODO: Consider threading this to decrease run time substantially
locations.each { |location|
		begin # exception: no reports available for location/premises
			reports[municipality][location] = []
			
			# set premises dropdown	
			browser.select_list(:id, handles[:location]).set(location)
			
			# get all report names as array			
			report_list = browser.select_list(:id, handles[:reports]).getAllContents
			report_list.delete_at(0)
				
			report_list.each { |report|
				
				browser.select_list(:id, handles[:reports]).set(report)
				
				browser.button(:id, handles[:view_button]).click
				
				
				# retrieve report url from mess
				report_url = browser.frame(:id, handles[:report_frame]).html
				report_url = report_url.scan(/"(\/Reserved\.ReportViewerWebControl\.axd\?.+)"/)[0][0]	# weird
				report_url = report_url.gsub("&amp;", "&") # properly encode url
				
				# open report
				report_browser = Watir::Browser.start("http://orii.health.gov.sk.ca" + report_url)
				# append report to array
				reports[municipality][location] << report_browser.html
				report_browser.close
				
			}
			
			
			# Save reports to disk
			# TODO: Pipe directly to parser
			reports[municipality][location].each { |report|
				File.open("reports/" + location.gsub("\xA0", " ").gsub("/", "-") + ".html", 'a') { |f|
					f.write(report)
				}	
			}
	
		rescue
			puts "Error: " + $!	
		end
}
browser.close
