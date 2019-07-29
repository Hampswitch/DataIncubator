import pandas
import numpy
from sklearn.linear_model import LinearRegression

pandas.set_option("display.precision",10)

data=pandas.read_csv("data/Parking_Citations.csv",
dtype={'Citation':numpy.int64, 'Tag':str, 'ExpMM':str,
                                                         'ExpYY':str, 'State':str, 'Make':str, 'Address':str,
       'ViolCode':numpy.int32, 'Description':str, 'ViolFine':numpy.float32, 'ViolDate':str, 'Balance':numpy.float32,
       'PenaltyDate':str, 'OpenFine':numpy.float32, 'OpenPenalty':numpy.float32, 'NoticeDate':str,
       'ImportDate':str, 'Neighborhood':str, 'PoliceDistrict':str, 'CouncilDistrict':str,
       'Location':str})

# Q For all citations, what is the mean violation fine?
print("Q1")
print("{:.12}".format(data["ViolFine"].mean()))
# Q Looking only at vehicles that have open penalty fees, what dollar amount is the 81st percentile of that group?
print("Q2")
openpenaltydata=data[data["OpenPenalty"]>0]["OpenPenalty"].sort_values()
print(openpenaltydata.values[int(len(openpenaltydata)*.81)])
# Q Find the police district that has the highest mean violation fine. What is that mean violation fine?
#     Keep in mind that Baltimore is divided into nine police districts, so clean the data accordingly.
print("Q3")
districtmap={'Eastern':'Eastern', 'Western':'Western', 'Northern':'Northern', 'Central':'Central', 'Southeastern':'Southeastern',
       'Notheastern':'Northeastern', 'Northwestern':'Northwestern', 'NORTHERN':'Northern', 'Southern':'Southern', 'SOUTHERN':'Southern',
       'Southwestern':'Southwestern', 'SOUTHWESTERN':'Southwestern', 'SOUTHEASTERN':'Southeastern', 'CENTRAL':'Central',
       'WESTERN':'Western', 'EASTERN':'Eastern', 'NORTHWESTERN':'Northwestern', 'NORTHEASTERN':'Northeastern','NORTHEAST':'Northeastern',
       'NORTHWEST':'Northwestern','SOUTHEAST':'Southeastern','SOUTHWEST':'Southwestern'}
