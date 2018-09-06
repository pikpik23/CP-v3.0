#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""

from datetime import datetime
from flask import Flask, render_template, request, redirect
from file import File
from flask_compress import Compress


APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')
Compress(APP)

SERIALS = File.read_dic()
LOCATIONS = File.read_locations()
CALLSIGNS = File.read_callsigns()
SETTINGS = File.read_settings()
LOG = File.load_log()

File.generate_css_min()


@APP.route('/')
@APP.route('/transmission')
def display_return_frame():
    """ Renders the return frame """
    return render_template('transmission.html', serials_def=SERIALS)


@APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    """ Renders the internal return form """

    if rtrn_type == 'MESSAGE':
        return render_template('returns/MESSAGE.html',
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS)
    else:
        return render_template('returns/inner_return.html',
                               return_type=rtrn_type,
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS)

@APP.route('/notes')
def display_notes():
    """ Renders the notes page """
    return render_template('notes.html')


@APP.route('/settings/<setting>/', methods=['POST'])
def abstracted_updating_settings(setting):
    """ handles setting changes (POST) then reloads page """
    SETTINGS[setting] = request.form['name']
    update_setting()
    return ""


@APP.route('/settings')
def display_settings():
    """ Renders the settings page """
    return render_template('settings/settings_page.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS)


@APP.route('/settings/locs')
def display_settings_locations():
    """ Renders the locations edit field """
    return render_template('locations_edit.html',
                           locs=LOCATIONS)


@APP.route('/settings/general')
def display_settings_general():
    """ Renders the general settings field """
    return render_template('settings/settings_general.html',
                           settings=SETTINGS)


@APP.route('/settings/info')
def display_info():
    """ Renders the Product info Page """
    return render_template('product_info.html')


@APP.route('/games/tetris')
def display_tetris():
    """ Renders the tetris Page """
    return render_template('games/tetris.html')


@APP.route('/settings/locs', methods=['POST'])
def update_settings_locations():
    File.save_Locations(request.form['locs'])
    # print(LOCATIONS)
    # print(request.form['locs']).split('\n')
    # print(request.form['locs'].split('\n'))
    global LOCATIONS
    LOCATIONS = request.form['locs'].split('\n')
    return ''


def update_setting():
    """ sub function to update the settings """
    File.save_settings(SETTINGS)


@APP.route('/transmission/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):
    """ handles the return submission (POST) returns same page """
    # print(request.form)
    ret = {}
    ret.update({'net': request.form['net']})
    ret.update({'name': rtrn_type})
    ret.update({'sender': request.form['sender']})
    ret.update({'receiver': request.form['receiver']})
    ret.update({'duty': request.form['duty']})
    ret.update({'time': datetime.today().strftime('%d%H%M')})

    if rtrn_type == "MESSAGE":
        ret.update({'msg': convert_newlines(request.form['msg'])})

    else:
        for serial in SERIALS[rtrn_type]:
            try:
                ret.update({serial: convert_newlines(request.form[serial])})
            except KeyError:
                ret.update({serial: ''})

    LOG.insert(0, (ret))
    File.save_log(ret)
    # return ""
    return test_log('init')


def convert_newlines(line):
    """ replaces new lines with <br> to be displayed in html """
    new_content = []
    for i in line.split('\n'):
        if '\r' in i:
            i = i[:-1]
        new_content.append(i)
    new_content.append('')
    return '<br>'.join(new_content)


@APP.route('/log')
def display_log():
    """ Renders the log_frame """
    return render_template("log/log_test.html", log=list(reversed(File.load_log())))


@APP.route('/log/<log_id>')
def test_log(log_id):
    """ Renders the return form """
    # print(LOG[int(logID)])
    if log_id == 'init':
        log_id = File.get_first()

    try:
        # index = int(logID)

        return render_template("log/log_frame.html",
                               ret=File.load_log(log_id=log_id)[0])

    except IndexError:
        return "<h1>ERROR</h1><p>There are not logs</p>"


@APP.route('/edit_return')
def display_edit_return():
    """ Renders the edit return page """
    return render_template('returns/edit_return.html', serials_def=SERIALS)


@APP.route('/edit_return/<rtrn_type>')
def display_abstracted_serials(rtrn_type):
    """ Renders the edit return page """
    return render_template('edit.html',
                           return_type=rtrn_type,
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS,
                           callsigns=CALLSIGNS)


@APP.route('/edit_return/info')
def display_edit_return_info():
    """ Renders the edit return info page """
    return render_template('returns/edit_return_info.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS)


@APP.route('/edit_return/<action>', methods=['POST'])
@APP.route('/update', methods=['POST'])
def test_update(action):

    if action == "return_update":
        x = request.form.to_dict()
        if 'add' in x:
            print(x['add'])

        elif 'rem' in x:
            SERIALS.pop(x['rem'])
            File.save_dic(SERIALS)

        else:
            print(x)

    else:
        outdic = dict()
        for key, row in request.form.to_dict().items():

            name, right = key.split('[')
            id = right[:-1]
            if id == 'options':
                # print(row)
                row = row.split(', ')

            if name in outdic.keys():
                outdic[name].update({id:row})
            else:
                outdic.update({name:{id:row}})
        SERIALS.update({action:outdic})
        File.save_dic(SERIALS)

    return ""


@APP.route('/log/edit/<index>')
def test_log_edit(index):
    """ Renders the return form """
    index = int(index)
    print(LOG[index])
    try:
        index = int(index)
        return render_template("returns/abstracted_return.edit.html",
                               return_type=LOG[index]['name'],
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS,
                               ret=LOG[index])
    except IndexError:
        return "<h1>ERROR</h1><p>That is not a valid log ID</p>"


@APP.route('/games/minesweeper')
def minesweeper():
    return render_template("games/minesweeper.html")


if __name__ == '__main__':

    APP.jinja_env.cache = {}
    # below is wip
    # File.pre_merge()
    try:
        APP.run(host='0.0.0.0', debug=True, port=8080, threaded=True)
    except PermissionError:
        APP.run(host='0.0.0.0')
