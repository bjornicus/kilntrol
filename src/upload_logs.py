""" start logging stuff to google sheets
"""
from __future__ import print_function
import os
import sys

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete your previously token.json
# see https://developers.google.com/sheets/api/quickstart/python
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'Kiln Troll'
SPREADSHEET_ID = '11HniCGaGZ8Hxs9w4wf1NqTmgrF_GLUpVq_j3qO5IJ2k'
LOGFILE = 'logs/temperature_summary.log'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """   
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_id.json', SCOPES)
            creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def get_service():
    """ Gets a the google sheets service
    Returns:
        The sheets service
    """
    credentials = get_credentials()
    service = build('sheets', 'v4', credentials=credentials)
    return service


def append_row(service, range_name, row):
    result = append_rows(service, range_name, [row])
    print('appended "' + str(row) + '" at ' +
          str(result['updates']['updatedRange']))
    return result


def append_rows(service, range_name, rows, insert_mode='OVERWRITE'):
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

def clear(service, range_name):
    return service.spreadsheets().values().clear(
        spreadsheetId=SPREADSHEET_ID,
        range=range_name,
        body={}).execute()


def upload_logfile(service, range_name, logfile=LOGFILE):
    """ Uploads the log file contents to the spreadsheet
    """
    rows = []
    with open(logfile, "r") as file:
        for l in file:
            rows.append(l.strip().split(','))
    append_rows(service, range_name, rows)


def tail_and_upload(service):
    """ Tails the temperature_log.csv and uploads entries to google sheets
    """
    range_name = 'Sheet1!A:C'
    print('clearing log')
    print(clear(service, range_name))
    print('uploading any existing logs')
    upload_logfile(service, range_name)

    print('tailing the log...')
    import subprocess
    f = subprocess.Popen(['tail', '-F', '-n', '0', LOGFILE],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        line = f.stdout.readline().decode()
        print('appending', line)
        try:
            append_row(service, range_name, line.split(','))
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            sys.stderr.writelines([
                'error appending entry: ' + str(sys.exc_info()[0]),
                line
            ])

def upload_target_profile(service):
    range_name = 'Sheet1!E:F'
    print('clearing target profile')
    print(clear(service, range_name))
    print('uploading target profile')
    upload_logfile(service, range_name, 'logs/target_profile.csv')

def test(service):
    """ Uploads a test entry to google sheets
    """
    range_name = 'Sheet1!A1'
    print('uploading...')
    append_row(service, range_name, "4:06 AM, 1234, 68".split(','))
    append_row(service, range_name, "4:07 AM, 5678, 68".split(','))


def main():
    service = get_service()
    upload_target_profile(service)
    tail_and_upload(service)
    # test(sevice)


if __name__ == '__main__':
    main()
