import pandas
import numpy
from sklearn.cluster import KMeans
from matplotlib import pyplot as plt

data=pandas.read_csv("E:/data/taxitrip_2016/CY 2016/Apr 2016 Trips.rpt",delimiter="|")

data["StartBlock"]=data["StartDateTime"].str.slice(0,15)
data["StartBlockTime"]=data["StartDateTime"].str.slice(11,15)

skdata=data[(data["OriginLatitude"]>35)&(data["OriginLatitude"]<45)&(data["OriginLongitude"]>-80)&(data["DestinationLongitude"]<-70)&(data["DestinationLatitude"]>35)&(data["DestinationLatitude"]<45)&(data["DestinationLongitude"]>-80)&(data["OriginLongitude"]<-70)][["OriginLatitude","OriginLongitude","DestinationLatitude","DestinationLongitude"]].dropna().values

kmeans=KMeans(n_clusters=16).fit(skdata)
print(kmeans.cluster_centers_)

clusters=[x for sublist in zip(kmeans.cluster_centers_[:,0:4:2],kmeans.cluster_centers_[:,1:4:2]) for x in sublist]

plt.plot(*clusters)
plt.xlim(38,42)
plt.ylim(-74,-78)
plt.title("Taxicab trip clusters")
plt.savefig("routes.png")

def counttrips(index,threshold=.001): # Default threshold is approx 100 meters
    sblock=data.iloc[index]["StartBlock"]
    olat=data.iloc[index]["OriginLatitude"]
    olong=data.iloc[index]["OriginLongitude"]
    dlat=data.iloc[index]["DestinationLatitude"]
    dlong=data.iloc[index]["DestinationLongitude"]
    if numpy.isnan(olat) or numpy.isnan(olong) or numpy.isnan(dlat) or numpy.isnan(dlong):
        raise ValueError("Selected index ({}) contains incomplete data".format(index))
    if olat<35 or olat>45 or dlat<35 or dlat>45 or olong<-80 or olong>-70 or dlong<-80 or dlong>-70:
        raise ValueError("Selected index ({}) falls outside target area".format(index))
    return data[(data["StartBlock"]==sblock)&(data["OriginLatitude"]>olat-threshold)&(data["OriginLatitude"]<olat+threshold)&
                (data["OriginLongitude"]>olong-threshold)&(data["DestinationLongitude"]<olong+threshold)&
                (data["DestinationLatitude"]>dlat-threshold)&(data["DestinationLatitude"]<dlat+threshold)&
                (data["DestinationLongitude"]>dlong-threshold)&(data["OriginLongitude"]<dlong+threshold)]["StartBlock"].count()

i=0
sbord={}
for h in range(24):
    for m in range(6):
        sbord["{:02d}:{}".format(h,m)]=i
        i=i+1

results=[0]*144

for i in range(10000):
    if i%100==0:
        print(i)
    try:
        results[sbord[data.iloc[i]["StartBlockTime"]]]+=counttrips(i)
    except (ValueError,TypeError,KeyError):
        pass

plt.figure()
plt.plot([x/6.0 for x in range(144)],results)
plt.xlabel("Time")
plt.ylabel("Number of Compatible Trips")
plt.savefig("CompatibleTrips.png")
