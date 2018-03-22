""" start logging stuff to google sheets
"""
from __future__ import print_function
import os
import sys
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
# at ~/.credentials/sheets.googleapis.com-kiln-troll.json
# see https://developers.google.com/sheets/api/quickstart/python
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = '../client_id.json'
APPLICATION_NAME = 'Kiln Troll'
SPREADSHEET_ID = '11HniCGaGZ8Hxs9w4wf1NqTmgrF_GLUpVq_j3qO5IJ2k'
LOGFILE = '../logs/temperature.log'


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
        else:  # Needed only for compatibility with Python 2.6
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
    result = append_rows(service, range_name, [row])
    print('appended "' + str(row) + '" at ' +
          str(result['updates']['updatedRange']))
    return result


def append_rows(service, range_name, rows, insert_mode='INSERT_ROWS'):
    value_input_option = 'USER_ENTERED'

    value_range_body = {
        "values": rows
    }

    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        valueInputOption=value_input_option,
        insertDataOption=insert_mode,
        body=value_range_body).execute()
    return result


def upload_logfile(service, range_name):
    """ Uploads the log file contents to the spreadsheet
    """
    rows = []
    with open(LOGFILE, "r") as file:
        for l in file:
            rows.append(l.strip().split(','))
    append_rows(service, range_name, rows, 'OVERWRITE')


def tail_and_upload(service):
    """ Tails the temperature_log.csv and uploads entries to google sheets
    """
    range_name = 'Sheet1!A1'

    upload_logfile(service, range_name)

    import subprocess
    f = subprocess.Popen(['tail', '-F', '-n', '0', LOGFILE],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = f.stdout.readline()
        try:
            append_row(service, range_name, line.split(','))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.stderr.writelines([
                'error appending entry: ' + str(sys.exc_info()[0]),
                line
            ])


def test(service):
    """ Uploads a test entry to google sheets
    """
    range_name = 'Sheet1!A1'
    print('uploading...')
    append_row(service, range_name, "4:06 AM, 1234, 68".split(','))
    append_row(service, range_name, "4:07 AM, 5678, 68".split(','))


def main():
    service = get_service()
    tail_and_upload(service)
    # test(sevice)


if __name__ == '__main__':
    main()
