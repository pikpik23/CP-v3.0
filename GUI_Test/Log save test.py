# LOG save Test
from csv import reader, writer


LOG = [{'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'}
       ]


def save():
    # print('\n\n\nsaving')
    '''
    s = Timer(10.0, save)
    s.daemon = True
    s.start()
    '''
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
            test.pop(key, None)
        inn_lst = []
        for serial, val in test.items():
            inn_lst.append(serial+': '+val)

        lst.append('; '.join(inn_lst))

        w.writerow(lst)
    # print("Saved")


save()
