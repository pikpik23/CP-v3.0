from csv import reader, writer
from collections import OrderedDict as OrdDic
import sqlite3


class dbManager:

    FILE_NAME = 'LOG_Temp.db'
    TABLE_NAME = 'LOG_RETURNS'

    def create_DB():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            # Create table
            c.execute('''CREATE TABLE LOG_RETURNS
                        (logID int,
                        returnType text,
                        sender text,
                        reciever text,
                        logTime int,
                        dutyOfficer text,
                        serials text
                        )''')

            conn.commit()

    def read():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            for row in c.execute('SELECT * FROM stocks ORDER BY price'):
                print(row)

    def input():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            t = ('RHAT',)
            c.execute('SELECT * FROM stocks WHERE symbol=?', t)

    def massInput():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            # Larger example that inserts many records at a time
            purchases = [('2006-03-28', 'BUY', 'IBM', 1000, 45.00),
                         ('2006-04-05', 'BUY', 'MSFT', 1000, 72.00),
                         ('2006-04-06', 'SELL', 'IBM', 500, 53.00),
                         ]
            c.executemany('INSERT INTO stocks VALUES (?,?,?,?,?)', purchases)

    def newReturn(lst):
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(
                'INSERT INTO '+dbManager.TABLE_NAME+' VALUES (NULL,' +
                '?, '*(len(lst) - 1) + '?)',
                lst)

    def readReturn():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            return c.execute('SELECT * FROM ' + dbManager.TABLE_NAME)

    def findIndex(logID):
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            sqlStr = ("""SELECT * FROM """ +
                      dbManager.TABLE_NAME +
                      """ WHERE logID=?""")
            x = c.execute(sqlStr, [str(logID)])
            return x

    def getFirstIndex():
        with sqlite3.connect(dbManager.FILE_NAME) as conn:
            c = conn.cursor()
            sqlStr = ("""SELECT logID FROM """ +
                      dbManager.TABLE_NAME +
                      """ WHERE logID = (SELECT MAX(logID)  FROM """ +
                      dbManager.TABLE_NAME + ")")
            x = c.execute(sqlStr)
            for i in x:
                i = int(list(i)[0])
            return i


