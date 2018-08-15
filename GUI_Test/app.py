#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""

from threading import Timer
from datetime import datetime
from csv import reader, writer
from flask import Flask, render_template, request, redirect
from file import dictionary


APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')

LEGACY_DIC = dictionary.read_legacy()
SERIALS = dictionary.read()
LOCATIONS = dictionary.read_locations()
CALLSIGNS = dictionary.read_callsigns()
SETTINGS = dictionary.read_settings()
LOG = []


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

    # s = Timer(5.0, save)
    # s.daemon = True

    w = writer(open("logs.csv", 'w'))

    main_keys = [
        'name',
        'sender',
        'receiver',
        'time',
        'duty'
    ]

    # print('log: ', LOG)

    for ret in LOG:

        test = ret
        # print('ret', ret)
        # print('test', test)

        lst = []
        for key in main_keys:
            # print("key ", key)
            lst.append(test[key])
            # del test[key]
        inn_lst = []
        for serial, val in test.items():
            inn_lst.append(serial+': '+val)

        lst.append('; '.join(inn_lst))

        w.writerow(lst)
    # s.start()
    # print("Saved")


@APP.route('/')
@APP.route('/transmission')
def display_main():
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/transmission/MESSAGE')
def display_message():
    return render_template('MESSAGE.html', serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS, callsigns=CALLSIGNS)


@APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    return render_template('abstracted_return.new.html',
                           return_type=rtrn_type, serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS, callsigns=CALLSIGNS)


@APP.route('/notes')
def display_notes():
    return render_template('notes.html')


@APP.route('/text')
def display_text():
    return render_template('texttest.html')


@APP.route('/settings/<setting>/', methods=['POST'])
def abstracted_updating_settings(setting):
    SETTINGS[setting] = request.form['name']
    update_setting()
    return redirect(request.form['page'])


@APP.route('/settings')
def display_settings():
    return render_template('settings_page.html', serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS)


def update_setting():
    dictionary.save_settings(SETTINGS)


@APP.route('/transmission/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):
    # print(rtrn_type)
    # print(request.form)
    ret = {}
    ret.update({'name': rtrn_type})
    ret.update({'sender': request.form['sender']})
    ret.update({'receiver': request.form['receiver']})
    ret.update({'duty': request.form['Duty']})
    ret.update({'time': datetime.today().strftime('%d%H%M')})

    print('ret inint ', ret)

    if rtrn_type == "MESSAGE":
        ret.update({'msg': request.form['msg']})
        # print(ret)
    else:
        for serial in LEGACY_DIC[rtrn_type]:
            ret.update({serial: request.form[serial]})
    # print("ret: ", ret)
    LOG.append(ret)
    #LOG.insert(0, (ret))
    print('\n\nreturn logged: ', LOG)
    # save()
    return render_template("log_frame.html", ret=ret)


@APP.route('/log')
def display_log():
    return render_template("log_test.html", log=LOG)


@APP.route('/log/<index>')
def test_log(index):
    try:
        index = int(index)
        return render_template("log_frame.html", ret=LOG[index])
    except:
        return "<h1>ERROR</h1>"


if __name__ == '__main__':
    # save()
    APP.run(debug=True)
