import csv


class dictionary:

    def init():
        pass

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
        w = csv.writer(open("serials.csv", "w"))

        for name, serials in dic.items():
            lst = []
            try:
                for serial, des in serials.items():
                    lst.append(serial+':'+des)
            except:
                lst = [serials]
            w.writerow([(name), (', '.join(lst))])

    def read():
        # wip
        dic = {}
        r = csv.reader(open("output.csv", "r"))
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

    #meme = dictionary.read()

    x = dictionary()
    x.save()

"""
class admin_return:
    
    def init(self):
        self.serials_def = dictionary.read()

"""
