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
import mgrs

SETTINGS = File.read_settings()
DB_CONN = File.db_connect(SETTINGS)

class convert:

    def __init__(self):
        self.m = mgrs.MGRS()

    def Cord(self, lat,long):
        return self.m.toMGRS(lat, long)

    def MGRS(self, code):
        return self.m.toLatLon(code)


if __name__ == "__main__":
    x = convert()