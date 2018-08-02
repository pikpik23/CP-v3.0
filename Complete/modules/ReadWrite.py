# Read Write function
# dependant on main.py function

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# for the modules
import sys
sys.path.append("./modules")

import common




#
# Read
#

def readSheet(range = ''):
    if not range:
        range = common.totalRange

    '''
    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', common.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    '''
    
    # Call the Sheets API
    result = common.service.spreadsheets().values().get(
        spreadsheetId=common.SPREADSHEET_ID,
        range=range).execute()
    return result.get('values', [])


#
# Print
#

def printValues(table = '', header=["Names", "Number"]):
    if not table:
        table = readSheet()

    print(", ".join(header),end=":\n")
    for row in table:
        try:
            print(", ".join(row))
            #print(u'%s, %s' % (row[0], row[1]))
        
        # should not be needed but just for incase
        except IndexError:
            if len(row) == 1:
                print(row[0])
            else:
                print("Blank")

#
# Edit Record
#

def editRecord(record, range = ''):
    if not range:
        range = common.totalRange

    '''
    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', common.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))
    '''

    table = {
        'values': record
    }

    # Call the Sheets API
    result = common.service.spreadsheets().values().update(
        spreadsheetId=common.SPREADSHEET_ID,
        range=range,
        valueInputOption=common.value_input_option,
        body=table
        ).execute()
