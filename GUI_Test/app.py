#!/usr/local/bin/python3
"""
The main file for the CP site

All request handling is done from here
"""

# from threading import Timer
# test
from datetime import datetime
from flask import Flask, render_template, request, redirect
from file import file


APP = Flask(__name__, template_folder='resources/templates',
            static_folder='resources/static', static_url_path='')

LEGACY_DIC = file.read_legacy()
SERIALS = file.read_dic()
LOCATIONS = file.read_locations()
CALLSIGNS = file.read_callsigns()
SETTINGS = file.read_settings()
LOG = file.load_log()


@APP.route('/')
@APP.route('/transmission')
def display_return_frame():
    """ Renders the return frame """
    return render_template('index_test.html', serials_def=LEGACY_DIC)


@APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    """ Renders the internal return form """

    if rtrn_type == 'MESSAGE':
        return render_template('MESSAGE.html',
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS)
    else:
        return render_template('abstracted_return.new.html',
                               return_type=rtrn_type,
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS)


''' @APP.route('/transmission/<rtrn_type>')
def abstracted_return(rtrn_type):
    """ Renders the internal return form """
    if rtrn_type == 'MESSAGE':
        return render_template('MESSAGE.html',
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS)
    else:
        return render_template('abstracted_return.new.html',
                               return_type=rtrn_type,
                               serials_def=SERIALS,
                               locs=LOCATIONS,
                               settings=SETTINGS,
                               callsigns=CALLSIGNS) '''


@APP.route('/notes')
def display_notes():
    """ Renders the notes page """
    return render_template('notes.html')


@APP.route('/settings/<setting>/', methods=['POST'])
def abstracted_updating_settings(setting):
    """ handles setting changes (POST) then reloads page """
    SETTINGS[setting] = request.form['name']
    update_setting()
    return redirect(request.form['page'])


@APP.route('/settings')
def display_settings():
    """ Renders the settings page """
    return render_template('settings_page.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS)


def update_setting():
    """ sub function to update the settings """
    file.save_settings(SETTINGS)


@APP.route('/transmission/<rtrn_type>', methods=['POST'])
def abstracted_return_return(rtrn_type):
    """ handles the return submissin (POST) returns same page """

    ret = {}
    ret.update({'name': rtrn_type})
    ret.update({'sender': request.form['sender']})
    ret.update({'receiver': request.form['receiver']})
    ret.update({'duty': request.form['Duty']})
    ret.update({'time': datetime.today().strftime('%d%H%M')})

    if rtrn_type == "MESSAGE":
        ret.update({'msg': convert_newlines(request.form['msg'])})

    else:
        for serial in LEGACY_DIC[rtrn_type]:
            try:
                ret.update({serial: convert_newlines(request.form[serial])})
            except KeyError:
                ret.update({serial: ''})

    LOG.insert(0, (ret))
    file.save_log(LOG)
    return redirect("/")
    # return abstracted_return(rtrn_type)


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
    return render_template("log_test.html", log=LOG)


@APP.route('/log/<index>')
def test_log(index):
    """ Renders the return form """
    try:
        index = int(index)
        return render_template("log_frame.html", ret=LOG[index])
    except IndexError:
        return "<h1>ERROR</h1><p>That is not a valid log ID</p>"


@APP.route('/edit_return')
def display_edit_return():
    """ Renders the edit return page """
    return render_template('edit_return.html', serials_def=SERIALS)


@APP.route('/edit_return/<rtrn_type>')
def display_abstracted_serials(rtrn_type):
    """ Renders the edit return page """
    return render_template('test_edit.html',
                           return_type=rtrn_type,
                           serials_def=SERIALS,
                           locs=LOCATIONS,
                           settings=SETTINGS,
                           callsigns=CALLSIGNS)


@APP.route('/edit_return/info')
def display_edit_return_info():
    """ Renders the edit return info page """
    return render_template('edit_return_info.html',
                           serials_def=SERIALS,
                           locs=LOCATIONS)


@APP.route('/edit_return/<action>', methods=['POST'])
@APP.route('/update', methods=['POST'])
def test_update(action):
    # print(request.form)

    # dict = request.form.to_dict()
    # print(action)
    tmpDic = request.form.to_dict()
    rtrn_type = tmpDic['return_type']
    rtrn_serial = tmpDic['serial']

    # print(SERIALS[rtrn_type][rtrn_serial])

    # print(tmpDic)

    inner_dic = {}
    for name, val in tmpDic.items():
        inner_dic.update({name: val})

    SERIALS[rtrn_type].update({rtrn_serial: {}})
    LEGACY_DIC.update({rtrn_type: {}})

    SERIALS[rtrn_type][rtrn_serial].update({name: val})

    SERIALS[rtrn_type][rtrn_serial].update({
        'desc': tmpDic['desc']
    })

    SERIALS[rtrn_type][rtrn_serial].update({
        "data_type": tmpDic['data_type']
    })

    if tmpDic['data_type'] == 'choice':
        x = tmpDic['options']
        x = x.replace('<span style="font-size: 11pt;">', '')
        x = x.replace('</span>', '')
        x = x.split(', ')
        SERIALS[rtrn_type][rtrn_serial].update({
            "options": x
        })

    LEGACY_DIC[rtrn_type].update({'desc': tmpDic['desc']})

    # deleting things
    """
    del dic[rtrn_type]
    or 
    dic.pop(rtrn_type)
    """

    #  print(LEGACY_DIC[rtrn_type][rtrn_serial])
    # print(SERIALS[rtrn_type][rtrn_serial])

    return "Recieved"


if __name__ == '__main__':

    APP.run(host='0.0.0.0', debug=True)
