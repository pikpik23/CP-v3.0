from tornado import Server
import TemplateAPI
from random import randint
import json

def dummy():
    print("Started")


def indexPage(response):
    response.write(TemplateAPI.render('Main_Page.html', response, {}))

def wikiPage(response):
    response.write(TemplateAPI.render('CMAP_Wiki.html', response, {}))

def randPage(response):
    response.write(str(rangen()))

#----- Training Pages --------
#For Cadets
def cdtTrainPage(response):
    response.write(TemplateAPI.render('Training_Cadets.html', response, {}))

def cdtTrainPageSig(response):
    response.write(TemplateAPI.render('Training_Cadets_Sig.html', response, {}))

def cdtTrainPageOps(response):
    response.write(TemplateAPI.render('Training_Cadets_Ops.html', response, {}))

def cdtTrainPageAdmin(response):
    response.write(TemplateAPI.render('Training_Cadets_Admin.html', response, {}))

def cdtTrainPageQstore(response):
    response.write(TemplateAPI.render('Training_Cadets_Q-Store.html', response, {}))

#For Cmaps   
def cmapTrainPage(response):
    response.write(TemplateAPI.render('Training_Cmaps.html', response, {}))
#------------------------------
def rangen():
    return randint(0, 10)
    
def inputPage(response):    
    response.write(TemplateAPI.render('input.html', response, {}))

