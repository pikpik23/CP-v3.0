'''sheets_Backend'''
# dependant on main.py function
from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

###########################################################
#
# sheetsBackend.py
#
# The script used to automate RO Creation
#
# AUTHOR: LAMINGTON (ADMINO 2019)
# Renier Lambinon 
#
###########################################################



# If modifying these scopes, delete the file token.json.
# remember to init from main otherwise values won't exist



class Sheet:

    oauth = 'sheetsToken.json'
    client_secret = 'credentials.json'
    data_option = 'INSERT_ROWS'
    scopes = 'https://www.googleapis.com/auth/spreadsheets'
    input_option = 'USER_ENTERED'

    #
    # init
    #

    def __init__(self, spread_sheet_id, default_range):
        '''To be run at startup'''

        # The ID and range of a sample spreadsheet.
        self.spreadsheet_id = spread_sheet_id

        self.default_range = default_range

        # Auth with google

        store = oauth_file.Storage(self.oauth)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                self.client_secret, self.scopes)
            creds = tools.run_flow(flow, store)
        self.service = build('sheets', 'v4', http=creds.authorize(Http()))

    #
    # Read
    #

    def readSheet(self, CellRange=''):
        ''' Reads the sheet'''

        if not CellRange:
            CellRange = self.default_range

        # Call the Sheets API
        result = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=CellRange).execute()
        return result.get('values', [])

    #
    # Print
    #

    def printValues(self, data='', header=["Time", "Type", "Message"]):
        '''Prints the sheet'''

        if not data:
            data = self.readSheet()

        print(", ".join(header), end=":\n")
        for row in data:
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

    def editTable(self, record, CellRange=''):
        '''Edits table at given range'''

        if not CellRange:
            CellRange = self.default_range

        table = {
            'values': record
        }

        # Call the Sheets API
        result = self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=CellRange,
            valueInputOption=self.input_option,
            body=table
        ).execute()

        return result

    #
    # append function
    #

    def append(self, record, CellRange='', insert=''):
        '''Add data to bottom of CellRange'''

        if not CellRange:
            CellRange = self.default_range
        if not insert:
            insert = self.data_option

        table = {
            'values': record
        }

        # Call the Sheets API
        result = self.service.spreadsheets().values().append(
            spreadsheetId=self.spreadsheet_id,
            range=CellRange,
            valueInputOption=self.input_option,
            insertDataOption=insert,
            body=table
        ).execute()

        return result
