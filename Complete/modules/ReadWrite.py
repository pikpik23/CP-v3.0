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

def readSheet(range = commmon.spreadSheetRange):

    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', common.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=common.SPREADSHEET_ID,
        range=range).execute()
    return result.get('values', [])


#
# Print
#

def printValues(values, header=["Names", "Number"]):
    if not values:
        print('No data found.')
    else:
        print(", ".join(header),end=":\n")
        for row in values:
            try:
                print(", ".join(row))
                #print(u'%s, %s' % (row[0], row[1]))
            except IndexError:
                if len(row) == 1:
                    print(row[0])
                else:
                    print("Blank")

#
# Edit Record
#

def editRecord(range = commmon.spreadSheetRange, values):

    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', common.SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    body = {
        'values': values
    }

    # Call the Sheets API
    result = service.spreadsheets().values().update(
        spreadsheetId=common.SPREADSHEET_ID,
        range=range,
        valueInputOption=common.value_input_option,
        body=body
        ).execute()


#
# Examples
#

def ex_Read_Print():

    # Define the range that you want to read
    range = 'Names!A2:B'

    # Function takes in the range and returns
    # a list with the values 
    # use printValues function if you want to display
    values = readSheet(range)


    printValues(values)


def ex_editRecord():

    # Range is where the data is placed
    # starting in the top left corner
    range = 'Names!A2:B'

    # This is meant to be an array for the row
    # EG "col A", "Col B", "Col C" etc...
    # Note the range must be big enough to include
    # the Values
    
    values = [[
        "Bob","123"
    ],]
    
    editRecord(range, values)
