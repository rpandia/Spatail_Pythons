import arcpy
import sys
import datetime

#Taking Inputs(1 - 10)
cachefolder = sys.argv[1]
if cachefolder == '#' or not cachefolder:
	print "No cache folder given!"
	sys.exit()

mode = sys.argv[2]
if mode == '#' or not mode:
	mode = "RECREATE_ALL_TILES"

cacheName = sys.argv[3]
if cacheName == '#' or not cacheName:
	cacheName = "Test"

dataSource = sys.argv[4]
if dataSource == '#' or not dataSource:
	print "No Data Source given!"
	sys.exit()

method = sys.argv[5]
if method == '#' or not method:
	method = "IMPORT_SCHEME"

tilingScheme = sys.argv[6]
if tilingScheme == '#' or not tilingScheme:
	print "No TilingScheme(xml) given!"
	sys.exit()

scales = sys.argv[7]
if scales == '#' or not scales:
	scales = "16000;8000;4000;2000;1000"

areaofinterest = sys.argv[8]
if areaofinterest == '#' or not areaofinterest:
	areaofinterest = "#"

maxcellsize = sys.argv[9]
if maxcellsize == '#' or not maxcellsize:
	maxcellsize = "#"

mincachedscale = sys.argv[10]
if mincachedscale == '#' or not mincachedscale:
	mincachedscale = "8000"

maxcachedscale = sys.argv[11]
if maxcachedscale == '#' or not maxcachedscale:
	maxcachedscale = "2000"
#Intializing Staring Time
StTme = datetime.datetime.now()

#Running main script
arcpy.ManageTileCache_management(cachefolder, mode, cacheName, dataSource, method, tilingScheme,scales,areaofinterest, maxcellsize, mincachedscale, maxcachedscale)

#Intializing Ending Time
EdTme = datetime.datetime.now()

#finding the time difference
elapsedTime = EdTme - StTme

#Caluclating time difference in hh:mm:ss
hours = math.floor(elapsedTime / (60*60))
elapsedTime = elapsedTime - hours * (60*60);
minutes = math.floor(elapsedTime / 60)
elapsedTime = elapsedTime - minutes * (60);
seconds = math.floor(elapsedTime);
elapsedTime = elapsedTime - seconds;
ms = elapsedTime * 1000;

#printing the values
print("Processing Time:")
if(hours != 0):
	print ("%d hours %d minutes %d seconds" % (hours, minutes, seconds)) 
elif(minutes != 0):
	print ("%d minutes %d seconds" % (minutes, seconds))
else :
	print ("%d seconds %f ms" % (seconds, ms))
#Process completed!
print("Done")
"""---------------------------End---------------------------"""
