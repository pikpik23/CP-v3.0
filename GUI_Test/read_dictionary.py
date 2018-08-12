import csv


class dictionary:

    def save(dic=None):
        if not dic:
            dic = {

                'Return Name': 'Serials',

                'MESSAGE': {
                    "MSG": {
                        "desc": "Message",
                        "data_type": "long"
                    }
                },

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

        w = csv.writer(open("new_serials.csv", "w"))

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
                                inner_lst.append(cont+"@" +
                                                 "#".join(serials[serial]["options"]))
                            else:
                                inner_lst.append(
                                    cont+"@"+serials[serial][cont])
                        lst.append(serial+':'+"!".join(inner_lst))
            w.writerow([(name), (', '.join(lst))])

    def read():
        # should return the original format
        dic = {}
        r = csv.reader(open("new_serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = {}
                for serial in row[1].split(', '):
                    serial = serial.split(':')
                    sub_dic = {}
                    for sub_serial in serial[1].split('!'):
                        sub_serial = sub_serial.split("@")
                        if sub_serial[0] == 'options':
                            options = sub_serial[1].split("#")
                            sub_dic.update({sub_serial[0]: options})
                        else:
                            sub_dic.update(
                                {sub_serial[0]: sub_serial[1]})
                    inner_dic.update({serial[0]: sub_dic})
                lst = row[1].split(': ')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
        return dic

    def read_legacy():
        serials = dictionary.read()
        final_dic = {}
        for name, dic in serials.items():
            inner_dic = {}
            for serial in dic:
                inner_dic.update({serial: dic[serial]['desc']})
            final_dic.update({name: inner_dic})
        return final_dic
        # wip

        # should return only this format
        '''
            'LOCSTAT': {
            "A": "Location",  # GR
            "B": "Moving / Stationary",  # boolean
            "C": "Direction of Movement or Length of Halt"
        },
        '''

    def read_locations():
        r = open("locations.txt", "r")
        locations = r.read().split("\n")
        return locations

    def read_settings():
        r = open("settings.txt", "r")
        settings = {}
        for option in r.read().split('\n'):
            try:
                option = option.split(': ')
                settings.update({option[0]: option[1]})
            except IndexError:
                pass
        return settings

    def read_legacy_old_file():
        dic = {}
        r = csv.reader(open("serials.csv", "r"))
        i = 0
        for row in r:
            if i:
                inner_dic = {}
                for serial in row[1].split(', '):
                    serial = serial.split(':')
                    inner_dic.update({serial[0]: serial[1]})
                lst = row[1].split(': ')
                dic.update({row[0]: inner_dic})
            else:
                i += 1
        return dic

    def save_settings(dic):
        w = open("settings.txt", "w")
        for sett, val in dic.items():
            w.write(sett+': '+val+'\n')


if __name__ == '__main__':

    dic = dictionary.read_settings()
    dictionary.save_settings(dic)
    dictionary.read_locations()
    dictionary.save()
    dictionary.read()

    # x = dictionary()
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
        self.serials_def = dictionary.read()

"""
