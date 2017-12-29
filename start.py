""" start logging stuff to google sheets
"""
from __future__ import print_function
import os
import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Kiln Troll'
SPREADSHEET_ID = '11HniCGaGZ8Hxs9w4wf1NqTmgrF_GLUpVq_j3qO5IJ2k'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-kiln-troll.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_service():
    """ Gets a the google sheets service
    Returns:
        The sheets service
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discovery_url = ('https://sheets.googleapis.com/$discovery/rest?'
                     'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discovery_url)
    return service

def append_row(service, range_name, row):
    value_input_option = 'USER_ENTERED'

    # How the input data should be inserted.
    # insert_data_option = ''  # OVERWRITE | INSERT_ROWS

    value_range_body = {
        "values": [
            row
        ]
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption=value_input_option,
        body=value_range_body).execute()

def main():
    """ Main :)
    """
    service = get_service()

    range_name = 'Sheet1'
    # How the input data should be interpreted.
    append_row(service, range_name, ["the time", 1234])




if __name__ == '__main__':
    main()
