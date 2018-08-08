import csv


class dictionary:

    def init():
        pass

    def save(self, dic=''):
        if not dic:
            dic = {

                'Return Name': 'Serials',

                'LOCSTAT': {
                    "A": "Location",
                    "B": "Moving / Stationary",
                    "C": "Time"
                },

                'MAINTDEM': {
                    "A": "Location",
                    "B": "Moving / Stationary",
                    "C1": "Time",
                    "C2": "Time",
                    "C3": "Time",
                    "D1": "Time",
                    "D2": "Time",
                    "D3": "Time",
                    "E": "Time"
                },

                'MOVEREQ': {
                    "A": "Location",
                    "B": "Moving / Stationary",
                    "C": "Time"
                },    

            }
        w = csv.writer(open("output.csv", "w"))

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

    dictionary.save

"""
class admin_return:
    
    def init(self):
        self.serials_def = dictionary.read()

"""
