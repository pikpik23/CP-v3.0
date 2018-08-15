# LOG save Test
from csv import reader, writer


LOG = [{'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'},
       {'name': 'LOCSTAT', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Sargent',
        'time': '151111', 'A': 'POE', 'B': 'on', 'C': '234324'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS',
           'duty': 'Sargent', 'time': '151203', 'msg': 'hello'},
       {'name': 'MESSAGE', 'sender': '6-0', 'receiver': '0A',
           'duty': 'Lambinon', 'time': '151305', 'msg': 'memr'},
       {'name': 'MESSAGE', 'sender': '0A', 'receiver': 'KGS', 'duty': 'Lambinon', 'time': '151306', 'msg': 'gggb'}, {
           'name': 'MESSAGE', 'sender': '0A', 'receiver': '0A', 'duty': 'Lambinon', 'time': '151306', 'msg': 'lol'}
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
        inn_lst = []
        for serial, val in test.items():
            if not (serial in main_keys):
                inn_lst.append(serial+': '+val)

        lst.append('; '.join(inn_lst))

        w.writerow(lst)


save()
print(LOG)
