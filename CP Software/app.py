#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""
import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from file import File, SaveTimer, backup
from flask_compress import Compress
from threading import Thread
from time import sleep

APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')

Compress(APP)

SERIALS = File.read_dic()
LOCATIONS = File.read_locations()
CALLSIGNS = File.read_callsigns()
SETTINGS = File.read_settings()
DB_CONN = File.db_connect(SETTINGS)
GAME_CONN = File.db_connect({'DB_FILE_NAME':'resources/static/db/game.db', 'DB_TABLE_NAME':"'tetris'"})

File.generate_css_min()


@APP.route('/')
@APP.route('/transmission')
def transmission_shell():
    """ Renders the return shell """
    return render_template('transmission.html', serials_def=SERIALS)


@APP.route('/transmission/<rtrn_type>')
def transmission_return(rtrn_type):
    """ Renders the internal return submission form
    (Message has a special page)
    """

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
def notes():
    """ Renders the notes page """
    return render_template('notes.html')


@APP.route('/settings/update/', methods=['POST'])
def settings_general_update_post():
    """ handles the general setting changes (POST) """
    try:
        for key, val in request.form.to_dict().items():
            SETTINGS[key] = val
        update_setting()
    except Exception as e: # If an error is thrown please create an issue with the error!
        print("An error has occured, please create an issue on the github with the following:\n",e)
    return ""


