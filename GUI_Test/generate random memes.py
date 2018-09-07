from datetime import datetime
from flask import Flask, render_template, request, redirect
from file import File
from flask_compress import Compress
from random import choice
from app import *

CONTENT = ['aksdfhlks', 'repeat', 'idk', 'this is a test', 'sample data here', 'help', 'a LOT of tick bites']
NETS = ['ADMIN NET', 'UNIT NET', 'HQ NET']
CALLSIGNS = File.read_callsigns()
DUTY = ['Lambinon', 'Muskens', 'Lambinon']
SERIALS = File.read_dic()
RETURNS = ['MESSAGE']
for i in SERIALS:
    RETURNS.append(i)

def generate_data(rows):
    for generate in range(rows):
        generate_log()

def generate_log():
    rtrn_type = choice(RETURNS)
    ret = {}
    ret.update({'net': choice(NETS)})
    ret.update({'name': rtrn_type})
    ret.update({'sender': choice(CALLSIGNS)})
    ret.update({'receiver': choice(CALLSIGNS)})
    ret.update({'duty': choice(DUTY)})
    ret.update({'time': datetime.today().strftime('%d%H%M')})

    if rtrn_type == "MESSAGE":
        ret.update({'msg': choice(CONTENT)})

    else:
        for serial in SERIALS[rtrn_type]:
            try:
                ret.update({serial: choice(CONTENT)})
            except KeyError:
                ret.update({serial: ''})

    File.save_log(ret)

if __name__ == '__main__':
    rows = int(input("rows to generate: "))
    generate_data(rows)