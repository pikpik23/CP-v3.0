"""
Set up settings for CP v3.0

Don't use this to build app (More things are added by script)
use the createApp.sh found in the dist folder
Requires active developer signature to complete properly
"""

from setuptools import setup

APP = ['app.py']
APP_NAME = "Command Post V3.2"
DATA_FILES = ['CP.icns','resources', 'file.py',"CPL.gif"]
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'CP.icns',
    'packages': ["PIL",
                 "flask",
                 "jinja2",
                 "markupsafe",
                 "werkzeug",
                 "mgrs",
                 "tkinter",
                 #"libmgrs",
                 #"ctypes",
                 #"atexit",
                 #"sysconfig",
                 #"math",
                 #"os",
                 #"re",
                 #"sys",
                 # "argparse",
                 #"click",
                 # "itsdangerous",
                 #"wsgiref",
                 #"quart",
                 #"tox",
                 #"pip",
                 #"python3.7.0",
                 #"flask-compress",
                 #"flask-static-compress",
                 #"jsmin",
                 #"csscompressor",
                 #"flask-compress",
                 "py2app"],
        'plist': {
                'CFBundleName': APP_NAME,
                'CFBundleDisplayName': APP_NAME,
                'CFBundleGetInfoString': "Portaloo Duty INC.",
                'CFBundleIdentifier': "com.RenierLambinon.CommandPostV3.0",
                'CFBundleVersion': "3.2",
                'CFBundleShortVersionString': "3.2",
                'NSHumanReadableCopyright': u"Copyright © 2019, Renier Lambinon and Trent Muskens",
                'NSSystemAdministrationUsageDescription': "Needs this to lock port 80"
            }
        }

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)