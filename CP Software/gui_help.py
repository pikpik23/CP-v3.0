# GUI Imports
from tkinter import *
from tkinter import font
from PIL import ImageTk, Image


# The Rest
import logging
import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, jsonify, url_for
from werkzeug.utils import secure_filename
from file import File, SaveTimer, backup
from flask_compress import Compress
from threading import Thread
from time import sleep
import requests
import socket
from requests import post

SETTINGS = File.read_settings()
DB_CONN = File.db_connect(SETTINGS)

def count_logs():

    x = DB_CONN.count_records()
    y=None
    if x != None:
        for i in x:
            try:
                y = i[0]
            finally:
                pass
            break
    return y


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        # IP = '127.0.0.1'
        IP = 'OFFLINE'
    finally:
        s.close()
    return str(IP)

def get_net_status():
    try:
        post("http://0.0.0.0/api/v1.0/status")
        return "Online"
    except requests.exceptions.ConnectionError:
            return "Offline"

class helpgui:
    def __init__(self):
        self.root = Tk()
        self.root.title("Command Post V3.0 Help")
        self.root.geometry("249x324+600+150")
        self.root.resizable(width=False, height=False)

        # Generate Frame
        self.gen_frame()

    def gen_frame(self):

        # Fonts
        h1 = font.Font(family='Helvetica', size=24, weight='bold')
        name = font.Font(family='Helvetica', size=16, weight='bold')
        value = font.Font(family='Helvetica', size=16)

        #Status label
        self.status_text = Label(self.root, font=h1, anchor='center')
        self.status_text['text'] = " Help "

        self.status_text.grid(column=0,row=0, pady=10, columnspan=2)

        # Center everything
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        dic = {
            'IP Address':get_ip(),
            'Status': get_net_status(),
            'Server Time': datetime.today().strftime('%d%H%M'),
            'Log Entries': count_logs(),
            'S/W Version': 3.0
        }

        self.items_dict = dict()
        x = 1
        for key, val in dic.items():

            label_key = Label(self.root, font=name)
            label_key['text'] = str(key)+": "
            label_key.grid(column=0, row=x, sticky='e')

            label_val = Label(self.root, font=value)
            label_val['text'] = str(val)
            label_val.grid(column=1, row=x, sticky='w')


            self.items_dict.update({key:[label_key,label_val]})

            x+=1

        help_label = Label(self.root, font=value, wraplength=230)
        help_label['text'] = \
        "\n" \
        "Type the IP Address into Chrome to connect to the CP server\n\n" \
        "If you need help Contact CUO Lambinon or CUO Muskens"

        help_label.grid(column=0, row=x, columnspan=2)

        # run fix for gui glitch
        self.root.after_idle(self.ready)
        # start the event loop
        self.root.mainloop()

    def ready(self):
        # resize to fix button glitch
        self.root.geometry("250x325+300+150")

if __name__ == "__main__":
    helpgui()