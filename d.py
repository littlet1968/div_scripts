import re
import csv
import argparse

#Commandline ARGS
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="listener log file")
ap.add_argument("-o", "--output", required=True,
	help="output file")
args = ap.parse_args()

#Pattern dict
pattern_dict = {
	'Connection Time' : r'(\d+\-\w+\-\d+\s*\d+\:\d+\:\d+)', 
	'HOSTNAME' : r'HOST=([^\)]*)', 
	'IP' : r'HOST=.*?HOST=(\d+\.\d+\.\d+\.\d+)', 
	'PROGRAM' : r'PROGRAM\=([^\)]*)', 
	'SERVICE_NAME' : r'([^\s]+)\s+\*?\s+\d+$', 
	'ERROR' : r'(?<=\*)\s+(\d+)$', 
	'OS_USER' : r'USER=([^\)]*)', 
	'PROTOCOL' : r'PROTOCOL=([^\)]*)', 
	'PORT' : r'PORT=([^\)]*)'
}

def match_line(line):
	object_dict = {}
	for key in pattern_dict:
		try:
			object_dict[key] = re.search(pattern_dict[key], line)[1]
		except Exception as e:
			print(e)
	return object_dict
	
# Make sure file gets closed after being iterated
with open(args.input, 'r') as f:
   # Read the file contents and generate a list with each line
   lines = f.readlines()

# Iterate each line
connectObjectArray = []
for line in lines:
	if 'establish' in line.lower():
		connectObjectArray.append(match_line(line))

with open(args.output, 'w', newline='') as f:
	fieldnames = ['Connection Time', 'HOSTNAME', 'IP', 'PROGRAM', 'SERVICE_NAME', 'ERROR', 'OS_USER', 'PROTOCOL', 'PORT']

	csvWriter = csv.DictWriter(f, fieldnames=fieldnames)
	csvWriter.writeheader()
	for object in connectObjectArray:
		print(object)
		csvWriter.writerow(object)