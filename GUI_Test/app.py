from flask import Flask, render_template, request
from read_dictionary import dictionary

app = Flask(__name__, template_folder='templates',
            static_folder='static', static_url_path='')


@app.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')

@app.route('/table')
def display_table():
    return render_template('tables_test.html', serials_def=dictionary.read())

@app.route('/testIndex')
def display_main():
    return render_template('index_test.html', serials_def=dictionary.read())

@app.route('/testIndex/<rtrn_type>')
def abstracted_return(rtrn_type):
    serials = dictionary.read()
    return render_template('abstracted_return.html', return_type=rtrn_type, serials_def=serials)


@app.route('/testIndex/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):

    ret = {}
    for serial in dictionary.read()[rtrn_type]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=ret)

if __name__ == '__main__':
    app.run(debug=True)
