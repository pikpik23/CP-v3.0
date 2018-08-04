from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauth_file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    store = oauth_file.Storage('mailToken.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))

    # Call the Gmail API
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        index = 1
        for label in labels:
        	if index == 20:
        		break
        	else:
        		index += 1

        	print(label)
        	#print(str(index)+". "+label['name'])


if __name__ == '__main__':
    main()