from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
# remember to init from main otherwise values won't exist

def init():

	global SCOPES, SPREADSHEET_ID, value_input_option, totalRange, DataOption

	SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

	# The ID and range of a sample spreadsheet.
	SPREADSHEET_ID = '12T7Ub21E-gAlwtJRZdsu3cww-wwIOvdjP_plhMxUn-0' #My test sheet

	value_input_option = 'USER_ENTERED' #Leave this as is (it makes life easier)

	totalRange = 'Names!A2:B'

	DataOption='INSERT_ROWS'




	# Auth with google
	global service

	store = oauth_file.Storage('sheetsToken.json')
	creds = store.get()
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('sheets', 'v4', http=creds.authorize(Http()))