data["PoliceDistrict"]=data["PoliceDistrict"].map(districtmap)
print(data.groupby("PoliceDistrict")["ViolFine"].mean())
# Q Find the ten vehicle makes that received the most citations during 2017. For those top ten, find all
#     Japanese-made vehicles. What proportion of all citations were written for those vehicles? Note that the
#     naming in Make is not consistent over the whole dataset, so you will need to clean the data before calculating
#     your answer. Your answer should be expressed as a decimal number (i.e. 0.42, not 42).
print("Q4")
makemap={"Ford":["FORD","FOR","F0RD","4FORD","FORD3"],
         "Honda":["HOND","HONDA","HON","HONA","MONDA","HOMDA","HODNA","HODA","HND","HN","HHOND","H0NDA","GONDA"],
         "Toyota":["TOYT","TOYOT","TOY","TOYO","TOYA","TOTY","TOYP","TAOTA""TYT","TAOT","TOYTD","TOYTA","TOYT0"],
         "Chevrolet":["CHEV","CHEVR","CHE","CHEVY","CHEVV","CHVY","CHEVS","CHEVE","CHER","CHE2V","C4HEV"],
         "Nissan":["NISS","NISSA","NIS","NISN","NI","NISSN","NISS4","NISA"],
         "Jeep":["JEEP","JEE","JEP","JE","JEEPS"],
         "Hyundai":["HYUN","HYUND","HYU","HYD","HY","4HYUN","HYN","Hyund","HYUN4","HYND"],
         "Dodge":["DODG","DODGE","DOD"],
         "BMW":["BMW","BMW.","BMW (","BMW 7","BWW","BMN","BMV","DMW"],
         "Kia":["KIA","KIA M","KIA."],
         "Acura":["ACUR","ACURA","ACU","ACUA"],
         "Volkswagon":["VOLKS","VOLK","VW","V W","VLK","VW.","VLW","VOLW","VOLKW","VOKS"],
         "Chrysler":["CHRY","CHRYS","CHR","CHYR","CHY","CRYS","CHYRS"],
         "GMC":["GMC","GMC (","GMC.","GMC U","GMC S"],
         "Lexus":["LEXUS","LEXS","LEXU","LEX","LEXY","LEXSU"],
         "Mazda":["MAZDA","MAZD","MAZ","MAZA","MADZ","MAZEA","MAZD7","MAZD0","MAZAD","MAXDA"],
         "Mercedes-Benz":["MERZ","MERCE","MERC","MER","BENZ","MERZB","MERZ4","MERB"],
         "Buick":["BUIC","BUICK","BUI","BUCI","BUIK"],
         "Audi":["AUDI","AUD","AUID","AYDI","JAUDI"],
         "Subaru":["SUBAR","SUBA","SUB","SUBU","SUBUR"],
         "Cadillac":["CADI","CADIL","CAD","CADL"],
         "Infiniti":["INFI","INFIN","INF"],
         "Volvo":["VOLVO","VOLV","VLV","VOL","VOLO","VO","VOVL","VOLV4","VOV"],
         "Lincoln":["LINC","LINCO","LIN","LINCL","LINCN"],
         "Mitsubishi":["MITS","MITSU","MIT"],
         "Mercury":["MERCU","MECUR"],
         "Pontiac":["PONTI","PONT","PONI","PON"],
         "Saturn":["SATUR","STRN","SATU","SATR","SAT","SATN","SATUN","SAT4U"],
         "Oldsmobile":["OLDS","OLDSM","OLD","0LDS"],
         "Scion":["SCION","SCIO"],
         "Mini":["MINI-","MINI","MNNI","MIN"],
         "Ram":["RAM"],
         "Landrover":["LAND","LNDR","ROV","LANDR","LND","LANR","ROVR","LAN","LR","LANRO","ROVE","LDRO","LDRV","LNRV","LNRO"],
         "Plymouth":["PLYM","PLYMO","PLY"],
         "Saab":["SAAB","SAA","SABB","SAB"],
         "Freight":["FREIG","FRHT","FREIT","FREI","FRIEG","FRT","FRIGH","FRGT","FRGHT"],
         "Jaguar":["JAGU","JAGUA","JAQU","JAG","JAQUA","JAQ","JAQUR","JAGR"],
         "Fiat":["FIAT","FAIT"],
         "Suzuki":["SUZUK","SUZI","SUZU","SUZ","SUZK","SUZKI","SUSK","SUK","SUZUI","SUZIK","SUKI"],
         "Isuzu":["ISUZU","ISU","ISUZ","ISZU","ISUS","IZUZU"],
         "Porsche":["PORSC","PORS","PORSH"],
         "Yamaha":["YAMAH","YAMA","YAM"]}

for make in makemap.keys():
    data.loc[data["Make"].isin(makemap[make]),"Make"]=make

print(data.groupby("Make").count().sort_values("Citation")["Citation"])
japanese=["Acura","Nissan","Toyota","Honda"] # Hyundai is Korean

print(float(data[data["Make"].isin(japanese)].count()["Citation"])/data.count()["Citation"])

# Q First, find the total number of citations given in each year between 2004 and 2014 (inclusive). Next, using linear
#     regression, create a function that plots the total number of citations as a function of the year. If you were to
#     plot a line using this function, what would be the slope of that line?
print("Q5")
data["ViolYear"]=data["ViolDate"].str.slice(6,10)
rdata=data[data["ViolYear"].isin(["2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014"])].groupby("ViolYear")["Citation"].count()
model=LinearRegression().fit(rdata.index.astype(numpy.int32).values.reshape(-1,1),rdata.values)
print(model.coef_)
# Q First, determine how many instances of auto theft ocurred in each police district during 2015. Next, determine the
#     number of parking citations that were issued in each police district during the same year. Finally, determine
#     the ratio of auto thefts to parking citations for each district. Out of the nine police districts, what was
#     the highest ratio?
print("Q6")
citations=data[data["ViolYear"]=="2015"].groupby("PoliceDistrict").count()["Citation"]
crimedata=pandas.read_csv("data/BPD_Part_1_Victim_Based_Crime_Data.csv")
crimedata["District"]=crimedata["District"].map(districtmap)
crimedata["CrimeYear"]=crimedata["CrimeDate"].str.slice(6,10)
thefts=crimedata[(crimedata["Description"]=="AUTO THEFT") & (crimedata["CrimeYear"]=="2015")].groupby("District").count()["Total Incidents"]
print(thefts/citations)