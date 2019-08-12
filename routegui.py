apikey="Google maps api key"

import googlemaps
import datetime
import dateutil.parser
import pandas
import pickle
import os
import random
import numpy
from matplotlib import pyplot as plt
import tkinter as tk

sampletrips=[[ 38.9026, -77.0604,  38.9134, -77.0434],
       [ 38.9073, -77.0589,  38.9073, -77.0589],
       [ 38.9083, -77.0427,  38.9211, -77.0437],
       [ 38.9206, -77.0715,  38.9308, -77.0728],
       [ 38.9079, -77.0424,  38.8952, -77.0731],
       [ 38.9114, -77.0319,  38.9417, -77.0619],
       [ 38.9025, -77.0338,  38.9023, -77.0441],
       [ 38.917 , -77.0312,  38.9095, -77.0481],
       [ 38.9154, -77.0219,  38.9297, -77.0401],
       [ 38.9171, -77.031 ,  38.906 , -77.0638]]

samplestartdates=['2016-04-29 21:24:18.6066667 +00:00',
       '2016-04-29 21:07:20.5433333 +00:00',
       '2016-04-29 20:39:34.5000000 +00:00',
       '2016-04-29 20:01:54.3366667 +00:00',
       '2016-04-29 19:42:46.9266667 +00:00',
       '2016-04-29 19:23:52.1166667 +00:00',
       '2016-04-29 19:33:28.0133333 +00:00',
       '2016-04-29 16:20:59.4533333 +00:00',
       '2016-04-29 18:44:22.0433333 +00:00',
       '2016-04-29 17:58:14.8233333 +00:00']

i=0
#result=gmaps.directions((sampletrips[i][0],sampletrips[i][1]),(sampletrips[i][2],sampletrips[i][3]),mode="transit",departure_time=datetime.now())

def duration(route):
    return route[0]["legs"][0]["duration"]["value"]
    #return route[0]["legs"][0]["arrival_time"]["value"] - route[0]["legs"][0]["departure_time"]["value"]

def walkingdistance(route):
    total=0.0
    for leg in route[0]["legs"]:
        for step in leg["steps"]:
            if step["travel_mode"]=='WALKING':
                total=total+step["distance"]["value"]
    return total

def gettriptime(datetimestr):
    tripdatetime=dateutil.parser.parse(datetimestr)
    return datetime.datetime(2019,8,14+((tripdatetime.day+1)%7),tripdatetime.hour,tripdatetime.minute)

