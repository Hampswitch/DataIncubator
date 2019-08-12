import pandas
import pickle
import os


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

data=pandas.read_csv("data/Apr 2016 Trips.rpt",delimiter="|")

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

#incomplete