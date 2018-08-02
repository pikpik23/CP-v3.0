from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# for the modules
import sys
sys.path.append("./modules")

from ReadWrite import readSheet, printValues, editRecord, ex_Read_Print
from common import init







if __name__ == '__main__':
	init()

	ex_Read_Print()
	#ex_editRecord()