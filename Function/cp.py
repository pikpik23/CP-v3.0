"""The Main Section for the CP replacement"""
import datetime
from sheetsBackend import init, editTable, append, printValues


def send_message(msg_type, msg):
    '''Edit this to change the program.'''
    print("-------------------------\n" +
          "Sending data to server...\n" +
          "-------------------------")
    # ["Time", "Type", "Message"]
    data = [[str(datetime.datetime.now()), msg_type, msg], ]
    rtrn = append(data, CellRange=(msg_type+'!A2:Z'))

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

        def __init__(self, lst):
            self.serials = {
                "A": lst[0],
                "B": lst[1],
                "C": lst[2]
            }

        def send_message(self):
            send_message(self.name, self.serials)

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


'''
def cp_reset():
    """Resets the table"""
    editTable(record=['', '', ''])

def assign_dictionary():
    """Defines the dictonary of serials"""
    availible_types = {
        "Locstat": {
            "A": "Location",
            "B": "Moving / Stationary",
            "C": "Time"
        },
        "Test": {
            "A": "Meme",
            "B": "Meme2",
            "C": "mem3",
        }
    }
    print(availible_types)
'''

if __name__ == '__main__':
    # init()  # Must always be run first

    x = admin_return.locstat

    define(x)

    x = admin_return.locstat(["Teest", "twe", "sure"])
    recall(x)
    # print(admin_return.locstat.definition)
    # x.send_message()

# cp_main()
