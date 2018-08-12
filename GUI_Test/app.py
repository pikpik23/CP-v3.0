"""
The main file for the CP site

All request handling is done from here
"""

from flask import Flask, render_template, request, redirect
from read_dictionary import dictionary

APP = Flask(__name__, template_folder='templates',
            static_folder='static', static_url_path='')

LEGACY_DIC = dictionary.read_legacy()
SERIALS = dictionary.read()
LOCATIONS = dictionary.read_locations()
SETTINGS = dictionary.read_settings()


@APP.route('/')
def direct():
    return redirect("/transmission", code=302)


@APP.route('/table')
def display_table():
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/notes')
def display_notes():
    return render_template('notes.html')


@APP.route('/transmission')
def display_main():
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    return render_template('abstracted_return.new.html', return_type=rtrn_type, serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS)


@APP.route('/transmission/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):
    ret = {}
    for serial in LEGACY_DIC[rtrn_type]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=LEGACY_DIC)


@APP.route('/settings/<setting>/', methods=['POST'])
def abstracted_updating_settings(setting):
    print('updating '+setting+' officer to: ' + request.form['name'])
    SETTINGS[setting] = request.form['name']
    return abstracted_return('MESSAGE')


def update_setting(setting, value):
    SETTINGS.update({setting: value})
    dictionary.save_settings(SETTINGS)


if __name__ == '__main__':
    APP.run(debug=True)
