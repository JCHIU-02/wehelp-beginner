import urllib.request as req
import json
import re
import csv

src_spot="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src_mrt="https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"

with req.urlopen(src_spot) as res_spot:	
	data_spot = json.load(res_spot) # json.load 可將JSON格式的資料轉換為Python的字典（dict）型別。
with req.urlopen(src_mrt) as res_mrt:	
	data_mrt = json.load(res_mrt)

spots_list = data_spot["data"]["results"] #撥開外層結構，得到想要的資料list #變數命名時可加上資料型別方便辨識
stations_list = data_mrt["data"]


#在csv一一寫入(title, dist, longitude, latitude, first_img) 格式的資料

data_to_write = []

for spot in spots_list: #把需要的資料一個個提取出來
	title = spot["stitle"]
	spot_serial_num = spot["SERIAL_NO"]
	longitude = spot["longitude"]
	latitude = spot["latitude"]
	img = spot["filelist"]
	
	rule = re.compile(r'jpg', flags=re.I)
	the_jpg = rule.search(img)   #如果有匹配，rule.search(img) 會返回一個「Match 物件」，其中包含匹配結果的詳細資訊（例如匹配的字串、開始和結束位置等）。
	jpg_index = img.find(the_jpg.group()) #group 將匹配結果的字傳從 Match object 中提取出來
	first_img = img[0:jpg_index+3]
	
	for station in stations_list:
		if(spot_serial_num == station["SERIAL_NO"]):
			for i in range(len(stations_list)):
				if station["SERIAL_NO"] in stations_list[i].values(): #尋找serial num在station list的index，再用這個index找到district
					dist=stations_list[i]["address"][5:8]

	data_to_write.append([title, dist, longitude, latitude, first_img])

with open("spot.csv", mode="w", newline="") as spot_file:  #create an object for reading or writing #with 通常用於開關檔案或連線，會自動關閉 after operations
	writer = csv.writer(spot_file) #".writer" is an object created from csv.writer() class
	
	for row in data_to_write:
		writer.writerow(row) #".writerow", a method of writer object


#put spots at same mrt station into groups

spot_mrt = {}

for spot in spots_list: #把需要的資料一個個提取出來
	title = spot["stitle"]
	spot_snum = spot["SERIAL_NO"]
	#print(title)
	for station in stations_list:
		if spot_snum == station["SERIAL_NO"]:
			station = station["MRT"]
			spot_mrt[title] = station 
#print(spot_mrt)

grouped_dict = {}
for key, value in spot_mrt.items():  #.items()會把dictionaty轉成這樣的view[(key1, value1),(key2, value2),(key3, value3)]。把鍵值段變成 tuples in a list
    if value not in grouped_dict:
        grouped_dict[value] = [key] #把spot_mrt的value轉為grouped_dict的key，grouped_dict key的value則為一個list，放入spot_mrt的key {mrt:[spot1 , spot2, spot3...]}
    else:
        grouped_dict[value].append(key) #如果value已經存在grouped_dict aka value已是grouped_dict的key，把當下的key放進 mrt 為 key 的 array 之中。		
#print(grouped_dict)

#把grouped_dict寫入csv
with open("mrt.csv", mode="w", newline="") as spot_file:  #create an object for reading or writing #with 通常用於開關檔案或連線，會自動關閉 after operations
	writer = csv.writer(spot_file)
	for key, value_list in grouped_dict.items():
		single_row = [key] #建立每次要寫入的內容，先放key
		for value in value_list: 
			single_row.append(value) #把value從value_list提取出來放進single_row
		writer.writerow(single_row) #只有第一行 with open 的行為會將檔案重置、清空

