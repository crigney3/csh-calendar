import datetime
from flask import Flask, render_template
import random

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
application = Flask(__name__)

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

@application.route("/")
def hello():
    return render_template('home.html')

@application.route("/array")
def arrayTest():
    things = ["1","2","3","4","5","6","7"]
    placeHolder = random.randint(0,len(things)-1);
    return things[placeHolder]

@application.route("/google")
def calendar():
    #Authorize with credentials.json
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES);
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    #Call some API functions
    now = datetime.datetime.utcnow().isoformat() + 'Z';
    print("Fetching the upcoming ten events")
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('You have no upcoming events!')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

if __name__ == "__main__":
    application.run()
