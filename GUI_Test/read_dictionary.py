import csv


class dictionary:

    def init():
        pass

    def save(self, dic=None):
        if not dic:
            dic = {

                'Return Name': 'Serials',

                'LOCSTAT': {
                    "A": {
                        "desc": "Location",
                        "data_type": "string"
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
                }
            }

        """ =========OLD VERSION=============
        def save(self, dic=''):
            if not dic:
                dic = {

                    'Return Name': 'Serials',

                    'LOCSTAT': {
                        "A": "Location",  # GR
                        "B": "Moving / Stationary",  # boolean
                        "C": "Direction of Movement or Length of Halt"
                    },

                    'MAINTDEM': {
                        "A": "Demand Number",
                        "B": "Priority",  # PRI
                        "C1": "Quantity of Ration Packs",
                        "C2": "Quantity of Water Jerries",
                        "C3": "Other Items and Quantity",
                        "D1": "Location of Delivery",  # GR or NL
                        "D2": "Time of Delivery",  # Date/Time Group
                        "D3": "Mode of Delivery",  # boolean Playtime/Pickup
                        "E": "Remarks"
                    },

                    'STRENGTHSTATE': {
                        "A1": "No. of Own Cadets",
                        "A2": "No. of Attachments",
                        "A3": "No. of Staff",
                        "B1": "No. of expected attachments in next 24 hours",
                        "B2": "No. of expected detachments in next 24 hours",
                        "C": "Total Personnel"
                    },

                    'CASEVAC': {
                        "A": "Patient ID",
                        "B1": "No. of Stretcher Cases",
                        "B2": "No. of Sitting Cases",
                        "C": "Requirements for special equipment",
                        "D1": "Location of RV",  # GR or NL
                        "D2": "Callsign and Channel at RV",
                        "E": "Remarks"
                    },

                    'NOTICAS': {
                        "A": "Patient ID",
                        "B": "Rank",
                        "C": "Name",
                        "D": "Details of injury or illness",
                        "E": "Location of injury",  # GR or NL
                        "F": "Time of injury",  # DTG
                        "G": "Treatment administered",
                        "H": "Remarks and Present Location"  # GR or NL
                    },

                    'SITREP': {
                        "A": "Time",  # DTG
                        "B": "Own Situation",
                        "C": "Situation with Regard to third parties",
                        "D": "Future intentions and relevant general information"
                    },

                    'INTREP': {
                        "A": "Time of incident",  # DTG
                        "B": "Location of incident",  # GR or NL
                        "C": "Brief description of incident",
                        "D": "Commanders evaluation"
                    },

                    'MOVEREQ': {
                        "A": "Callsign of person at pick-up location",
                        "B1": "Location of pick up",  # GR AND LOC
                        "B2": "Location of Destination",  # GR and LOC
                        "C1": "Number of persons to be transported",
                        "C2": "Configuration of troops",  # Boolean marching or patrol
                        "D1": "Description of cargo",
                        "D2": "Estimated number of vehicles",
                        "D3": "Is a loading/unloading pary available at Loc",
                        "E": "Time of pickup"  # DTG
                    },

                    'STARLIGHTREQ': {
                        "A": "Callsign of person at location",
                        "B": "Location",  # GR or NL
                        "C": "Nature of illness or injury",
                        "D": "Any RV details",
                        "E": "Remarks"
                    },

                    'SENTRYREP': {
                        "A": "Vehicle Number Plate",
                        "B": "Status",  # boolean returning/leaving
                        "C": "Passengers",
                        "D": "Destination",
                        "E": "Estimated time of return",
                        "F": "Remarks"
                    },

                }
            """

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
                                inner_lst.append(cont+"@"
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


if __name__ == '__main__':

    meme = dictionary.read_legacy()
    print(meme)

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
