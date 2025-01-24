import urllib.request as req
import json
import re
import csv

src_spot="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src_mrt="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with req.urlopen(src_spot) as res_spot:	
	data_spot = json.load(res_spot)
with req.urlopen(src_mrt) as res_mrt:	
	data_mrt = json.load(res_mrt)

spots_list = data_spot["data"]["results"]
stations_list = data_mrt["data"]


#在csv一一寫入(title, dist, longitude, latitude, first_img) 格式的資料

data_to_write = []

for spot in spots_list:
	title = spot["stitle"]
	spot_serial_num = spot["SERIAL_NO"]
	longitude = spot["longitude"]
	latitude = spot["latitude"]
	img = spot["filelist"]
	
	rule = re.compile(r'jpg', flags=re.I)
	the_jpg = rule.search(img) 
	jpg_index = img.find(the_jpg.group()) 
	first_img = img[0:jpg_index+3]
	
	for station in stations_list:
		if(spot_serial_num == station["SERIAL_NO"]):
			for i in range(len(stations_list)):
				if station["SERIAL_NO"] in stations_list[i].values():
					dist=stations_list[i]["address"][5:8]

	data_to_write.append([title, dist, longitude, latitude, first_img])

with open("spot.csv", mode="w", newline="") as spot_file:
	writer = csv.writer(spot_file)
	
	for row in data_to_write:
		writer.writerow(row)


#put spots at same mrt station into groups

spot_mrt = {}

for spot in spots_list:
	title = spot["stitle"]
	spot_snum = spot["SERIAL_NO"]

	for station in stations_list:
		if spot_snum == station["SERIAL_NO"]:
			station = station["MRT"]
			spot_mrt[title] = station 

grouped_dict = {}
for key, value in spot_mrt.items():
    if value not in grouped_dict:
        grouped_dict[value] = [key]
    else:
        grouped_dict[value].append(key)	

with open("mrt.csv", mode="w", newline="") as spot_file:
	writer = csv.writer(spot_file)
	for key, value_list in grouped_dict.items():
		single_row = [key]
		for value in value_list: 
			single_row.append(value)
		writer.writerow(single_row)

