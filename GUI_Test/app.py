from flask import Flask, render_template, request
from read_dictionary import dictionary

app = Flask(__name__, template_folder='templates',
            static_folder='static', static_url_path='')


@app.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')


@app.route('/table')
def display_table():
    return render_template('tables_test.html', serials_def=legacy_dictionary)


@app.route('/testIndex')
def display_main():
    return render_template('index_test.html', serials_def=legacy_dictionary)


@app.route('/testIndex/<rtrn_type>')
def abstracted_return(rtrn_type):
    return render_template('abstracted_return.new.html', return_type=rtrn_type, serials_def=detailed_dictionary, locs=locations, own_cs=callsign, duty=duty_officer)


@app.route('/textIndex/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):

    ret = {}
    for serial in legacy_dictionary[rtrn_type]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=ret)


if __name__ == '__main__':
    global legacy_dictionary, detailed_dictionary, locations, callsign, duty_officer
    legacy_dictionary = dictionary.read_legacy()
    detailed_dictionary = dictionary.read()
    locations = dictionary.read_locations()
    callsign, duty_officer = dictionary.read_settings()
    app.run(debug=True)
