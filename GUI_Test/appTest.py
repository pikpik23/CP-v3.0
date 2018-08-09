from flask import Flask, render_template
from read_dictionary import dictionary

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html', test_var='\nHi from python')


@app.route('/table')
def display_table():
    lel = "LOCSTAT"
    x = dictionary.read()
    for k, v in x[lel].items():
        print(k)
        print(v)
    return render_template('tables_test.html', serials_def=x)


if __name__ == '__main__':
    app.run(debug=True)