def displayAllPage(response):
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_user(name, password)
    response.write(TemplateAPI.render('Track_Database.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))

def displayMapPage(response):
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_user(name, password)
    response.write(TemplateAPI.render('Track_Map.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))
    
def aboutPage(response):    
    response.write(TemplateAPI.render('About.html', response, {}))


def inputHandler(response):
    uuid = response.get_field("uuid")
    latitude = response.get_field("latitude")
    longitude = response.get_field("longitude")
    
    insertPositions(uuid, latitude, longitude)

def insertAssignments(response):
    uuid = response.get_field("uuid")
    pas = response.get_field("pass")
    name = response.get_field("name")
    typ = response.get_field("typ")

    cur = con.cursor()
    cur.execute("""
INSERT OR REPLACE INTO Assignments (UUID, IsVehicle, Name) 
  VALUES (  ?, 
            ?,
            ?
          );
    """, (uuid, typ == "1", name,))
    con.commit()
    cur.close()
    response.redirect("/assignments")

def showAllDebugPage(response):
    data = getLocations(100)
    response.write(TemplateAPI.render('display.html', response, {'data': data}))
    print(data)

def getAssignments():
    cur = con.cursor()
    cur.execute("SELECT UUID, IsVehicle, Name FROM Assignments ORDER BY UUID asc")
    data = cur.fetchall()
    return data


def getAssignmentsPageHandler(response):
    assignments = getAssignments()
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_high_user(name, password)
    response.write(TemplateAPI.render('Manage_Assignments.html', response, {'assignments': assignments, 'name': name, 'password': password, 'is_Valid':is_Valid}))


def getLatestHandler(response):
    data = getLatestForEach()
    output = []
    for uuidData in data:
        o = list(uuidData)
        cur = con.cursor()
        cur.execute("SELECT Name, IsVehicle FROM Assignments WHERE UUID = ?", (str(uuidData[0]),))
        res = cur.fetchone()
        if res == None:
            res = ('No Assignment', False)
        cur.close()
        o.append(res[0])
        o.append(res[1])
        output.append(o)
    response.write(json.dumps(output))

def getPolyLineHandler(response): response.write(json.dumps(getLineData()))


#--------------------Code for displaying settings page--------------    
def displaySettingsPage(response):
    name = response.get_field("name")
    password = response.get_field("password")
    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_high_user(name, password)
    response.write(TemplateAPI.render('Settings.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))

def setHandler(response):
    time = str(float(response.get_field("time") if type(response.get_field("time")) is str else 0)*3600)
    print(time)
    uuid = response.get_field("uuid")
    f=open("options.txt",'w')
    f.write("UUIDs to Display:\n")
    f.write((uuid if type(uuid) is str else "")+"\n")
    f.write("Length of Trail (seconds):\n")
    f.write(time)
    f.close()
    response.redirect("/track_map")
#-------------------------------------------------------------------------------------

#-----------------------------Code for Dynamic Map Settings-------------------------


# This handler replaces the default handler for the Track_Map page
def displayMapPageD(response):
    name = response.get_field("name")
    password = response.get_field("password")

    if name == None or password == None:
        is_Valid = False
    else:
        is_Valid = get_user(name, password)
    response.write(TemplateAPI.render('Track_Map_d.html', response, {'name': name, 'password': password, 'is_Valid':is_Valid}))

def submitMapDSettings(response):
    a = response.get_field("timelim")
    time = str(float(a if a != None else '-1' )*3600)
    if time != float([line for line in open("options.txt")][1]) and float(time) >= 0:
        old=[line for line in open("options.txt")][:1]
    	f=open("options.txt",'w')
    	for line in old:
        	f.write(line)
    	f.write(time)
    	f.close()
	print('Time Saved')
    print(time)
    response.write(json.dumps(float([line for line in open("options.txt")][1])/3600))
    #response.redirect("/track_map/dyn")

def getUUIDList(response):
    cur = con.cursor()
    cur.execute("SELECT DISTINCT UUID FROM Positions WHERE Time>?",(int(time.time()-float([line for line in open("options.txt")][1])),)) 
    ids=[int(i[0]) if i[0]!=None else None for i in cur.fetchall()]
    print(ids)
    data=[]
    for id in ids:
	if id == None:
		continue
    	cur.execute("SELECT DISTINCT Name FROM Assignments WHERE UUID=?",(id,))
    	a=cur.fetchall()
        if a == []:
                continue
        data.append([id,str(a[0][0])])
    	
    print(data)
    response.write(json.dumps(data))
    


#-------------------------------------------------------------------------------------


    
#----------------------------------Custom_Map_Markers---------------------------------
markers=[line.split(',') for line in open("markers.txt")][1:]
for i in range(0,len(markers)):
    displayName=markers[i][0]+' '+markers[i][1]+','+markers[i][2]
    markers[i]=[displayName,float(markers[i][1]),float(markers[i][2]),markers[i][3].rstrip()]
    
print(markers)
def getCMData(response):
    response.write(json.dumps(markers))


    
#--------------------------------------User_Data--------------------------------------    
    
users = [line for line in open("users.txt")]  
user_dict = {}
for user in users:
    UUID = user.split(":")[0]
    Username = user.split(":")[1].split(",")[0]
    Password = user.split(":")[1].split(",")[1].strip()
    user_dict[UUID] = Username + "," + Password
    
def get_user(name, password):
    result = None
    for user in user_dict.keys():
        u_name = user_dict[user].split(",")[0]
        u_password = user_dict[user].split(",")[1]
        if str(name + " " + password) == str(u_name + " " + u_password):
            result = True
            break
    if result == None:
        return False
    else:
        return True

def make_user(input_name, input_password):
    UUID = int(len(user_dict.keys())) + 1
    user_dict[UUID] = input_name + "," + input_password
    with open("users.txt", "a") as file:
        file.write("\n" + str(UUID) + ":" + input_name + "," + input_password)
        
        
high_users = [line for line in open("high_users.txt")]  
high_user_dict = {}
for user in high_users:
    UUID = user.split(":")[0]
    Username = user.split(":")[1].split(",")[0]
    Password = user.split(":")[1].split(",")[1].strip()
    high_user_dict[UUID] = Username + "," + Password
    
def get_high_user(name, password):
    result = None
    for user in high_user_dict.keys():
        u_name = high_user_dict[user].split(",")[0]
        u_password = high_user_dict[user].split(",")[1]
        if str(name + " " + password) == str(u_name + " " + u_password):
            result = True
            break
    if result == None:
        return False
    else:
        return True
#-------------------------------------------------------------------------------------    




#--------------------------------Database Interaction--------------------------------- 
import sqlite3 as lite
import sys
import time

con = lite.connect('positions.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS Positions (UUID int, Lat float, Lon float, Time timestamp)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionTime ON Positions (Time)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionUUID ON Positions (UUID)")
cur.execute("CREATE INDEX IF NOT EXISTS PositionCombo ON Positions (Time, UUID)")
cur.execute("CREATE TABLE IF NOT EXISTS Assignments (UUID INTEGER PRIMARY KEY, IsVehicle BOOLEAN, Name varchar(255))")

con.commit()
cur.close()


def getTime():
    raw = str(datetime.now())
    datelist = []
    datelist.append(str(raw.split(" ")[1].split(".")[0]))
    datelist.append(str(raw.split(" ")[0].split("-")[2] + "-" + raw.split(" ")[0].split("-")[1]+ "-" + raw.split(" ")[0].split("-")[0]))
    return datelist


def insertPositions(UUID, Lat, Lon):
    Time = int(time.time())
    
    cur = con.cursor()
    cur.execute("INSERT INTO Positions (UUID, Lat, Lon, Time) VALUES (?, ?, ?, ?)", (UUID, Lat, Lon, Time))
    con.commit()
    cur.close()



def queryPositions():
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions")
    data = cur.fetchall()
    print(data)

def getLocations(limit):
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions ORDER BY Time desc LIMIT ?", (str(limit),))
    data = cur.fetchall()
    cur.close()
    return data
    
def getLineData():
    lim = int(time.time()-float([line for line in open("options.txt")][1]))
    print(lim)
    cur = con.cursor()    
    out = [
    ]
    cur.execute("SELECT DISTINCT UUID FROM Positions WHERE Time>?",(int(time.time()-float([line for line in open("options.txt")][1])),)) 
    ids=[int(i[0]) if i[0]!=None else None for i in cur.fetchall()]
    #---------------This Code is for filtering UUIDS through options.txt--------------
    #Deprecated
    
    
    #Either the UUIDs can be filtered in here
    #ids=[int(i) for i in [line for line in open("options.txt")][1].split(",")] 
    
    #Or they can be read from the available UUIDs in the SQL Database
    #cur.execute("SELECT UUID FROM Positions")
    #uuids = cur.fetchall()
    #ids=set()
    #for id in uuids:
    #    if type(id[0]) is int:
    #        ids.add(id[0])
    
    
    
    #for id in ids:
    #    cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions WHERE UUID=? AND Time>? ORDER BY Time DESC ", (str(id),str(lim)))
    #    data.append([list(i) for i in cur.fetchall()])
        
    #---------------------------------------------------------------------------------
    
    
    
    #Or the polyline data can be filtered by the client.
    for id in ids:
	if id== None:
		continue
    	cur.execute("SELECT UUID, Lat, Lon, Time FROM Positions WHERE Time>? AND UUID=? ORDER BY Time DESC ", (str(lim),str(id)))
    	data=[list(i) for i in (cur.fetchall())]
    	print(data)
    	while [] in data:
        	data.remove([])
        out.append(data)
    
    
    return out
    
    
def getLatestForEach():
    cur = con.cursor()
    cur.execute("SELECT UUID, Lat, Lon, MAX(TIME) FROM Positions GROUP BY UUID")
    data = cur.fetchall()
    cur.close()
    return data
#------------------------------------------------------------------------------------- 

    

#------------------------------Page Links---------------------------------------------
    
    
# ------------- Main Pages --------------------
server = Server('0.0.0.0', 80)
server.register("/", indexPage)
server.register("/about", aboutPage)
server.register("/random", randPage)
server.register("/input", inputPage)
server.register("/wiki", wikiPage)

#--------Training Pages--------------------------------------------
#----------   Cadets  ---------------
server.register("/training/cadets", cdtTrainPage)
server.register("/training/signalers", cdtTrainPageSig)
server.register("/training/operations", cdtTrainPageOps)
server.register("/training/admin", cdtTrainPageAdmin)
server.register("/training/q-store", cdtTrainPageQstore)

#-----------  CMAPS  ---------------
server.register("/training/cmaps", cmapTrainPage)

#--------------- Maps ---------------------------
#/track_map is deprecated
server.register("/track_map/dyn", displayMapPageD)
server.register("/track_map/dyn/pushT",submitMapDSettings)
server.register("/track_map/dyn/getU",getUUIDList)
server.register("/assignments", getAssignmentsPageHandler)
server.register("/ass/new", insertAssignments)

#------------ Database --------------------------
#server.register("/settings",displaySettingsPage)
#server.register("/set",setHandler)
server.register("/all", showAllDebugPage)
server.register("/location/push", inputHandler)
server.register("/location/get/polyline", getPolyLineHandler)
server.register("/location/get/sm", getCMData)
server.register("/location/get/all", getLatestHandler)
server.register("/track_database", displayAllPage)
#server.register("/track_map", displayMapPage)

server.run(dummy)
