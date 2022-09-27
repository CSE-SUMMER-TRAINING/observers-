from re import S
from operator import indexOf
from sre_compile import isstring
import string
from xmlrpc.client import DateTime
import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
import xlrd     
import openpyxl
# from asyncio import taskgroups
khalafawy=arabic_reshaper.reshape("خلفاوي")[::-1]
road_el_farag=arabic_reshaper.reshape("روض الفرج")[::-1]
professor=arabic_reshaper.reshape("ا.د")[::-1]
Adoctor=arabic_reshaper.reshape("ا.م")[::-1]
doctor=arabic_reshaper.reshape("دكتور")[::-1]
mp = {"professor":0,professor:0,Adoctor:1,doctor:2,"Adoctor":1,"doctor":2,"other":3,"road el farag":1 ,"khalafawy":0,road_el_farag:1,khalafawy:0}
class Task(object):
    def __init__(self,day = 0,building = 0,type = "observer"):
            self.day = day
            self.building = building
            self.type = type

    def select_day(self,d,m,y):
                self.day = d
                self.month = m
                self.year = y

    def print_info (self):
            print(f'-exam day {self.day} at {self.building} as {self.type}')

    def task_place(self):
            return mp[self.building]

class Monitor:
    def __init__(self,user_name = "unkhown", title = "employee", work_place = "college", branch = "main",max_days = 0):
        self.user_name = user_name
        self.title = title
        self.work_place = work_place
        self.branch = branch
        self.max_days = max_days
        self.task = []
        self.accupied_days = {}

    def append_task(self,new_task):
        self.task.append(new_task)

    def print_info(self):
        print()
        print("Monitor info: ")
        print(f'- UserName:{self.user_name.capitalize()}')
        print(f'- Job_title:{self.title}')
        print(f'- work_place:{self.work_place}')
        print(f'- branch:{self.branch}')
        print()
        print("Monitor Tasks:")

        for task in self.task:
            task.print_info()
        print()
        print('#'*20)
        print()
        
    def Work_place(self):
        return mp[self.branch]

    def Title(self):
        if(self.title in mp.keys()):return mp[self.title]
        return 3 

class Day:

	def __init__(self,day = 0,obs = 0,manager = 0,monit = 0,building = 0):
		self.day = day
		self.obs = obs
		self.manager = manager
		self.monit = monit
		self.building = building
	def current_day(self):
		return self.day

	def observers(self):
		return self.obs

	def Manager(self):
		return self.manager

	def monitor(self):
		return self.monit

	def work_place(self):
		return self.building


    # def append_task(self,new_task):
    #   new_task.select_day(self.d,self.m,self.y)
    #   self.task.append(new_task)

    # def current_day(self):
	# 	return (self.d,self.m,self.y)


def flip_place(cur):
	return "road el farag" if cur == "khalafawy" else "khalafawy"

def process_single_task(day,tsk,monitors,lst):

	if not monitors:return False

	try:
		if monitors[lst[0]].accupied_days[day.current_day()]:
			return False
	except KeyError:
		pass

	monitors[lst[0]].accupied_days[day.current_day()] = 1

	if not monitors[lst[0]].max_days:
		lst[1] = lst[0]
		lst[0] = 0

	if not lst[1]:return False
	monitors[lst[0]].append_task(tsk)
	monitors[lst[0]].max_days-=1
	lst[0] = (lst[0] + 1) % lst[1]

	return True

def process(monitors,days):

    monitors = sorted(monitors ,key = lambda monitor : monitor.max_days ,reverse = True)

    employees = {   
        0:{
            2:[[],[]],
            3:[[],[]],
            1:[[],[]],
            0:[[],[]],
        },
        1:{
            2:[[],[]],
            3:[[],[]],
            1:[[],[]],
            0:[[],[]],
        },
    }
    for monitor in monitors:
        employees[monitor.Work_place()][monitor.Title()][1].append(monitor)
    
    for i in employees:
        for j in employees[i]:
            employees[i][j][0] = [0,len(employees[i][j][1])]

    done , ok = 1 , 0
    # s=[0]
    for day in days:
        for i in range(1,day.observers()+1):
            tsk = Task(day.current_day(),day.work_place(),"observer")
            # print(tsk.task_place())
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][3][1], 
            employees[tsk.task_place()][3][0])
            if ok:continue
            # print(tsk.task_place())
            ok = process_single_task(day, tsk, 
            employees[(tsk.task_place()+1)%2][3][1], 
            employees[(tsk.task_place()+1)%2][3][0])
            if ok:continue
            return False

        for i in range(1,day.monitor()+1):

            tsk = Task(day.current_day(),day.work_place(),"monitor");
            
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][2][1], 
            employees[tsk.task_place()][2][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][1][1], 
            employees[tsk.task_place()][1][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][0][1], 
            employees[tsk.task_place()][0][0])
            if ok:continue
            return False

        for i in range(1,day.Manager()+1):

            tsk = Task(day.current_day(),day.work_place(),"manager")
            employees[tsk.task_place()][0]
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][0][1], 
            employees[tsk.task_place()][0][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][1][1], 
            employees[tsk.task_place()][1][0])
            if ok:continue
            
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][2][1], 
            employees[tsk.task_place()][2][0])
            if ok:continue
            return False

        monitors = []
        for i in employees:
            for j in employees[i]:
                for k in employees[i][j][1]:
                    monitors.append(k)
    return True

monitors , days = [],[]

# # monitors input
# monitors.append(Monitor("ahmed", "doctor", "control", "road el farag", 5))
# monitors.append(Monitor("mohamed", "other", "control", "khalafawy", 3))
# monitors.append(Monitor("ali", "other", "control", "khalafawy", 1))
# monitors.append(Monitor("amr", "other", "control", "khalafawy", 7))
# monitors.append(Monitor("sameh", "other", "control", "road el farag", 2))
# monitors.append(Monitor("shady", "doctor", "control", "khalafawy", 3))
# monitors.append(Monitor("salem", "professor", "control", "road el farag", 3))
# monitors.append(Monitor("said", "professor", "control", "khalafawy", 3))

dataframe1 = pd.read_excel('arb.xlsx', na_values = "E",sheet_name='Sheet1')
lst=[]
for index, rows in dataframe1.iterrows():
    # Create list for the current row
    my_list =rows.values.tolist()
    if(not isstring(my_list[0])):continue
    if( not (my_list[0][0]>='A' and my_list[0][0]<='z')):
        my_list[0]= arabic_reshaper.reshape(my_list[0])[::-1]
    if( not( my_list[1][0]>='A' and my_list[1][0]<='z')):
        my_list[1]= arabic_reshaper.reshape(my_list[1])[::-1]
    if( not(my_list[2][0]>='A' and my_list[2][0]<='z')):
        my_list[2]= arabic_reshaper.reshape(my_list[2])[::-1]
    if( not(my_list[3][0]>='A' and my_list[3][0]<='z')):
        my_list[3]= arabic_reshaper.reshape(my_list[3])[::-1]
    # #append the list to the final list
    lst.append(my_list)
# Print the list
for x in lst:
    monitors.append(Monitor(*x))
# [[],[]]
# days input
# Day(day number , number of observres , number of monitors,number of managers) needed for that day in total

day1 = Day(1,2,1,1,khalafawy)
day2 = Day(2,5,1,1,road_el_farag)
day3 = Day(3,4,1,1,khalafawy)

days.append(day1)
days.append(day2)
days.append(day3)


ok = process(monitors, days)

if not ok :
	print("Monitors are not enough\n")

else:
	for mon in monitors:
		mon.print_info()