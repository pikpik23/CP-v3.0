"""The Main Section for the CP replacement"""
import datetime
from sheetsBackend import Sheet
from read_dictionary import dictionary


def send_message(sender, msg, time):
    '''Edit this to change the program.'''
    print("-------------------------\n" +
          "Sending data to server...\n" +
          "-------------------------")

    new_msg = []
    for serial in msg:
        if serial != 'name':
            new_msg.append(msg[serial])

    data = [[str(datetime.datetime.now()), sender,
             msg['name'], ", ".join(new_msg)], ]
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


class admin_returns:

    def __init__(self):
        global serials_def
        serials_def = dictionary.read()

    def print_serials(self, return_type):
        print('-------------------------')
        print(return_type)
        print('-------------------------')

        for serial in serials_def[return_type]:
            print(serial+': ' +
                  serials_def[return_type][serial])
        print('-------------------------')

    class new_return:

        def __init__(self, return_type, sender, lst, time='', send=True):
            if time:
                self.time = time
            else:
                self.time = datetime.datetime.now()
            self.sender = sender

            try:
                self.serials_dict = {'name': return_type}
                i = 0
                for serial in serials_def[return_type]:
                    self.serials_dict.update({str(serial): lst[i]})
                    i += 1
            except:
                print("That Return type dosn't exist")

            print(self.serials_dict)
            if send:
                self.send_message()

        def send_message(self):
            send_message(self.sender,
                         self.serials_dict, self.time)

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
            print(admin_returns.locstat.name)
            print(' '.join(record[0:2]))
            print('-----------------------------')
            record = record[3].split(', ')
            i = 0
            for serial in admin_returns.locstat.definition:
                print(serial + ': '+record[i])
                i += 1
            print('-----------------------------')
            print('')


def import_sheets():
    data = SHEET.readSheet()

    new_data = []

    for record in data:
        if record[2] == 'LOCSTAT':
            x = admin_returns.locstat(
                record[1], record[3].split(', '), time=record[0], send=False)
            new_data.append(x)
    return new_data


if __name__ == '__main__':

    SHEET = Sheet(
        '12T7Ub21E-gAlwtJRZdsu3cww-wwIOvdjP_plhMxUn-0', 'CP!A2:Z')

    '''
    needs updating
    # reading sheet
    # read data
    data = import_sheets()

    for 
    '''

    '''
    # Updating sheet
    # init admin returns (reads from file)
    rtrns = admin_returns()

    # example send locstat
    rtrns.new_return('LOCSTAT', '2-0', ['a', 'b', 'c'])

    # example lookup serials
    rtrns.print_serials("LOCSTAT")
    '''

# cp_main()
