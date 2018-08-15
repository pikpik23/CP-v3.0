# LOG load Test
from csv import reader, writer

LOG = []


def load_log():
    r = reader(open("logs.csv", "r"))

    for row in r:
        ret = {}
        try:
            # print(row)
            ret.update({'name': row[0]})
            ret.update({'sender': row[1]})
            ret.update({'receiver': row[2]})
            ret.update({'time': row[3]})
            ret.update({'duty': row[4]})

            for serial_data in row[5:]:
                for serial in serial_data.split('; '):
                    ser, val = serial.split(': ')
                    ret.update({ser: val})
            LOG.append(ret)
        except:
            print("error")


'''
def load():
    # print('\n\n\nsaving')

    s = Timer(10.0, load)
    s.daemon = True
    s.start()

    w = writer(open("logs_test.csv", 'w'))

    main_keys = [
        'name',
        'sender',
        'receiver',
        'time',
        'duty'
    ]

    for ret in LOG:

        test = ret
        print(test)

        lst = []
        for key in main_keys:
            print(key)
            lst.append(test[key])
        inn_lst = []
        for serial, val in test.items():
            if not (serial in main_keys):
                inn_lst.append(serial+': '+val)

        lst.append('; '.join(inn_lst))

        w.writerow(lst)
'''

load_log()
print(LOG)