sampleresult=[{u'bounds': {u'northeast': {u'lat': 38.9134, u'lng': -77.0434405},   u'southwest': {u'lat': 38.9025723, u'lng': -77.0603995}},  u'copyrights': u'Map data \xa92019 Google',  u'legs': [{u'arrival_time': {u'text': u'6:53pm',     u'time_zone': u'America/New_York',     u'value': 1565218392},    u'departure_time': {u'text': u'6:28pm',     u'time_zone': u'America/New_York',     u'value': 1565216893},    u'distance': {u'text': u'1.7 mi', u'value': 2695},    u'duration': {u'text': u'25 mins', u'value': 1499},    u'end_address': u'1721 19th St NW, Washington, DC 20009, USA',    u'end_location': {u'lat': 38.9134, u'lng': -77.0434405},    u'start_address': u'1000 Thomas Jefferson St NW, Washington, DC 20007, USA',    u'start_location': {u'lat': 38.9025723, u'lng': -77.0603995},    u'steps': [{u'distance': {u'text': u'0.6 mi', u'value': 1021},      u'duration': {u'text': u'14 mins', u'value': 855},      u'end_location': {u'lat': 38.9105201, u'lng': -77.05896489999999},      u'html_instructions': u'Walk to Q St NW & 30th St NW',      u'polyline': {u'points': u'admlFnziuMA}@?kA?a@?wAM?_@?eDBeA@c@?aA@{@?sA@eA@m@@Y?[?m@@kB@c@?G?q@?w@@O?yA@iA@U?kB@c@@aA@Y?]@aBBS??Y?e@'},      u'start_location': {u'lat': 38.9025723, u'lng': -77.0603995},      u'steps': [{u'distance': {u'text': u'367 ft', u'value': 112},        u'duration': {u'text': u'1 min', u'value': 86},        u'end_location': {u'lat': 38.9025825, u'lng': -77.0591003},        u'html_instructions': u'Head <b>east</b> on <b>K St NW</b> toward <b>Thomas Jefferson St NW</b>',        u'polyline': {u'points': u'admlFnziuMA}@?kA?a@?wA'},        u'start_location': {u'lat': 38.9025723, u'lng': -77.0603995},        u'travel_mode': u'WALKING'},       {u'distance': {u'text': u'0.5 mi', u'value': 882},        u'duration': {u'text': u'12 mins', u'value': 747},        u'end_location': {u'lat': 38.9105169, u'lng': -77.0592775},        u'html_instructions': u'Turn <b>left</b> onto <b>30th St NW</b>',        u'maneuver': u'turn-left',        u'polyline': {u'points': u'cdmlFjriuMM?_@?eDBeA@c@?aA@{@?sA@eA@m@@Y?[?m@@kB@c@?G?q@?w@@O?yA@iA@U?kB@c@@aA@Y?]@aBBS?'},        u'start_location': {u'lat': 38.9025825, u'lng': -77.0591003},        u'travel_mode': u'WALKING'},       {u'distance': {u'text': u'89 ft', u'value': 27},        u'duration': {u'text': u'1 min', u'value': 22},        u'end_location': {u'lat': 38.9105201, u'lng': -77.05896489999999},        u'html_instructions': u'Turn <b>right</b> onto <b>Q St NW</b><div style="font-size:0.9em">Destination will be on the right</div>',        u'maneuver': u'turn-right',        u'polyline': {u'points': u'wunlFnsiuM?Y?e@'},        u'start_location': {u'lat': 38.9105169, u'lng': -77.0592775},        u'travel_mode': u'WALKING'}],      u'travel_mode': u'WALKING'},     {u'distance': {u'text': u'0.8 mi', u'value': 1321},      u'duration': {u'text': u'6 mins', u'value': 330},      u'end_location': {u'lat': 38.911105, u'lng': -77.044601},      u'html_instructions': u'Bus towards Dupont Circle',      u'polyline': {u'points': u'ounlFnqiuMG??KAsB?WA{A?_A?w@A_AAeFAaB?i@C[A{DCcF?I?U?u@Ao@?g@?KAK?MAIAIAICKAICKCKCKCIEKCIEIEIEIEGEGEGKMCCII@]?q@A{C?aB?AJ@G??]?W@]?g@?c@?U?YAc@?Q?UAc@?e@?i@?e@?O?SA?@o@?k@@o@?o@?m@?i@?i@?_@?E?I?[?E?G?ALk@Mj@?@B?'},      u'start_location': {u'lat': 38.910477, u'lng': -77.058964},      u'transit_details': {u'arrival_stop': {u'location': {u'lat': 38.911105,         u'lng': -77.044601},        u'name': u'Q St NW & Connecticut Ave NW'},       u'arrival_time': {u'text': u'6:48pm',        u'time_zone': u'America/New_York',        u'value': 1565218080},       u'departure_stop': {u'location': {u'lat': 38.910477,         u'lng': -77.058964},        u'name': u'Q St NW & 30th St NW'},       u'departure_time': {u'text': u'6:42pm',        u'time_zone': u'America/New_York',        u'value': 1565217750},       u'headsign': u'Dupont Circle',       u'line': {u'agencies': [{u'name': u'WMATA',          u'phone': u'1 (202) 637-7000',          u'url': u'http://www.wmata.com/'}],        u'short_name': u'D2',        u'vehicle': {u'icon': u'//maps.gstatic.com/mapfiles/transit/iw2/6/bus2.png',         u'name': u'Bus',         u'type': u'BUS'}},       u'num_stops': 5},      u'travel_mode': u'TRANSIT'},     {u'distance': {u'text': u'0.2 mi', u'value': 353},      u'duration': {u'text': u'5 mins', u'value': 283},      u'end_location': {u'lat': 38.9134, u'lng': -77.0434405},      u'html_instructions': u'Walk to 1721 19th St NW, Washington, DC 20009, USA',      u'polyline': {u'points': u'oynlFvwfuM?]AM?A?A?I?E?A?U?y@?cA@OS?aCAy@?wA@cAA{@?W?G?'},      u'start_location': {u'lat': 38.9111245, u'lng': -77.0446008},      u'steps': [{u'distance': {u'text': u'328 ft', u'value': 100},        u'duration': {u'text': u'2 mins', u'value': 92},        u'end_location': {u'lat': 38.91112210000001, u'lng': -77.0434473},        u'html_instructions': u'Head <b>east</b> on <b>Q St NW</b> toward <b>Connecticut Ave NW</b>',        u'polyline': {u'points': u'oynlFvwfuM?]AM?A?A?I?E?A?U?y@?cA@O'},        u'start_location': {u'lat': 38.9111245, u'lng': -77.0446008},        u'travel_mode': u'WALKING'},       {u'distance': {u'text': u'0.2 mi', u'value': 253},        u'duration': {u'text': u'3 mins', u'value': 191},        u'end_location': {u'lat': 38.9134, u'lng': -77.0434405},        u'html_instructions': u'Turn <b>left</b> onto <b>19th St NW</b><div style="font-size:0.9em">Destination will be on the right</div>',        u'maneuver': u'turn-left',        u'polyline': {u'points': u'oynlFppfuMS?aCAy@?wA@cAA{@?W?G?'},        u'start_location': {u'lat': 38.91112210000001, u'lng': -77.0434473},        u'travel_mode': u'WALKING'}],      u'travel_mode': u'WALKING'}],    u'traffic_speed_entry': [],    u'via_waypoint': []}], u'overview_polyline': {u'points': u'admlFnziuMAcGyGD_LFyKFkMLS??Y?e@F?G??KAkCCsGCgICeAE_MAyCEm@Kk@Qm@Ug@]e@MM@oAA}FJ?G??]?W@_CAeBAmF@sH?s@Lm@Ml@B?C??]AM?C?g@?}B@OS?{DA{C?{A?'}, u'summary': u'', u'warnings': [u'Walking directions are in beta. Use caution \u2013 This route may be missing sidewalks or pedestrian paths.'], u'waypoint_order': []}]

