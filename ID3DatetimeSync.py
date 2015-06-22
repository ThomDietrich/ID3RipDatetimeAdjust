#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TXXX
import datetime
import win32file
import win32con
from datetime import timedelta, datetime, tzinfo
from colorama import Fore, Back, Style
from colorama import init as coloramainit
coloramainit()



if (len(sys.argv) != 2 or not os.path.exists(sys.argv[1])):
	print "parameter missing!"
	print "this script takes one path to a folder with MP3s as command line parameter"
	print ""
	print "https://github.com/ThomDietrich/ID3RipDatetimeAdjust"
	sys.exit()
path = os.path.abspath(sys.argv[1].rstrip('\\'))



def getMP3Files(path):
	files = []
	for entry in os.listdir(path):
		filepath = path + os.sep + entry
		if os.path.isfile(filepath):
			#print entry
			if os.path.splitext(filepath)[1][1:].strip().lower() == "mp3":
				files.append(filepath)
	return files



def getDatetimeFileCreated(filepath):
	t = os.path.getctime(filepath)
	t = datetime.fromtimestamp(t)
	t = t.replace(microsecond = 0)
	return t



def setDatetimeFileCMA(filepath, timestamp):
	#we need to correct summer saving time
	#dirty workaround, does the job...
	d = datetime(timestamp.year, 4, 1)   # DST starts last Sunday in March
	dstOn = d - timedelta(days=d.weekday() + 1) 
	d = datetime(timestamp.year, 11, 1) # DST ends last Sunday in October
	dstOff = d - timedelta(days=d.weekday() + 1)
	if (dstOn <=  timestamp.replace(tzinfo=None) < dstOff):
		#timestamp inside summer saving time
		#print timedelta(hours=1)
		pass
	else:
		#print timedelta(0)
		timestamp = timestamp + timedelta(hours=1)
	handle = win32file.CreateFile(filepath, win32con.GENERIC_WRITE, 0, None, win32con.OPEN_EXISTING, 0, None)
	win32file.SetFileTime(handle, timestamp, timestamp, timestamp)
	handle.close()



def getDatetimeID3(filepath):
	audiofile = ID3(filepath)
	txxx = audiofile.getall('TXXX')
	if not len(txxx):
		print "No TXXX tag"
		return 0
	print txxx
	ripdate = str(txxx[0])
	try:
		d = datetime.strptime(ripdate, "%Y-%m-%d")
		d = date.replace(second = 1)
		return d
	except ValueError as e:
		print "Error TXXX tag contains no valid date: " + str(e)
		return 0



for file in reversed(getMP3Files(path)):
	print Style.BRIGHT + "\n" + "-"*50 + Style.RESET_ALL
	print file
	
	datetimeID3 = getDatetimeID3(file)
	datetimeFileCreated = getDatetimeFileCreated(file)
	print "ID3:\t\t" + str(datetimeID3)
	print "FileCreate:\t" + str(datetimeFileCreated)
	
	# if (datetimeID3 and datetimeFileCreated):
		# print "--> elected:\t" + str(datetimeExif)
		# #if (datetimeExif == datetimeFilename): #...because we are not in a perfect world
		# if ((datetimeFilename - timedelta(seconds=30)) < datetimeExif < (datetimeFilename + timedelta(seconds=30))):
			# if (datetimeExif == datetimeFileCreated):
				# #print "case 0: EXIF Photo.DateTimeOriginal, filename timestamp and file creation date match"
				# print Fore.GREEN + "nothing to do here." + Style.RESET_ALL
			# else: 
				# print "case 1: EXIF Photo.DateTimeOriginal and filename timestamp match"
				# print Fore.CYAN + "correcting file creation date..." + Style.RESET_ALL
				# setDatetimeFileCMA(file, datetimeExif)
		# else:
			# print "case 2: EXIF Photo.DateTimeOriginal and filename timestamp are different"
			# print Fore.RED + "manual correction needed!" + Style.RESET_ALL
			# print "continue?", raw_input()
	# elif (datetimeExif and not datetimeFilename):
		# print "--> elected:\t" + str(datetimeExif)
		# if (datetimeExif == datetimeFileCreated):
			# print "case 3: EXIF Photo.DateTimeOriginal and file creation date match"
			# print Fore.CYAN + "correcting filename timestamp..." + Style.RESET_ALL
			# print "continue?", raw_input()
			# renameFilenameDatetime(file, datetimeExif)
		# else:
			# print "case 4: EXIF Photo.DateTimeOriginal found"
			# print Fore.CYAN + "correcting file creation date..." + Style.RESET_ALL
			# print Fore.CYAN + "correcting filename timestamp..." + Style.RESET_ALL
			# print "continue?", raw_input()
			# setDatetimeFileCMA(file, datetimeExif)
			# renameFilenameDatetime(file, datetimeExif)
	# elif (not datetimeExif and datetimeFilename):
		# print "--> elected:\t" + str(datetimeFilename)
		# if (datetimeFilename == datetimeFileCreated):
			# print "case 5: filename timestamp and file creation date match"
			# print Fore.CYAN + "correction EXIF Photo.DateTimeOriginal..." + Style.RESET_ALL
			# print "continue?", raw_input()
			# setDatetimeExif(file, datetimeFilename)
		# else:
			# print "case 6: filename timestamp found"
			# print Fore.CYAN + "correction EXIF Photo.DateTimeOriginal..." + Style.RESET_ALL
			# print Fore.CYAN + "correcting file creation date..." + Style.RESET_ALL
			# print "continue?", raw_input()
			# setDatetimeExif(file, datetimeFilename)
			# setDatetimeFileCMA(file, datetimeFilename)
	# else:
		# print Fore.RED + "no clue... try yourself" + Style.RESET_ALL
		# print "(go set the filename, than tickle me again)"
		# print "continue?", raw_input()




