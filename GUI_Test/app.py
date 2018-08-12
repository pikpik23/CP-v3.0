"""
The main file for the CP site

All request handling is done from here
"""

from flask import Flask, render_template, request
from read_dictionary import dictionary

APP = Flask(__name__, template_folder='templates',
            static_folder='static', static_url_path='')

LEGACY_DIC = dictionary.read_legacy()
SERIALS = dictionary.read()
LOCATIONS = dictionary.read_locations()
SETTINGS = dictionary.read_settings()

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> parent of caf39e3... way too much css

@APP.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')

<<<<<<< HEAD
=======
>>>>>>> c29cc6e58a0230501216b12b2f39e9efba8e52ff
=======
>>>>>>> parent of caf39e3... way too much css

@APP.route('/table')
def display_table():
    return render_template('tables_test.html', serials_def=LEGACY_DIC)


<<<<<<< HEAD
<<<<<<< HEAD
@APP.route('/testIndex')
=======
@APP.route('/')
@APP.route('/transmission')
>>>>>>> c29cc6e58a0230501216b12b2f39e9efba8e52ff
=======
@APP.route('/testIndex')
>>>>>>> parent of caf39e3... way too much css
def display_main():
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/testIndex/<rtrn_type>')
def abstracted_return(rtrn_type):
    return render_template('abstracted_return.new.html', return_type=rtrn_type, serials_def=SERIALS, locs=LOCATIONS, settings=SETTINGS)


@APP.route('/textIndex/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):
    ret = {}
    for serial in LEGACY_DIC[rtrn_type]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=LEGACY_DIC)


if __name__ == '__main__':
    APP.run(debug=True)
