from flask import Flask, render_template, request
from read_dictionary import dictionary

app = Flask(__name__, template_folder='test_templates',
            static_folder='test_templates/test_static', static_url_path='')


@app.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')


@app.route('/table')
def display_table():
    return render_template('tables_test.html', serials_def=dictionary.read())


@app.route('/testIndex')
def display_index():
    return render_template('index_test.html', serials_def=dictionary.read())


@app.route('/return')
def return_page():
    return render_template('return.html')


@app.route('/return', methods=['POST'])
def get_data():

    text = request.form["content"]
    print(text)
    processed_text = text.upper()
    return processed_text


@app.route('/maintdem')
def maint_test():
    return render_template('maint_test.html')


@app.route('/maintdem', methods=['POST'])
def maint_test_return():

    ret = {}
    for serial in dictionary.read()["MAINTDEM"]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=ret)


@app.route('/abret')
def abstracted_return():
    rtrn_type = "MAINTDEM"
    serials = dictionary.read()
    return render_template('abstracted_return.html', return_type=rtrn_type, serials_def=serials)


@app.route('/abret', methods=['POST'])
def abstracted_return_return():

    ret = {}
    for serial in dictionary.read()["MAINTDEM"]:
        ret.update({serial: request.form[serial]})
    return render_template('return_display_test.html', serials_def=ret)


if __name__ == '__main__':
    app.run(debug=True)
