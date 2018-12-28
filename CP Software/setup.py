"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['app.py']
APP_NAME = "Command Post V3.0"
DATA_FILES = ['CP.icns','resources', 'file.py']
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'CP.icns',
    'packages': ["flask",
                 "jinja2",
                 "markupsafe",
                 "werkzeug",
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
            'CFBundleGetInfoString': "Portaloo Duty FTW",
            'CFBundleIdentifier': "com.RenierLambinon.CommandPostV3.0",
            'CFBundleVersion': "3.0-Alpha",
            'CFBundleShortVersionString': "3.0-Alpha",
            'NSHumanReadableCopyright': u"Copyright © 2019, Renier Lambinon and Trent Muskens"
        }
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)