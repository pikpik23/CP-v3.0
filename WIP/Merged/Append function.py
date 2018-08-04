#
# append function
#
def append(record, range = '', insert=''):
    if not range:
        range = common.totalRange
    if not insert:
        insert = common

    table = {
        'values': record
    }

    # Call the Sheets API
    result = common.service.spreadsheets().values().append(
        spreadsheetId=common.SPREADSHEET_ID,
        range=range,
        valueInputOption=common.value_input_option,
        insertDataOption= common.DataOption,
        body=table
        ).execute()
