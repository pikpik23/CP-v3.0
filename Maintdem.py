from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1E8XFG8gVYvhUEtkMn6Sz6Erup0RQm2PKa2oIkjRrYto'
RANGE_NAME = 'MAINTDEM!A5:B'


def main():

    store = oauth_file.Storage('sheetsToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    else:
        print('Name, Score:')
        for row in values:
            try:
                print(u'%s, %s' % (row[0], row[1]))
            except IndexError:
                if len(row) == 1:
                    print(row[0])
                else:
                    print("Blank")


if __name__ == '__main__':
    main()