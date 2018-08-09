from flask import Flask, render_template, request
from read_dictionary import dictionary

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')

@app.route('/table')
def display_table():
    return render_template('tables_test.html', serials_def=dictionary.read())

@app.route('/testIndex')
def display_main():
    return render_template('index_test.html', serials_def=dictionary.read())

if __name__ == '__main__':
    app.run(debug=True)