data=pandas.read_csv("data/Apr 2016 Trips.rpt",delimiter="|")

print("loaded")

data["StartBlock"]=data["StartDateTime"].str.slice(0,15)
data["StartBlockTime"]=data["StartDateTime"].str.slice(11,15)

data=data[(data["OriginLatitude"]>35)&(data["OriginLatitude"]<45)&(data["OriginLongitude"]>-80)&(data["DestinationLongitude"]<-70)&(data["DestinationLatitude"]>35)&(data["DestinationLatitude"]<45)&(data["DestinationLongitude"]>-80)&(data["OriginLongitude"]<-70)]

data["TransitTime"]=-1
data["TransitWalkingDistance"]=-1

if os.path.exists("routepickle.txt") and os.path.isfile("routepickle.txt"):
    f=open("routepickle.txt","r")
    routedict=pickle.load(f)
    f.close()
else:
    routedict={}

print("cleaned")

"""
gmaps=googlemaps.Client(key=apikey)

while len(routedict)<10000:
    i=random.randint(0,len(data)-1) # random sampling because the records might be sorted
    print(str(i))
    if not routedict.has_key(data.index[i]):
        try:
            route=gmaps.directions((data["OriginLatitude"][data.index[i]],data["OriginLongitude"][data.index[i]]),(data["DestinationLatitude"][data.index[i]],data["DestinationLongitude"][data.index[i]]),
                               mode="transit",departure_time=gettriptime(data["StartDateTime"][data.index[i]]))
            routedict[data.index[i]]=route
        except TypeError:
            pass


f=open("routepickle.txt","w")
pickle.dump(routedict,f)
f.close()
"""
for i in routedict.keys():
    try:
        if len(routedict[i])>0:
            data.at[i,"TransitTime"]=duration(routedict[i])
            data.at[i,"TransitWalkingDistance"]=walkingdistance(routedict[i])
        else:
            data.at[i,"TransitTime"] = -2
            data.at[i,"TransitWalkingDistance"] = -2
    except (KeyError,IndexError):
        print(i)
        print(routedict[i])
        raise

data["TripLatitude"]=(data["OriginLatitude"]+data["DestinationLatitude"])/2
data["TripLongitude"]=(data["OriginLongitude"]+data["DestinationLongitude"])/2

data["TransitEfficiency"]=data["Duration"]/data["TransitTime"]
data["TransitLoss"]=data["TransitTime"]-data["Duration"]

print("Data Load Complete")

data=data[data["TransitTime"]>0]

yrange=(38.8,39) # 35-45
xrange=(-77.1,-76.9) # -70 - -80
resolution=20
xbins=[xrange[0]+(xrange[1]-xrange[0])*i/float(resolution) for i in range(resolution+1)]
ybins=[yrange[0]+(yrange[1]-yrange[0])*i/float(resolution) for i in range(resolution+1)]

xcol="OriginLongitude"
ycol="OriginLatitude"
vcol="TransitTime" # Transit time, Transit Walking Distance, Duration

data["xbin"]=pandas.cut(data[xcol],xbins,labels=range(resolution))
data["ybin"]=pandas.cut(data[ycol],ybins,labels=range(resolution))

griddata=data.groupby(["xbin","ybin"])[vcol].mean()

grid=numpy.nan_to_num(griddata.unstack().values)
print(grid)

plt.imshow(grid)



