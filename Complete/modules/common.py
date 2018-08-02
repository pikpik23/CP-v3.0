# If modifying these scopes, delete the file token.json.

# remember to init from main otherwise values won't exist
def init():
	global SCOPES, SPREADSHEET_ID, value_input_option

	SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

	# The ID and range of a sample spreadsheet.
	SPREADSHEET_ID = '12T7Ub21E-gAlwtJRZdsu3cww-wwIOvdjP_plhMxUn-0' #My test sheet

	value_input_option = 'USER_ENTERED' #Leave this as is (it makes life easier)