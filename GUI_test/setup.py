from setuptools import setup

APP = ['gui.py']
DATA_FILES = ["CPL.gif"]

OPTIONS = {'packages': ['PIL']}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)