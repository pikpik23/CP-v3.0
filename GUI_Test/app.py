#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from file import File
from flask_compress import Compress

APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')

Compress(APP)

SERIALS = File.read_dic()
LOCATIONS = File.read_locations()
CALLSIGNS = File.read_callsigns()
SETTINGS = File.read_settings()
DB_CONN = File.db_connect(SETTINGS)

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


@APP.route('/settings/update/', methods=['POST'])
def abstracted_updating_settings():
    """ handles setting changes (POST) then reloads page """
    try:
        for key, val in request.form.to_dict().items():
            SETTINGS[key] = val
        update_setting()
    except Exception as e: # If an error is thrown please create an issue with the error!
        print("An error has occured, please create an issue on the github with the following:\n",e)
    return ""


@APP.route('/settings')
def display_settings():
    """ Renders the settings page """
    return render_template('settings/settings_page.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS)


@APP.route('/settings/updatelist/<list_name>', methods=['POST'])
def update_list_settings(list_name: str) -> str:
    """
    updates the given settings
    """
    if list_name.upper() == 'LOCATIONS':
        global LOCATIONS
        LOCATIONS = request.form['lst'].split('\n')
        File.save_Locations(LOCATIONS)

    elif list_name.upper() == 'CALLSIGNS':
        global CALLSIGNS
        CALLSIGNS = request.form['lst'].split('\n')
        File.save_callsigns(CALLSIGNS)

    return ""


@APP.route('/settings/locs')
def display_settings_locations():
    """ Renders the locations edit field """
    return render_template('settings/list_edit.html',
                           data=LOCATIONS)


@APP.route('/settings/callsigns')
def display_settings_callsigns():
    """ Renders the locations edit field """
    return render_template('settings/list_edit.html',
                           data=CALLSIGNS)


@APP.route('/settings/general')
def display_settings_general():
    """ Renders the general settings field """
    return render_template('settings/settings_general.html',
                           settings=SETTINGS)


@APP.route('/settings/info')
def display_info():
    """ Renders the Product info Page """
    return render_template('product_info.html')

@APP.route('/settings/download_log')
def download_log():
    """ Renders the LOG """
    return redirect("/"+SETTINGS['DB_FILE_NAME'].replace("resources/static/",""))

@APP.route('/settings/action/', methods=['POST'])
def settings_actions():
    """ Renders the LOG """
    try:
        action = request.form.to_dict()['action']
    except KeyError:
        action = None
        return "Error Could not detect action"

    if action == "delete_log":
        SETTINGS['DB_FILE_NAME'] = get_new_log_name(SETTINGS['DB_FILE_NAME'])
        update_setting()
        global DB_CONN
        DB_CONN = File.db_connect(SETTINGS)

    return ""



@APP.route('/games/tetris')
def display_tetris():
    """ Renders the tetris Page """
    return render_template('games/tetris.html')


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

    # LOG.insert(0, (ret))
    File.save_log(DB_CONN, ret)
    # return ""
    return test_log('init')


def convert_newlines(line):
    """ replaces new lines with <br> to be displayed in html """
    new_content = []
    for i in line.split('\n'):
        if '\r' in i:
            i = i[:-1]
        if i:
            new_content.append(i)
    new_content.append('')
    return '<br>'.join(new_content)


@APP.route('/log')
def render_log_page():
    log = File.load_log(DB_CONN)
    return render_template('log/log_edit_new.html', serials_def=SERIALS, log=log)


@APP.route('/log/<log_id>')
def test_log(log_id):
    """ Renders the return form """
    # print(LOG[int(logID)])
    if log_id == 'init':
        # DEPRECIATED
        log_id = File.get_first(DB_CONN)

    try:
        log = File.load_log(DB_CONN, log_id=log_id)
        if log:
            return render_template("log/log_frame.html",
                                   ret=log)
        else:
            return "<h1 style='text-align:center; padding-top: 20px;'>Log Deleted</h1>"

    except IndexError:
        return "<h1>ERROR</h1><p>There are no logs to display</p>"


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

            if x['old']:
                SERIALS[x['add']] = SERIALS.pop(x['old'])
            else:
                SERIALS.update({x['add']: {'A': {'desc': 'default entry', 'data_type': 'short', 'options': ['']}}})
            File.save_dic(SERIALS)

        elif 'rem' in x:
            try:
                SERIALS.pop(x['rem'])
                File.save_dic(SERIALS)
            except KeyError:
                print("Tried to delete something that didn't exist")

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
                outdic[name].update({id: row})
            else:
                outdic.update({name: {id: row}})
        SERIALS.update({action: outdic})
        File.save_dic(SERIALS)

    return ""


@APP.route('/log/edit/<log_id>')
def test_log_edit(log_id):
    """ Renders the return form """
    log_id = int(log_id)
    try:
        index = int(log_id)
        return render_template("Edit_Log/edit_log_body.html",
                               return_type=File.load_log(DB_CONN, log_id=log_id)['name'],
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS,
                               ret=File.load_log(DB_CONN, log_id=log_id))

    except IndexError:
        return "<h1>ERROR</h1><p>That is not a valid log ID</p>"


@APP.route('/log/<action>/<log_id>', methods=['POST'])
def test_log_edit_submit(action, log_id):
    if action == 'edit':
        edit_log_by_id(log_id)
        return ""
    elif action == 'delete':
        File.delete_log_byID(DB_CONN, request.form.to_dict()['logID'])
        return ""


def edit_log_by_id(log_id):
    log = request.form.to_dict()

    ret = {}
    ret.update({'logID': log_id})
    ret.update({'name': log['name']})
    ret.update({'sender': log['sender']})
    ret.update({'receiver': log['receiver']})
    ret.update({'time': log['time']})
    ret.update({'duty': log['duty']})
    ret.update({'net': log['net']})

    if log['name'] == "MESSAGE":
        ret.update({'msg': convert_newlines(log['msg'])})

    else:
        for serial in SERIALS[log['name']]:
            try:
                ret.update({serial: convert_newlines(log[serial])})
            except KeyError:
                ret.update({serial: ''})

    File.save_log(DB_CONN, ret, update=True)

    return ""


@APP.route('/games/minesweeper')
def minesweeper():
    return render_template("games/minesweeper.html")


@APP.route('/log/query', methods=['POST'])
def getQuery():
    # print(request.form.to_dict())
    x = File.load_log_query(DB_CONN, request.form.to_dict())
    # print(list(x))
    return render_template("log/log_innertable_list.html", log=list(x))

def get_new_log_name(lname=None):
    if not lname:
        lname = SETTINGS['DB_FILE_NAME']

    path = 'resources/static/log/LOG_'
    extension = '.db'
    lname = lname.strip(path) # strip the path
    lname = lname.strip(extension) # strip db extension

    try:
        lname = int(lname)
        lname += 1
    except ValueError:
        print("can't turn the name into an int")

    new_lname = path+str(lname)+extension

    return new_lname


# UPLOADING DB
@APP.route('/settings/log_upload', methods = ['POST'])
def upload_file():

    if 'file' in request.files:
        f = request.files['file']

        if f.filename[-3:]=='.db':
            SETTINGS['DB_FILE_NAME'] = get_new_log_name()
            update_setting()
            f.save("resources/static/log/"+secure_filename(SETTINGS['DB_FILE_NAME'].replace("resources/static/log/LOG_", "")))
            global DB_CONN
            DB_CONN = File.db_connect(SETTINGS)
    return redirect("/settings")


if __name__ == '__main__':

    APP.jinja_env.cache = {}

    try:
        APP.run(host='0.0.0.0', debug=True, port=80, threaded=True)
    except PermissionError:
        print("Could not use port 80 (use sudo to use port 80)")
        APP.run(host='0.0.0.0', debug=True, port=8080, threaded=True)
