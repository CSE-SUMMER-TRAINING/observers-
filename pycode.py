import pandas as pd
import arabic_reshaper
def arabic(str):
    return arabic_reshaper.reshape(str)[::-1]
khalafawy="خلفاوي"
road_el_farag="روض الفرج"
professor="ا.د"
Adoctor="ا.م"
doctor="دكتور"
manager =  "رئيس لجنة"
observer = "ملاحظ"
monitor0= "مراقب دور"
datalist=[]
mp = {"professor":0,professor:0,Adoctor:1,doctor:2,"Adoctor":1,"doctor":2,"other":3,"road el farag":1 ,"khalafawy":0,road_el_farag:1,khalafawy:0}
class Task(object):
    def __init__(self,day = 0,building = 0,type = observer):
            self.day = day
            self.building = building
            self.type = type

    def select_day(self,d,m,y):
                self.day = d
                self.month = m
                self.year = y

    def print_info (self):
            print(arabic(f' {self.type} ، التكليف: {self.building} ، المينى:  {self.day} اليوم رقم : '))

    def task_place(self):
            return mp[self.building]
    def work_place(self):
            return self.building
        

class Monitor:
    def __init__(self,user_name = "unkhown", title = "employee", work_place = "college", branch = "main",max_days = 0):
        self.user_name = user_name
        self.title = title
        self.work_place = work_place
        self.branch = branch
        self.max_days = max_days
        self.task = []
        self.accupied_days = {
        }

    def append_task(self,new_task):
        self.task.append(new_task)

    def print_info(self):
        print()
        print(arabic("بيانات المكلف"))
        print(arabic( f"{self.user_name.capitalize()} الاسم:"))
        print(arabic(f'{self.title} المسمى الوظيفى:'))
        print(arabic(f'{self.work_place} مكان العمل:'))
        print(arabic(f'{self.branch} المبنى: '))
        print()
        print(arabic("التكليفات: "))

        for task in self.task:
            task.print_info()
        print()
        print('#'*20)
        print()
    def push_info(self,dt,cnt):
        numofworkdays=0
        for i in range(50):
            dt[cnt].append(" ")
            if i in self.accupied_days.keys():
                dt[cnt].append(self.accupied_days[i][1])
                numofworkdays+=1
            else: dt[cnt].append(" ")
        dt[cnt][4]=numofworkdays
        
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

def process_single_task(day,tsk,monitors,lst):

	if not monitors:return False

	try:
		if day.current_day() in monitors[lst[0]].accupied_days.keys() :
			return False
	except KeyError:
		pass

	monitors[lst[0]].accupied_days[day.current_day()] = [1,tsk.work_place()]

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
    for day in days:
        for i in range(1,day.observers()+1):
            tsk = Task(day.current_day(),day.work_place(),observer)
            ok = process_single_task(day, tsk, 
            employees[tsk.task_place()][3][1], 
            employees[tsk.task_place()][3][0])
            if ok:continue
            ok = process_single_task(day, tsk, 
            employees[(tsk.task_place()+1)%2][3][1], 
            employees[(tsk.task_place()+1)%2][3][0])
            if ok:continue
            return False

        for i in range(1,day.monitor()+1):

            tsk = Task(day.current_day(),day.work_place(),monitor0)
            
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

            tsk = Task(day.current_day(),day.work_place(),manager)
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
dataframe1 = pd.read_excel('arb.xlsx', na_values = "E",sheet_name='Sheet1')
lst=[]
col=["الاسم","المسمى الوظيفى","مكان العمل","المبنى","التكليف الحالي"]
for i in range(50):
    if(not i):
        col.append(" ")
        col.append(" ")
    else:
        col.append(f'يوم {i} وقت')
        col.append(f'يوم {i}')
lst.append(col)
for index, rows in dataframe1.iterrows():
    my_list =rows.values.tolist()
    lst.append(my_list)
for x in lst:
    if(x==lst[0]):continue
    monitors.append(Monitor(*x))

# Day(day number , number of observres , number of monitors,number of managers) needed for that day in total
day1 = Day(1,2,1,1,khalafawy)
day2 = Day(2,5,1,1,road_el_farag)
day3 = Day(3,4,1,1,khalafawy)

days.append(day1)
days.append(day2)
days.append(day3)

ok = process(monitors, days)
cnt=1
if not ok :
	print(arabic("عدد الموظفين غير كافى"))
else:
    for mon in monitors:
        mon.push_info(lst,cnt)
        mon.print_info()
        cnt=cnt+1
    dataframeout=pd.DataFrame(lst)
    dataframeout.to_excel("observer_output.xlsx")
