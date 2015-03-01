import math
from geopy.geocoders import GoogleV3
to_add=""
to_search=""
result_string=""
results=[]
fileopen = open("UK_Cities.txt","r")
filewrite = open("UK_Cities_coord.txt","w")
line = fileopen.readline()
geolocator= GoogleV3()
while line:
	to_add=line.rstrip('\n')
	to_search=to_add + " United Kingdom"
	location=geolocator.geocode(to_search,timeout=20)
	result_string= str(to_add) + "_" + str(location.latitude) + "_" + str(location.longitude) + "_"
	print(result_string)
	print(result_string, file=filewrite)
	line=fileopen.readline()
	#results.append(result_string)