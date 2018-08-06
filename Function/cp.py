"""The Main Section for the CP replacement"""
import datetime
from sheetsBackend import Sheet


def send_message(msg_type, sender, msg, time):
    '''Edit this to change the program.'''
    print("-------------------------\n" +
          "Sending data to server...\n" +
          "-------------------------")

    new_msg = []
    for serial in msg:
        new_msg.append(msg[serial])

    data = [[str(datetime.datetime.now()), sender,
             msg_type, ", ".join(new_msg)], ]
    rtrn = SHEET.append(data, CellRange=('CP!A2:Z'))

    print("\n\n\n-------------------------\n" +
          "Updated\n\n" +
          (str(': '.join(rtrn['updates']['updatedRange'].split("!")))) +
          '\nRows: '+str(rtrn['updates']['updatedRows']) +
          '\nColumns: '+str(rtrn['updates']['updatedColumns']) +
          "\n-------------------------\n")

    # Do something


def define(return_type):
    print('-------------------------')
    print(return_type.name)
    print('-------------------------')

    for serial in return_type.definition:
        print(serial+': '+return_type.definition[serial])
    print('-------------------------')


def recall(return_type):
    print('-------------------------')
    print(return_type.name)
    print('-------------------------')

    for serial in return_type.serials:
        print(serial+': '+return_type.serials[serial])
    print('-------------------------')


class admin_return:
    class locstat:

        name = 'LOCSTAT'

        definition = {
            "A": "Location",
            "B": "Moving / Stationary",
            "C": "Time"
        }

        def __init__(self, sender, lst, time='', send=True):
            self.time = ''
            if time:
                self.time = time
            else:
                self.time = datetime.datetime.now()
            self.sender = sender
            self.serials = {
                "A": lst[0],
                "B": lst[1],
                "C": lst[2]
            }
            if send:
                self.send_message()

        def send_message(self):
            send_message(self.name, self.sender, self.serials, self.time)

    class maintdem:
        name = 'MAINTDEM'

        definition = {
            "A": "Location",
            "B": "Moving / Stationary",
            "C1": "Time",
            "C2": "Time",
            "C3": "Time",
            "D1": "Time",
            "D2": "Time",
            "D3": "Time",
            "E": "Time"
        }


def print_sheets():
    data = SHEET.readSheet()
    for record in data:
        if record[2] == 'LOCSTAT':
            print('-----------------------------')
            print(admin_return.locstat.name)
            print(' '.join(record[0:2]))
            print('-----------------------------')
            record = record[3].split(', ')
            i = 0
            for serial in admin_return.locstat.definition:
                print(serial + ': '+record[i])
                i += 1
            print('-----------------------------')
            print('')


def import_sheets():
    data = SHEET.readSheet()

    new_data = []

    for record in data:
        if record[2] == 'LOCSTAT':
            x = admin_return.locstat(
                record[1], record[3].split(', '), time=record[0], send=False)
            new_data.append(x)
    return new_data


if __name__ == '__main__':

    SHEET = Sheet(
        '12T7Ub21E-gAlwtJRZdsu3cww-wwIOvdjP_plhMxUn-0', 'CP!A2:Z')

    data = import_sheets()

    for record in data:
        print(record.time)

    # send = "3-0"
    # data = ["GR123456", "Moving", "South"]

    # x = admin_return.locstat(send, data)

    # print(admin_return.locstat.definition)
    # x.send_message()

# cp_main()