@APP.route('/settings')
def settings_shell():
    """ Renders the settings shell """
    return render_template('settings/settings_page.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS)


@APP.route('/settings/updatelist/<list_name>', methods=['POST'])
def settings_updatelist_post(list_name):
    """
    updates the lists in the settings page (Locations and Callsigns)
    """
    if list_name.upper() == "LOCATIONS":
        global LOCATIONS
        LOCATIONS = request.form['lst'].split('\n')
        File.save_Locations(LOCATIONS)

    elif list_name.upper() == "CALLSIGNS":
        global CALLSIGNS
        CALLSIGNS = request.form['lst'].split('\n')
        File.save_callsigns(CALLSIGNS)

    return ""



@APP.route('/settings/locs')
def settings_locations():
    """ Renders the locations edit page """
    return render_template('settings/list_edit.html',
                           data=LOCATIONS)


@APP.route('/settings/callsigns')
def settings_callsigns():
    """ Renders the callsings edit page """
    return render_template('settings/list_edit.html',
                           data=CALLSIGNS)


@APP.route('/settings/general')
def settings_general():
    """ Renders the general settings form """
    return render_template('settings/settings_general.html',
                           settings=SETTINGS)


@APP.route('/settings/info')
def settings_info():
    """ Renders the Product info Page """
    return render_template('settings/product_info.html')

@APP.route('/settings/download_log')
def settings_download_log():
    """ downloads the LOG db file """

    return redirect("/"+SETTINGS['DB_FILE_NAME'].replace("resources/static/",""))


@APP.route('/settings/action/', methods=['POST'])
def settings_action_post():
    """ handles delete log action
     (request is in a form to prevent the page being accidentally pre-rendered by google and deleting log )"""
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

def get_new_log_name(lname=None):
    """Gets old db name and creates a new one with a number higher
    eg: log1.db -> log2.db
    """
    if not lname:
        lname = SETTINGS['DB_FILE_NAME']

    path = 'resources/static/db/LOG_'
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

@APP.route('/games/tetris')
def game_tetris():
    """ returns the tetris game """
    return render_template('games/tetris.html')


def update_setting():
    """ sub function to update the settings """
    File.save_settings(SETTINGS)


@APP.route('/transmission/<rtrn_type>', methods=['POST'])
def transmission_return_post(rtrn_type):
    """ handles the return submission (POST) returns same page as log (for printing) """
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
    return log_detail('init')



def convert_newlines(line):
    """ replaces new lines (\n) with <br> to be displayed in html """
    new_content = []
    for i in line.split('\n'):
        if '\r' in i:
            i = i[:-1]
        if i:
            new_content.append(i)
    new_content.append('')
    return '<br>'.join(new_content)


@APP.route('/log')
def log_shell():
    """loads the log shell"""
    log = File.load_log(DB_CONN)
    return render_template('log/log_edit_new.html', serials_def=SERIALS, log=log, callsigns=CALLSIGNS)


@APP.route('/log/<log_id>')
def log_detail(log_id):
    """ Renders the log detail page for display inside the log shell """
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
            return "<h1 style='text-align:center; padding-top: 20px;'>Log file incorrect</h1>"

    except IndexError:
        return "<h1>ERROR</h1><p>There are no logs to display</p>"


@APP.route('/edit_return')
def edit_return():
    """ Renders the edit return page """
    return render_template('returns/edit_return.html', serials_def=SERIALS)


@APP.route('/edit_return/<rtrn_type>')
def edit_return_serials(rtrn_type):
    """ Renders the edit return form """
    return render_template('edit.html',
                           return_type=rtrn_type,
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS,
                           callsigns=CALLSIGNS)


@APP.route('/edit_return/info')
def edit_return_info():
    """ Renders the edit return info form """
    return render_template('returns/edit_return_info.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS)


@APP.route('/edit_return/<action>', methods=['POST'])
@APP.route('/update', methods=['POST'])
def edit_return_post(action):
    """handles the POST from settings page to edit the serials structure"""
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
def log_edit_detail(log_id):
    """ Renders the log edit form """
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
def log_actions_post(action, log_id):
    """Handles the POST from the log edit form"""
    if action == 'edit':
        edit_log_by_id(log_id)
        return ""
    elif action == 'delete':
        File.delete_log_byID(DB_CONN, request.form.to_dict()['logID'])
        return ""


def edit_log_by_id(log_id):
    """Sub function to help edit the log based on it's id"""
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
def game_minesweeper():
    """returns the minesweeper game"""
    return render_template("games/minesweeper.html")


@APP.route('/log/query', methods=['POST'])
def log_query_post():
    """Handles the post from the query / search function on the log page"""
    # print(request.form.to_dict())
    x = File.load_log_query(DB_CONN, request.form.to_dict())
    # print(list(x))
    return render_template("log/log_innertable_list.html", log=list(x))




# UPLOADING DB
@APP.route('/settings/log_upload', methods = ['POST'])
def setting_upload_log():
    """Handles the file upload"""
    if 'file' in request.files:
        f = request.files['file']

        if f.filename[-3:]=='.db':
            SETTINGS['DB_FILE_NAME'] = get_new_log_name()
            update_setting()
            f.save("resources/static/db/"+secure_filename(SETTINGS['DB_FILE_NAME'].replace("resources/static/db/", "")))
            global DB_CONN
            DB_CONN = File.db_connect(SETTINGS)

        else:
            print("Didn't upload DB correctly")
            return "<h1>Incorrect File Type</h1>"
    else:
        return "<h1>Didn't upload a file</h1>"

    return redirect("/settings")

@APP.route('/settings/sitemap', methods = ['GET'])
def setting_sitemap_generate():
    """Generates a site map of all the existing pages"""
    raw = list()
    map = str(APP.url_map)
    map = map.replace("Map([","").replace(">])", "")
    for x in map.split(">,"):
        raw.append(x.split("<Rule ")[1])
    raw = sorted(raw)

    groupedSites = dict()

    for site in raw:

        site = site.split(") -> ")
        func = site.pop(1)
        url, setts = site[0].replace("'","").split(" (")
        setts = setts.replace("OPTIONS, ","").replace(", OPTIONS", "").replace(", HEAD","").replace("HEAD, ","")


        breakdown = url.split("/")
        key = breakdown[1]
        val = "/"+"/".join(breakdown[2:])

        combo = [val,setts,func]

        if not (key == "" or key == "<path:filename>"):
            if key in groupedSites:
                groupedSites[key].append(combo)
            else:
                groupedSites.update({key:[combo]})



    response = render_template("settings/sitemap.html",sites=groupedSites,raw=raw)

    return response


@APP.errorhandler(500)
def handle_500_error(e):
    """Custom error page for server / Internal error"""
    err = str(e).replace(" ","%20")
    print(err)
    return "Oops...<br>Please send "+\
           '<a href="mailto:rlambinon19@knox.nsw.edu.au?subject=CP%20BUG&body=ERROR:%20'+\
           err+'">'+\
           "rlambinon19@knox.nsw.edu.au</a> "+\
           "an email with: <br>"+str(e)


@APP.route('/games/tetris/', methods = ['POST'])
def tetris_score_update():
    x = request.form.to_dict()
    game_data = [x['name'], x['rank'], x['pl'], x['score'], int(datetime.today().strftime('%Y'))]
    GAME_CONN.new_return(game_data)
    return ""

@APP.route('/games/tetris/scores', methods = ['GET'])
def tetris_get_score():
    x = GAME_CONN.read_game_score(entries=30)
    lst = list()
    for count, i in enumerate(x):
        lst.append(
            {
                "ID":count+1,
                "Name":i[1],
                "Rank":i[2],
                "Pl":i[3],
                "Score":i[4],
                "Time":i[5]
            }
        )
    #return ""
    return jsonify(lst)

@APP.route('/games/tetris/lowest', methods = ['GET'])
def tetris_get_lowest():
    x = GAME_CONN.read_game_score(entries=30)
    lst = list()
    for count, i in enumerate(x):
        lst.append(
            {
                "ID":count+1,
                "Name":i[1],
                "Rank":i[2],
                "Pl":i[3],
                "Score":i[4],
                "Time":i[5]
            }
        )
    #return ""
    return jsonify(lst[-1])

@APP.route('/instructions')
def instructions():
    """ Renders the instructions page """
    return render_template('instructions.html')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@APP.route('/settings/shutdown/', methods=['POST'])
def shutdown():
    shutdown_server()

def open_chrome():
    sleep(1)
    os.system("/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --kiosk http://0.0.0.0:80/")
    os.system("""osascript -e 'tell application "Google Chrome" to activate'""")

def start():
    logging.info("Starting Backup Daemon")
    save = SaveTimer(1800, backup)

    logging.info("Starting Server")
    APP.jinja_env.cache = {}  # creates unlimited cache size (so each page can be cached)

    DEBUG = False  # Changes launch settings
    Thread(target=open_chrome).start()
    try:
        if not DEBUG:
            print("Running")
            APP.run(host='0.0.0.0', debug=False, port=80, threaded=True)
            print("Terminating")
        else:
            raise Exception
    except PermissionError:
        print("Could not use port 80 (use sudo to use port 80)")
        APP.run(host='0.0.0.0', debug=False, port=8080, threaded=True)

    except Exception as e:
        if e == "":
            APP.run(host='0.0.0.0', debug=True, port=8080, threaded=True)
        else:
            logging.exception("The server encountered a problem")

    finally:
        logging.info("Stopping Server")
        save.stop()

if __name__ == '__main__':
    logging.basicConfig(filename='eventLog.log', filemode='a', level=logging.DEBUG)
    logging.info(f"Initial startup of server at {datetime.now()}")
    try:
        start()
    except Exception as e:
        logging.exception("This is why it crashed: ")


