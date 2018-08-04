'''sheetsBackend'''
# dependant on main.py function
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
# remember to init from main otherwise values won't exist


#
# init
#


def init():
    '''To be run at startup'''

    global SCOPES, SPREADSHEET_ID, INPUT_OPTION, DEFAULT_RANGE, DATA_OPTION

    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = '12T7Ub21E-gAlwtJRZdsu3cww-wwIOvdjP_plhMxUn-0'

    INPUT_OPTION = 'USER_ENTERED'  # Leave this as is (it makes life easier)

    DEFAULT_RANGE = 'Names!A2:B'

    DATA_OPTION = 'INSERT_ROWS'

    # Auth with google
    global SERVICE

    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    SERVICE = build('sheets', 'v4', http=creds.authorize(Http()))


#
# Read
#

def readSheet(CellRange=''):
    ''' Reads the sheet'''

    if not CellRange:
        CellRange = DEFAULT_RANGE

    # Call the Sheets API
    result = SERVICE.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=CellRange).execute()
    return result.get('values', [])


#
# Print
#

def printValues(list='', header=["Names", "Number"]):
    '''Prints the sheet'''

    if not list:
        list = readSheet()

    print(", ".join(header), end=":\n")
    for row in list:
        try:
            print(", ".join(row))
            # print(u'%s, %s' % (row[0], row[1]))

        # should not be needed but just for incase
        except IndexError:
            if len(row) == 1:
                print(row[0])
            else:
                print("Blank")

#
# Edit table
#


def editTable(record, CellRange=''):
    '''Edits table at given range'''

    if not CellRange:
        CellRange = DEFAULT_RANGE

    table = {
        'values': record
    }

    # Call the Sheets API
    result = SERVICE.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID,
        range=CellRange,
        valueInputOption=INPUT_OPTION,
        body=table
    ).execute()

    return result

#
# append function
#


def append(record, CellRange='', insert=''):
    '''Add data to bottom of CellRange'''

    if not CellRange:
        CellRange = DEFAULT_RANGE
    if not insert:
        insert = DATA_OPTION

    table = {
        'values': record
    }

    # Call the Sheets API
    result = SERVICE.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=CellRange,
        valueInputOption=INPUT_OPTION,
        insertDataOption=insert,
        body=table
    ).execute()

    return result
