import events_from_cal, re

def readfile(filename):
	with open(filename) as f:
		content = f.read().splitlines()
	return content

def parse_line(text):
	event_detail_regex = re.compile(r'''
		(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d) # start timestamp 2016-08-15T12:00:00-04:00 : 2016-08-15T12:30:00-04:00 : Read
		(-\d\d:\d\d) # timezone
		(\s:\s) # space
		(\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d) # end timestamp
		(-\d\d:\d\d) # timezone
		(\s:\s) # space
		([a-zA-Z0-9\s\/]+) # Event Title
		''', re.VERBOSE)
	mo = event_detail_regex.search(text)
	all_day_event_regex = re.compile(r'''
		(\d\d\d\d-\d\d-\d\d)
		(\s:\s) # space
		(\d\d\d\d-\d\d-\d\d)
		(\s:\s) # space
		([a-zA-Z0-9\s\/]+) # Event Title
		''',re.VERBOSE) # 2016-08-15 : 2016-08-16 : All-Day Long
	mo2 = all_day_event_regex.search(text)
	if mo2 is not None:
		return(mo2.group(1)+'T00:00:00', mo2.group(3)+'T00:00:00', mo2.group(5))
	
	if mo is not None:
		return (mo.group(1), mo.group(4), mo.group(7)) # return just the Event Title


def return_list(file):
	tmp_list = []
	try:
		f = readfile(file)
		for line in f:
			if line not in tmp_list:
				tmp_list.append(line)
	except:
		tmp_list = ['Error creating your list, check that this file exists: '+file, 'check the misc/ folder for an example '+file]
		print('error creating your list. '+file+' probably does not exist... returning a dummy list')
	return tmp_list

def update_cal():
	try:
		events_from_cal.main()
		print('Calendar Updated')
	except:
		print('Error updating calendar... Hopefully it will be fixed by the next update')
