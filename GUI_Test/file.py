from csv import reader, writer


class file:

    def save_dic(dic=None):
        if not dic:
            dic = {

                'Return Name': 'Serials',

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
                        "desc": "Future intentions and relevant general information",
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
                        "desc": "Remarksl",
                        "data_type": "long"
                    }
                }
            }

        w = writer(open("resources/files/new_serials.csv", "w"))

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
                                                 ";;##;;".join(serials[serial]["options"]))
                            else:
                                inner_lst.append(
                                    cont+";;@@;;"+serials[serial][cont])
                        lst.append(serial+';;:::;;'+";;!!!;;".join(inner_lst))
            w.writerow([(name), (';;,,,;;'.join(lst))])

    def read_dic():
        # should return the original format
        dic = {}
        r = reader(open("resources/files/new_serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = {}
                for serial in row[1].split(';;,,,;;'):
                    serial = serial.split(';;:::;;')
                    sub_dic = {}
                    for sub_serial in serial[1].split(';;!!!;;'):
                        sub_serial = sub_serial.split(";;@@;;")
                        if sub_serial[0] == 'options':
                            options = sub_serial[1].split(";;##;;")
                            sub_dic.update({sub_serial[0]: options})
                        else:
                            sub_dic.update(
                                {sub_serial[0]: sub_serial[1]})
                    inner_dic.update({serial[0]: sub_dic})
                lst = row[1].split(';;;///;;;')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
        return dic

    def read_legacy():
        serials = file.read_dic()
        final_dic = {}
        for name, dic in serials.items():
            inner_dic = {}
            for serial in dic:
                inner_dic.update({serial: dic[serial]['desc']})
            final_dic.update({name: inner_dic})
        return final_dic

    def read_locations():
        r = open("resources/files/locations.txt", "r")
        locations = r.read().split("\n")
        return locations

    def read_callsigns():
        r = open("resources/files/callsigns.txt", "r")
        callsigns = r.read().split("\n")
        return callsigns

    def read_settings():
        r = open("resources/files/settings.txt", "r")
        settings = {}
        for option in r.read().split('\n'):
            try:
                option = option.split(';;;///;;;')
                settings.update({option[0]: option[1]})
            except IndexError:
                pass
        return settings

    def read_legacy_old_file():
        dic = {}
        r = reader(open("resources/files/serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = {}
                for serial in row[1].split(';;,,,;;'):
                    serial = serial.split(';;:::;;')
                    inner_dic.update({serial[0]: serial[1]})
                lst = row[1].split(';;;///;;;')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
        return dic

    def save_settings(dic):
        w = open("resources/files/settings.txt", "w")
        for sett, val in dic.items():
            w.write(sett+';;;///;;;'+val+'\n')

    def save_log(log):
        # print('\n\n\nsaving')
        '''
        s = Timer(10.0, save)
        s.daemon = True
        s.start()
        '''
        w = writer(open("resources/static/logs.csv", 'w'))

        main_keys = [
            'name',
            'sender',
            'receiver',
            'time',
            'duty'
        ]

        for ret in log:

            test = ret
            # print(test)

            lst = []
            for key in main_keys:
                # print(key)
                lst.append(test[key])
            inn_lst = []
            for serial, val in test.items():
                if not (serial in main_keys):
                    inn_lst.append(serial+';;;///;;;'+val)

            lst.append(';;;,,,;;;'.join(inn_lst))

            w.writerow(lst)

    def load_log():
        try:
            r = reader(open("resources/static/logs.csv", "r"))
        except:
            w = open("resources/static/logs.csv", 'w')
            w.close()
            r = reader(open("resources/static/logs.csv", "r"))

        local_log = []
        for row in r:
            ret = {}

            # print(row)
            ret.update({'name': row[0]})
            ret.update({'sender': row[1]})
            ret.update({'receiver': row[2]})
            ret.update({'time': row[3]})
            ret.update({'duty': row[4]})

            for serial_data in row[5:]:
                for serial in serial_data.split(';;;,,,;;;'):
                    ser, val = serial.split(';;;///;;;')
                    ret.update({ser: val})
            local_log.append(ret)

            '''
            try:
                # print(row)
                ret.update({'name': row[0]})
                ret.update({'sender': row[1]})
                ret.update({'receiver': row[2]})
                ret.update({'time': row[3]})
                ret.update({'duty': row[4]})

                for serial_data in row[5:]:
                    for serial in serial_data.split(';;;,,,;;;'):
                        ser, val = serial.split(';;;///;;;')
                        ret.update({ser: val})
                local_log.append(ret)
            except:
                print("error")
            '''
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