class graphmaker(tk.Frame):
    def __init__(self,master):
        tk.Frame.__init__(self,master)
        tk.Button(self,text="Show Plot",command=self.mkplot).pack(side=tk.BOTTOM)
        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        l=tk.Label(f,text="Longitude Range")
        l.pack(side=tk.LEFT)
        self.xminvar=tk.DoubleVar()
        self.xminvar.set(-77.1)
        tk.Entry(f,textvariable=self.xminvar).pack(side=tk.LEFT)
        l = tk.Label(f, text="-")
        l.pack(side=tk.LEFT)
        self.xmaxvar = tk.DoubleVar()
        self.xmaxvar.set(-76.9)
        tk.Entry(f, textvariable=self.xmaxvar).pack(side=tk.LEFT)

        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        l = tk.Label(f, text="Latitude Range")
        l.pack(side=tk.LEFT)
        self.yminvar = tk.DoubleVar()
        self.yminvar.set(38.8)
        tk.Entry(f, textvariable=self.yminvar).pack(side=tk.LEFT)
        l = tk.Label(f, text="-")
        l.pack(side=tk.LEFT)
        self.ymaxvar = tk.DoubleVar()
        self.ymaxvar.set(39)
        tk.Entry(f, textvariable=self.ymaxvar).pack(side=tk.LEFT)

        f=tk.Frame(self)
        f.pack(side=tk.TOP)
        l = tk.Label(f, text="Resolution")
        l.pack(side=tk.LEFT)
        self.resvar = tk.IntVar()
        self.resvar.set(20)
        tk.Entry(f, textvariable=self.resvar).pack(side=tk.LEFT)

        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        l = tk.Label(f, text="Trip Position")
        l.pack(side=tk.LEFT)
        self.tripvar = tk.StringVar()
        self.tripvar.set("Average")
        tk.OptionMenu(f,self.tripvar,"Average","Origin","Destination").pack(side=tk.LEFT)

        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        l = tk.Label(f, text="Value")
        l.pack(side=tk.LEFT)
        self.valuevar = tk.StringVar()
        self.valuevar.set("TransitTime")
        tk.OptionMenu(f, self.valuevar, "TransitTime", "TransitWalkingDistance", "Duration","TransitEfficiency","TransitLoss").pack(side=tk.LEFT)

        f = tk.Frame(self)
        f.pack(side=tk.TOP)
        l = tk.Label(f, text="Aggregation")
        l.pack(side=tk.LEFT)
        self.aggvar = tk.StringVar()
        self.aggvar.set("Mean")
        tk.OptionMenu(f, self.aggvar, "Mean", "Count", "Median").pack(side=tk.LEFT)

    def mkplot(self):
        yrange = (self.yminvar.get(), self.ymaxvar.get())  # 35-45
        xrange = (self.xminvar.get(), self.xmaxvar.get())  # -70 - -80
        resolution = self.resvar.get()
        xbins = [xrange[0] + (xrange[1] - xrange[0]) * i / float(resolution) for i in range(resolution + 1)]
        ybins = [yrange[0] + (yrange[1] - yrange[0]) * i / float(resolution) for i in range(resolution + 1)]

        if self.tripvar.get()=="Origin":
            xcol="OriginLongitude"
            ycol="OriginLatitude"
        elif self.tripvar.get()=="Average":
            xcol = "TripLongitude"
            ycol = "TripLatitude"
        elif self.tripvar.get()=="Destination":
            xcol = "DestinationLongitude"
            ycol = "DestinationLatitude"
        else:
            raise ValueError("Unrecognized trip type value {}".format(self.tripvar.get()))
        vcol=self.valuevar.get()
        data["xbin"] = pandas.cut(data[xcol], xbins,labels=range(resolution))
        data["ybin"] = pandas.cut(data[ycol], ybins,labels=range(resolution))

        if self.aggvar.get()=="Mean":
            griddata=data.groupby(["xbin", "ybin"])[vcol].mean()
        elif self.aggvar.get()=="Median":
            griddata=data.groupby(["xbin", "ybin"])[vcol].median()
        elif self.aggvar.get()=="Count":
            griddata=data.groupby(["xbin", "ybin"])[vcol].count()
        else:
            raise ValueError("Unrecognized aggregation type {}".format(self.aggvar.get()))

        for i in range(resolution):
            for j in range(resolution):
                if (i,j) not in griddata.index:
                    griddata[(i,j)]=0.0

        grid = numpy.nan_to_num(griddata.unstack().values).transpose()
        plt.figure()
        plt.imshow(grid,origin="lower")
        plt.show()

plt.ion()
master=tk.Tk()
graphmaker(master).pack(side=tk.TOP)
tk.mainloop()