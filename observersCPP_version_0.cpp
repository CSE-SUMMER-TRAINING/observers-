#include<bits/stdc++.h>
#include<unordered_set>
#include<unordered_map>
#pragma GCC optimize("-Ofast")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,sse4.2,popcnt,abm,mmx,avx2,tune=native")
#pragma GCC optimize("-ffast-math")
#pragma GCC optimize("-funroll-loops")
#pragma GCC optimize("-funroll-all-loops,-fpeel-loops,-funswitch-loops")
#define _CRT_SECURE_NO_WARNINGS
#define IO ios_base::sync_with_stdio(0), cin.tie(0), cout.tie(0)
#define W  int g;  cin>>g; while(g--)
#define FIO freopen("input.txt","r",stdin);freopen("output.txt","w",stdout);
using namespace std;
typedef  long long  ll;
const long long N = 5e5 + 5, Mod = 1e9 + 7, INF = 1e16;
const double PI = 3.14159265;
ll gcd(ll a, ll b) { return a ? gcd(b % a, a) : b; }
ll lcm(ll a, ll b) { return a * b / gcd(a, b); }
#define sz(V) int(V.size())
const int dx[9] = { 0, 0, 1, -1, 1, 1, -1, -1,0 };
const int dy[9] = { 1, -1, 0, 0, -1, 1, 1, -1 ,0 };
class Task {
public:
	int hour = 0, minute = 0, dd = 0, mm = 0, yy = 0;
	string building = "main", type = "observer";//observer - monitor - manager
	Task() {};
	Task(int day, string b, string typ) {
		dd=day;
		building = b;
		type = typ;
	}
	void print_info() {
		cout <<"day " <<dd << " => " << building <<" "<<type<< endl;
	}
	string taskPlace() {
		return building;
	}
};
class Monitor {
private://title => [professor - Assistant doctor - doctor - assistant]
	string name = "unkhown", title = "employee", work_place = "college", branch = "main";
	vector<Task>tasks;
public:
	int max_days = 0;
	map <int,bool>accupied_days;
	Monitor() {};
	Monitor(string name, string title, string work_place, string branch, int max_days) {
		this->name = name;
		this->title = title;
		this->work_place = work_place;
		this->branch = branch;
		this->max_days = max_days;
	}
	void append_task(Task new_task) {
		tasks.push_back(new_task);
	}
	bool operator <(const Monitor tmp) const {
		return max_days < tmp.max_days;
	}
	void print_info() {
		cout << title <<" info: \n";
		cout << name << " " << title << " " << work_place << " " << branch << endl;
		cout << title<<" Tasks:\n";
		for (Task& tsk : tasks) {
			tsk.print_info();
		}
		cout<<"\n###########\n\n";
	}
	string workPlace() {
		return branch;
	}
	string Title() {
		return title;
	}
};
class Day {
private:
	int dd = 0,ob=0, mana=0,monit=0;
	string building;
public:
	Day() {};
	Day(int D,int obs,int man,int mont,string bul) {
		dd = D;
        ob=obs;
        mana=man;
        monit=mont;
        building=bul;
	}
	int current_day()
	{
	    return dd;
	}
    int observers()
    {
        return ob;
    }int managers()
	{
	    return mana;
	}int mont()
	{
	    return monit;
	}
    string place()
    {
        return building;
    }
};
string flip_palce(string cur) {
	return cur == "khalafawy" ? "road el farag" : "khalafawy";
}
bool process_single_task(Day d,Task tsk,vector<Monitor>&monitors,int &cur,int &avaiable_monitors) {
	if (monitors.empty())return false;
	if (monitors[cur].accupied_days[d.current_day()])
		return false;
	monitors[cur].accupied_days[d.current_day()] = 1;
	if (!monitors[cur].max_days) {
		avaiable_monitors = cur;
		cur = 0;
	}
	if (!avaiable_monitors)return false;
	monitors[cur].append_task(tsk);
	monitors[cur].max_days--;
	cur = (cur + 1) % avaiable_monitors;
	return true;
}
bool process(vector<Monitor>& monitors, vector<Day>& day) {
	sort(monitors.rbegin(), monitors.rend());
	map<string, map<string, pair<pair<int,int>,vector<Monitor>>>>empolyees;
	// spread monitors => [khalafawy - road el farag][professor -Adoctor -doctor - assistant]
	for (Monitor& monitor : monitors)
		empolyees[monitor.workPlace()][monitor.Title()].second.push_back(monitor);
	//for each vector => set inital cur and inital avalible monitors
	for (auto &i : empolyees)
		for (auto &j : i.second)
			j.second.first = { 0,sz(j.second.second) };//cur - avaliable
	bool done = 1, ok = 0;
	for (Day& d : day) {
                for(int i=1;i<=d.observers();i++)
                {
                    Task tsk(d.current_day(),d.place(),"observer");
                    ok = process_single_task(d, tsk, empolyees[tsk.taskPlace()]["assistant"].second, empolyees[tsk.taskPlace()]["assistant"].first.first, empolyees[tsk.taskPlace()]["assistant"].first.second);
                    if (ok)continue;
                    ok = process_single_task(d, tsk, empolyees[flip_palce(tsk.taskPlace())]["assistant"].second, empolyees[flip_palce(tsk.taskPlace())]["assistant"].first.first, empolyees[flip_palce(tsk.taskPlace())]["assistant"].first.second);
                    if (ok)continue;
                    return false;
                } for(int i=1;i<=d.mont();i++)
                {
                    Task tsk(d.current_day(),d.place(),"monitor");
                       ok = process_single_task(d, tsk, empolyees[tsk.taskPlace()]["doctor"].second, empolyees[tsk.taskPlace()]["doctor"].first.first, empolyees[tsk.taskPlace()]["doctor"].first.second);
                    if (ok)continue;
                    ok = process_single_task(d, tsk, empolyees[flip_palce(tsk.taskPlace())]["doctor"].second, empolyees[flip_palce(tsk.taskPlace())]["doctor"].first.first, empolyees[flip_palce(tsk.taskPlace())]["doctor"].first.second);
                    if (ok)continue;
                    return false;
                } for(int i=1;i<=d.managers();i++)
                {
                    Task tsk(d.current_day(),d.place(),"manager");
                       empolyees[tsk.taskPlace()]["professor"];
                    ok = process_single_task(d, tsk, empolyees[tsk.taskPlace()]["professor"].second, empolyees[tsk.taskPlace()]["professor"].first.first, empolyees[tsk.taskPlace()]["professor"].first.second);
                    if (ok)continue;
                    ok = process_single_task(d, tsk, empolyees[tsk.taskPlace()]["Adoctor"].second, empolyees[tsk.taskPlace()]["Adoctor"].first.first, empolyees[tsk.taskPlace()]["Adoctor"].first.second);
                    if (ok)continue;
                    ok = process_single_task(d, tsk, empolyees[tsk.taskPlace()]["doctor"].second, empolyees[tsk.taskPlace()]["doctor"].first.first, empolyees[tsk.taskPlace()]["doctor"].first.second);
                    if (ok)continue;
                    return false;
                }


	}
	monitors.clear();
	for (auto& i : empolyees)
		for (auto& j : i.second)
			for (auto& k : j.second.second)
				monitors.push_back(k);
	return true;
}
void solve() {
	vector<Monitor> monitors;
	vector<Day>day;
	//monitors input
	monitors.push_back(Monitor("ahmed", "doctor", "control", "road el farag", 5));
	monitors.push_back(Monitor("mohamed", "assistant", "control", "khalfawy", 3));
	monitors.push_back(Monitor("ali", "assistant", "control", "khalfawy", 1));
	monitors.push_back(Monitor("amr", "assistant", "control", "khalfawy", 7));
	monitors.push_back(Monitor("sameh", "assistant", "control", "road el farag", 2));
	monitors.push_back(Monitor("shady", "doctor", "control", "khalfawy", 3));
	monitors.push_back(Monitor("salem", "professor", "control", "road el farag", 3));
	monitors.push_back(Monitor("said", "professor", "control", "khalfawy", 3));
	//days inout
	//Day(day number , number of observres , number of monitors,number of managers) needed for that day in total
	Day day1(1,2,1,1,"khalfawy");
	Day day2(2,1,1,1,"road el farag");
	Day day3(3,3,1,1,"khalfawy");
	day.push_back(day1);
	day.push_back(day2);
	day.push_back(day3);
	//	day.push_back(day3);
	bool ok = process(monitors, day);
	if (!ok) {
		cout << "Monitors are not enough\n";
		return;
	}
	for (Monitor& mon : monitors) {
		mon.print_info();
	}
}
int main() {
	IO;
	solve();
	return 0;
}
