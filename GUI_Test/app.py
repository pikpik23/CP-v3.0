#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""

from flask import Flask, render_template, request, redirect
from read_dictionary import dictionary
from datetime import datetime

APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')

LEGACY_DIC = dictionary.read_legacy()
SERIALS = dictionary.read()
LOCATIONS = dictionary.read_locations()
SETTINGS = dictionary.read_settings()
LOG = []


@APP.route('/')
@APP.route('/transmission')
def display_main():
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/transmission/MESSAGE')
def display_message():
    return render_template('MESSAGE.html', serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS)


@APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    return render_template('abstracted_return.new.html',
                           return_type=rtrn_type, serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS)


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
    print(rtrn_type)
    print(request.form)
    ret = {}
    ret.update({'name': rtrn_type})
    ret.update({'sender': request.form['sender']})
    ret.update({'reciver': request.form['reciver']})
    ret.update({'time': datetime.today().strftime('%d%H%M')})

    if rtrn_type == "MESSAGE":
        ret.update({'msg': request.form['msg']})
    else:
        for serial in LEGACY_DIC[rtrn_type]:
            ret.update({serial: request.form[serial]})
    LOG.insert(0, ret)

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
    APP.run(debug=True)
