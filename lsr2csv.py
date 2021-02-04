#!/usr/bin/env python3
# parse listener logfile
# base on d.py received from R.Tobias
# 1.0 T.Liebscher

import re
import csv
import argparse
import os
import sys
from datetime import datetime

# Pattern dict
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
# create an output line
def match_line(line):
	object_dict = {}
	for key in pattern_dict:
		try:
			object_dict[key] = re.search(pattern_dict[key], line)[1]
		except Exception as e:
			print(e)
	return object_dict


def match_date(myDate):
    try:
        # we only have a date? 
        if len(myDate.split(' ')) == 1:
            try:
                # return date object in form "DD-MM-YYY"
                myDObj = datetime.strptime(myDate, '%d-%b-%Y')
                return(myDObj)
            except Exception as ie:
                print("Error dateonly :", ie)
                print("For date only please provide date in the format 'DD-Mon-YYYY'")
                return(False)
        elif len(myDate.split(' ')) == 2:
            try:
                # try to split the time based on the : (string -1 to remove a may ending : e.g.: 04: = 04)
                if len(myDate.split(' ')[1][:-1].split(':')) == 1:
                    # return date object in form "DD-MM-YYY HH24"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:')
                    return(myDObj)
                elif len(myDate.split(' ')[1][:-1].split(':')) == 2:
                    # return date object in form "DD-MM-YYY HH24:MI"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:')
                    return(myDObj)
                elif len(myDate.split(' ')[1][:-1].split(':')) == 3:
                    # return date object in form "DD-MM-YYY HH24:MI:SS"
                    try:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:%S')
                    except ValueError:
                        myDObj = datetime.strptime(myDate, '%d-%b-%Y %H:%M:%S:')
                    return(myDObj)
            except Exception as ie:
                print("Error date-time :", ie)
                print("Date-Time format should be in the format:")
                print("   -> 'DD-Mon-YYYY HH24'")
                print("   -> 'DD-Mon-YYYY HH24:MI'")
                print("   -> 'DD-Mon-YYYY HH24:MI:SS'")
                return(False)
        else:
            print("Date not recognized")
            return(False)

    except Exception as oe:
        print("No date string given I suppose:", oe)
        return(False)
			
#Commandline ARGS
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="listener log file")
ap.add_argument("-o", "--output", required=True,
	help="output file")
ap.add_argument("-bt", "--begin_time", required=False,
	help="Begin time in the format of 'DD-Mon-YYYY HH24:MI:SS'")
ap.add_argument("-et", "--end_time", required=False,
	help="End time in the format of 'DD-Mon-YYYY HH24:MI:SS'")
args = ap.parse_args()

btObj = False
etObj = False
# check for a valid begin time
if args.begin_time:
	# try to match begin time to a datetime object
	btObj = match_date(args.begin_time.upper())
	if not btObj:
		print("could not recognize Begin Time:", args.begin_time.upper())
		sys.exit(99)
# check for a valid end time
if args.end_time:
	# try to match end time to a datetime object
	etObj = match_date(args.end_time.upper())
	if not etObj:
		print("could not recognize End Time:", args.end_time.upper())
		sys.exit(99)
	# tsss end time smaller than begin 
	if btObj:
		if etObj < btObj:
			print("Oups - guess You made a typo, End Time should be greather than Begin Time")
			sys.exit(99)

# set a variable for time based processing
# 0 no time, 1 only begin, 2 only end, 3 begin and end
if args.begin_time and not args.end_time:
	checkTime = 1
elif not args.begin_time and args.end_time:
	checkTime = 2
elif args.begin_time and args.end_time:
	checkTime = 3
else:
	checkTime = 0

# if we cannot find the input file we shall go out
if not os.path.isfile(args.input):
	print("Input file %s not found" % (args.input))
	sys.exit(99)

# if an error catch it ...
try:
	fOut = open(args.output, 'w', newline='')
	# do we got a file handle
	if fOut:
		# for some stats
		cntOut = 0
		# the field names we want to have in the CSV
		fieldnames = ['Connection Time', 'HOSTNAME', 'IP', 'PROGRAM', 'SERVICE_NAME', 'ERROR', 'OS_USER', 'PROTOCOL', 'PORT']
		# init the csv object
		csvWriter = csv.DictWriter(fOut, fieldnames=fieldnames)
		# write a header 
		csvWriter.writeheader()
	else:
		# hmm could not open output file
		print("Looks like I cannot open output file %s" % (args.output))
		sys.exit(99)
	# just say something that we are working on the file
	print("Please wait processing ...")
	# try to open the input file
	with open(args.input, 'r') as fIn:
		cntIn = 0
		# for all lines in the file do
		for lineIn in fIn:
			# just some statistics :-)
			cntIn +=1
			process_line = 0
			# time based?
			# only begin time
			if checkTime == 1:
				try:
					# get the date time from the line 
					ltObj = re.search(pattern_dict['Connection Time'], lineIn)[1]
					ltObj = datetime.strptime(ltObj, '%d-%b-%Y %H:%M:%S')
					# is it in time range
					if ltObj >= btObj:
						process_line = 1
					else:
						process_line = 0
				except TypeError as e:
					print("Error processing line: %i %s" % (cntIn, e) )
			# only end time
			elif checkTime == 2:
				try:
					# get the date time from the line 
					ltObj = re.search(pattern_dict['Connection Time'], lineIn)[1]
					ltObj = datetime.strptime(ltObj, '%d-%b-%Y %H:%M:%S')
					# is it in time range
					if ltObj <= etObj:
						process_line = 1
					else:
						process_line = 0
				except TypeError as e:
					print("Error processing line: %i %s" % (cntIn, e) )
			# begin and end time
			elif checkTime == 3:
				try:
					# get the date time from the line 
					ltObj = re.search(pattern_dict['Connection Time'], lineIn)[1]
					ltObj = datetime.strptime(ltObj, '%d-%b-%Y %H:%M:%S')
					# is it in time range
					if ltObj >= btObj and ltObj <= etObj :
						process_line = 1
					else:
						process_line = 0
				except TypeError as e:
					print("Error processing line: %i %s" % (cntIn, e) )
			# not time based
			else:
				process_line = 1
			
			if process_line == 1:
				# do we have establish in the line
				if 'establish' in lineIn.lower():
					cntOut +=1
					# split the line
					lineOut = match_line(lineIn)
					# and write it out
					csvWriter.writerow(lineOut)
# ... and print a message that we got an error
except Exception as e:
	print("Got an error with the file operation!")
	print(e)
# and close the files in case they are open
finally:
	if fIn:
		fIn.close()
	if fOut:
		fOut.close()

print("Number of lines processed :", cntIn)
print("lines written to outfile  :", cntOut)