class file:

    def getFirst():
        return dbManager.getFirstIndex()

    def insert_into_dic(dct, key, value, dict_setitem=dict.__setitem__):
        """ still a WIP but hopefully will allow me to add at index """
        root = dct._OrderedDict__root
        first = root[1]

        if key in dct:
            link = dct._OrderedDict__map[key]
            link_prev, link_next, _ = link
            link_prev[1] = link_next
            link_next[0] = link_prev
            link[0] = root
            link[1] = first
            root[1] = first[0] = link
        else:
            root[1] = first[0] = dct._OrderedDict__map[key] = [root,
                                                               first,
                                                               key]
            dict_setitem(dct, key, value)

    def save_dic(dic=None):
        """ Saves the given dictionary of serials to a file """

        if not dic:
            dic = {

                'LOCSTAT': {
                    "A": {
                        "desc": "Location",
                        "data_type": "location"
                    },  # GR

                    "B": {
                        "desc": "Moving / Stationary",
                        "data_type": "choice",
                        "options": ["Moving", "Stationary"]
                    },  # boolean

                    "C": {
                        "desc": "Direction of Movement or Length of Halt",
                        "data_type": "string"
                    }
                },

                'MAINTDEM': {
                    "A": {
                        "desc": "Demand Number",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Priority",
                        "data_type": "choice",
                        "options": ["Pri 1", "Pri 2", "Pri 3"]
                    },

                    "C1": {
                        "desc": "Quantity of Ration Packs",
                        "data_type": "string"
                    },

                    "C2": {
                        "desc": "Quantity of Water Jerries",
                        "data_type": "string"
                    },

                    "C3": {
                        "desc": "Other Items and Quantity",
                        "data_type": "long"
                    },

                    "D1": {
                        "desc": "Location of Delivery",
                        "data_type": "location"
                    },

                    "D2": {
                        "desc": "Time of Delivery",
                        "data_type": "string"
                    },

                    "D3": {
                        "desc": "Mode of delivery",
                        "data_type": "choice",
                        "options": ["Playtime", "Pickup"]
                    },

                    "E": {
                        "desc": "Remarks",
                        "data_type": "long"
                    }
                },

                'STRENGTHSTATE': {
                    "A1": {
                        "desc": "No. of Own Cadets",
                        "data_type": "string"
                    },

                    "A2": {
                        "desc": "No. of Attachments",
                        "data_type": "string"
                    },

                    "A3": {
                        "desc": "No. of Staff",
                        "data_type": "string"
                    },

                    "B1": {
                        "desc": "No. of expected attachments in next 24 hours",
                        "data_type": "string"
                    },

                    "B2": {
                        "desc": "No. of expected detachments in next 24 hours",
                        "data_type": "string"
                    },

                    "C": {
                        "desc": "Total Personnel",
                        "data_type": "string"
                    },
                },

                'CASEVAC': {
                    "PRI": {
                        "desc": "Priority",
                        "data_type": "choice",
                        "options": ["Pri 1", "Pri 2", "Pri 3"]
                    },

                    "A": {
                        "desc": "Patient ID",
                        "data_type": "string"
                    },

                    "B1": {
                        "desc": "No. of Stretcher Cases",
                        "data_type": "string",
                    },

                    "B2": {
                        "desc": "No. of Sitting Cases",
                        "data_type": "string"
                    },

                    "C": {
                        "desc": "Requirements for special equipment",
                        "data_type": "long"
                    },

                    "D1": {
                        "desc": "Location of RV",
                        "data_type": "location"
                    },

                    "D2": {
                        "desc": "Callsign and Channel at RV",
                        "data_type": "string"
                    },

                    "E": {
                        "desc": "Remarks",
                        "data_type": "long"
                    },
                },

                'NOTICAS': {
                    "A": {
                        "desc": "Patient ID",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Rank",
                        "data_type": "string",
                    },

                    "C": {
                        "desc": "Name",
                        "data_type": "string"
                    },

                    "D": {
                        "desc": "Details of injury or illness",
                        "data_type": "long"
                    },

                    "E": {
                        "desc": "Location of injury",
                        "data_type": "location"
                    },

                    "F": {
                        "desc": "Time of injury",
                        "data_type": "string"
                    },

                    "G": {
                        "desc": "Treatment administered",
                        "data_type": "long"
                    },

                    "H": {
                        "desc": "Remarks and Present Location",
                        "data_type": "long"
                    },

                },

                'SITREP': {
                    "A": {
                        "desc": "Time",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Own Situation",
                        "data_type": "long",
                    },

                    "C": {
                        "desc": "Situation with regards to third parties",
                        "data_type": "long"
                    },

                    "D": {
                        "desc": "Future intentions and " +
                        "relevant general information",
                        "data_type": "long"
                    },
                },

                'INTREP': {
                    "A": {
                        "desc": "Time of incident",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Location of incident",
                        "data_type": "location",
                    },

                    "C": {
                        "desc": "Brief description of incident",
                        "data_type": "long"
                    },

                    "D": {
                        "desc": "Commanders evaluation",
                        "data_type": "long"
                    },
                },

                'MOVEREQ': {
                    "A": {
                        "desc": "Callsign of person at pick-up location",
                        "data_type": "string"
                    },

                    "B1": {
                        "desc": "Location of pick up",
                        "data_type": "location",
                    },

                    "B2": {
                        "desc": "Location of destination",
                        "data_type": "location"
                    },

                    "C1": {
                        "desc": "Number of persons to be transported",
                        "data_type": "string"
                    },

                    "C2": {
                        "desc": "Configuration of troops",
                        "data_type": "choice",
                        "options": ["Marching Order", "Patrol Order"]
                    },

                    "D1": {
                        "desc": "Description of cargo",
                        "data_type": "string"
                    },

                    "D2": {
                        "desc": "Estimated number of vehicles",
                        "data_type": "string"
                    },

                    "D3": {
                        "desc": "Is a loading/unloading pary available at Loc",
                        "data_type": "string"
                    },

                    "E": {
                        "desc": "Time of pickup",
                        "data_type": "string"
                    },
                },

                'STARLIGHTREQ': {
                    "A": {
                        "desc": "Callsign of person at location",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Location",
                        "data_type": "location",
                    },

                    "C": {
                        "desc": "Nature of illness or injury",
                        "data_type": "long"
                    },

                    "D": {
                        "desc": "Any RV details",
                        "data_type": "long"
                    },

                    "E": {
                        "desc": "Remarks",
                        "data_type": "long"
                    },
                },

                'SENTRYREP': {
                    "A": {
                        "desc": "Vehicle Number Plate",
                        "data_type": "string"
                    },

                    "B": {
                        "desc": "Status",
                        "data_type": "choice",
                        "options": ["Entering", "Leaving"]
                    },

                    "C": {
                        "desc": "Passengers",
                        "data_type": "string"
                    },

                    "D": {
                        "desc": "Destination",
                        "data_type": "location"
                    },

                    "E": {
                        "desc": "Estimated time of return",
                        "data_type": "string"
                    },

                    "F": {
                        "desc": "Remarks",
                        "data_type": "long"
                    }
                }
            }
        # print("start saving")
        w = writer(open("resources/files/serials.csv", "w"))
        w.writerow(['Return Name', 'Serials'])
        for name, serials in dic.items():
            lst = []
            if name == "Return Name":
                lst.append(name)
                lst.append(serials)
            else:
                for serial in serials:
                    if serial == "Return Name":
                        lst.append(serials)
                    else:
                        inner_lst = []
                        for cont in serials[serial]:
                            if cont == "options":
                                inner_lst.append(cont+";;@@;;" +
                                                 ";;##;;".join(
                                                     serials
                                                     [serial]
                                                     ["options"]))
                            else:
                                inner_lst.append(
                                    cont+";;@@;;"+serials[serial][cont])
                        lst.append(serial+';;:::;;'+";;!!!;;".join(inner_lst))
            w.writerow([(name), (';;,,,;;'.join(lst))])

    def read_dic():
        """ reads the dictionary of serials """
        # should return the original format
        dic = OrdDic()
        r = reader(open("resources/files/serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = OrdDic()
                for serial in row[1].split(';;,,,;;'):
                    serial = serial.split(';;:::;;')
                    sub_dic = OrdDic()
                    for sub_serial in serial[1].split(';;!!!;;'):
                        sub_serial = sub_serial.split(";;@@;;")
                        if sub_serial[0] == 'options':
                            options = sub_serial[1].split(";;##;;")
                            sub_dic.update({sub_serial[0]: options})
                        else:
                            sub_dic.update(
                                {sub_serial[0]: sub_serial[1]})
                    inner_dic.update({serial[0]: sub_dic})
                # lst = row[1].split('\\')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
        return dic

    def read_legacy():
        """ reads the dictionary and returns it in the legacy format """
        serials = file.read_dic()
        final_dic = OrdDic()
        for name, dic in serials.items():
            inner_dic = OrdDic()
            for serial in dic:
                inner_dic.update({serial: dic[serial]['desc']})
            final_dic.update({name: inner_dic})
        return final_dic

    def read_locations():
        """ reads the file containing the locations """
        r = open("resources/files/locations.txt", "r")
        locations = r.read().split("\n")
        return locations

    def save_Locations(lst):
        w = open("resources/files/locations.txt", "w")
        w.write(lst)

    def read_callsigns():
        """ reads the file containing the callsigns """
        r = open("resources/files/callsigns.txt", "r")
        callsigns = r.read().split("\n")
        return callsigns

    def read_settings():
        """ reads the settings from file """
        r = open("resources/files/settings.txt", "r")
        settings = OrdDic()
        for option in r.read().split('\n'):
            try:
                option = option.split('\\')
                settings.update({option[0]: option[1]})
            except IndexError:
                pass
        return settings

    def save_settings(dic):
        """ saves the given settings (dictionary) to file """
        w = open("resources/files/settings.txt", "w")
        for sett, val in dic.items():
            w.write(sett+'\\'+val+'\n')

    def save_log(log):
        """ Saves the log to file """

        # print('\n\n\nsaving')
        '''
        s = Timer(10.0, save)
        s.daemon = True
        s.start()
        '''
        # w = writer(open("resources/static/logs.csv", 'w'))

        main_keys = [
            'name',
            'sender',
            'receiver',
            'time',
            'duty'
        ]

        # print(test)

        lst = []
        for key in main_keys:
            # print(key)
            lst.append(log[key])
        inn_lst = []
        for serial, val in log.items():
            if not (serial in main_keys):
                inn_lst.append(serial+'\\'+val)

        lst.append('||'.join(inn_lst))

        dbManager.newReturn(lst)

    def load_log(logID=None):
        """ loads the log file """
        # try:
        #     r = reader(open("resources/static/logs.csv", "r"))
        # except FileNotFoundError:
        #     w = open("resources/static/logs.csv", 'w')
        #     w.close()
        #     r = reader(open("resources/static/logs.csv", "r"))

        if logID:
            x = dbManager.findIndex(logID)
        else:
            x = dbManager.readReturn()

        local_log = []
        for row in x:
            ret = OrdDic()

            # print(row)
            ret.update({'logID': row[0]})
            ret.update({'name': row[1]})
            ret.update({'sender': row[2]})
            ret.update({'receiver': row[3]})
            ret.update({'time': row[4]})
            ret.update({'duty': row[5]})

            for serial_data in row[6:]:
                for serial in serial_data.split('||'):
                    ser, val = serial.split('\\')
                    val = ""+val
                    ret.update({ser: str(val)})
            local_log.append(ret)

        return local_log


if __name__ == '__main__':

    settts = file.read_settings()
    file.save_settings(settts)
    file.read_locations()
    file.read_callsigns()
    file.save_dic()
    file.read_dic()

    # x = file()
    # x.save()


'''
INPUT TYPES

short text
location (contain a list of possible location)
long text
radio_button (list of possible options)

'''


"""
class admin_return:

    def init(self):
        self.serials_def = file.read()

"""
