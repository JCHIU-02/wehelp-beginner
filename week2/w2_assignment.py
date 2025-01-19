#Task 1:
def find_and_print(messages, current_station):

    friend_loc = list(msg_short.values())
    dist_arr = []

    for friend_station in friend_loc:
        if current_station in main_line and friend_station in main_line:
            dist_arr.append(abs(main_line.index(current_station) - main_line.index(friend_station)))
        elif current_station == "Xiaobitan" and friend_station == "Xiaobitan":
            dist_arr.append(0)
        elif current_station == "Xiaobitan":
            dist_arr.append(abs(main_line.index(friend_station) - main_line.index("Qizhang")) + 1)
        else:
            dist_arr.append(abs(main_line.index(current_station) - main_line.index("Qizhang")) + 1)

    nearest = min(dist_arr)
    index_of_friend = dist_arr.index(nearest)
    nearest_friend = list(msg_short.keys())[index_of_friend]
    print(nearest_friend)


main_line = [
    "Songshan",
    "Nanjing Sanmin",
    "Taipei Arena",
    "Nanjing Fuxing",
    "Songjiang Nanjing",
    "Zhongshan",
    "Beimen",
    "Ximen",
    "Xiaonanmen",
    "Chiang Kai-Shek Memorial Hall",
    "Guting",
    "Taipower Building",
    "Gongguan",
    "Wanlong",
    "Jingmei",
    "Dapinglin",
    "Qizhang",
    "Xindian City Hall",
    "Xindian"
]

msg_short = {
    "Bob": "Ximen",
    "Mary": "Jingmei",
    "Copper": "Taipei Arena",
    "Leslie": "Xiaobitan",
    "Vivian": "Xindian"
}

messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}

find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian



#Task 2:
time_slot = {
    "John": list(range(24)),
    "Bob": list(range(24)),
    "Jenny": list(range(24))
}

def book(consultants, hour, duration, criteria):

    sorted_consultants = sorted(
            consultants, 
            key=lambda x: x['price'] if criteria == "price" else -x['rate']
        )
    user_appt = list(range(hour, hour + duration))
    found = False

    for consultant in sorted_consultants:
        reserved_cons = consultant['name']
        cons_slot = time_slot[reserved_cons]

        if all(h in cons_slot for h in user_appt):
            print(reserved_cons)

            for h in user_appt:
                cons_slot.remove(h)
            found = True
            break

    if not found:
        print("No Service")


consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]

book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John



#Task 3:
def func(*data):
    mid_name_list = []
        
    for name in data:
        if len(name) <= 3:
            mid_name = name[1]
        else:
            mid_name = name[2]
        mid_name_list.append(mid_name)
        
    unique = [char for char in mid_name_list if mid_name_list.count(char) == 1]
        
    if not unique:
        print("沒有")
    else:
        name_index = mid_name_list.index(unique[0])
        print(data[name_index])

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安



#Task 4:
def get_number(index):

    result = 0

    for num in range(1, index + 1):
        if num % 3 != 0:
            result += 4
        else:
            result -= 1

    print(result)

get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70
