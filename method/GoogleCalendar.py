# -*- coding: utf-8 -*-
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
from datetime import datetime, timedelta
from Info.Args import args


flags = args
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'method/client_secret.json'
APPLICATION_NAME = 'Google Calendar'


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
                                   'calendar-python-quickstart.json')
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run_flow(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def calendar_insert(schedule_table):
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    date_now = datetime.now()
    if 2 <= date_now.month <= 7:
        until = str(date_now.year) + "0701"
    else:
        if date_now.month <= 1:
            until = str(date_now.year) + "0201"
        else:
            until = str(date_now.year + 1) + "0201"

    weeks = {}
    for i in range(7):
        date_now = datetime.now() + timedelta(days=i)
        weeks[date_now.weekday()] = date_now.strftime('%Y-%m-%d')
    times = [['08:10:00', '09:00:00'], ['09:10:00', '10:00:00'], ['10:10:00', '11:00:00'], ['11:10:00', '12:00:00'],
             ['12:10:00', '13:00:00'], ['13:10:00', '14:00:00'], ['14:10:00', '15:00:00'], ['15:10:00', '16:00:00'],
             ['16:10:00', '17:00:00'], ['17:10:00', '18:00:00'], ['18:30:00', '19:20:00'], ['19:30:00', '20:20:00'],
             ['20:30:00', '21:20:00']]

    for y in range(1, 14):
        for x in range(1, 7):
            if schedule_table[y][x] != '':
                start_time = times[y-1][0]
                end_time = times[y-1][1]
                week = weeks[x-1]
                event = {
                    'summary': schedule_table[y][x].split('\n')[1],
                    'location': schedule_table[y][x].split('\n')[2],
                    'start': {
                        'dateTime': week + 'T' + start_time + '+08:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'end': {
                        'dateTime': week + 'T' + end_time + '+08:00',
                        'timeZone': 'America/Los_Angeles',
                    },
                    'recurrence': [
                        'RRULE:FREQ=WEEKLY;UNTIL=' + until
                    ],
                    'reminders': {
                        'useDefault': False,
                    },
                }
                service.events().insert(calendarId='primary', body=event).execute()
    print u"課表已匯入google行事曆"
