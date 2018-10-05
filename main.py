import datetime
from flask import Flask, render_template
import random
import re
import calendar

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
application = Flask(__name__)

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
newCalendar = calendar.Calendar()

#Define the Event class that will be passed into the html file for sorting
class cshEvent:
    def __init__(self, titleE, wDay, dayM, sTime, eTime, descr=None):
        self.title = titleE
        self.day = wDay
        self.date = dayM
        self.sTime = sTime
        self.eTime = eTime
        self.desc = descr
class cshCalendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month
    def getDays(self):
        return newCalendar.monthdays2calendar(self.year, self.month)



cshCalendarDates = cshCalendar(int(datetime.datetime.today().year), int(datetime.datetime.today().month))
calendarStruct = cshCalendarDates.getDays()
print(calendarStruct)

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
    #Initialize storage arrays for sorting/searching
    dates = []
    startTimes = []
    endTimes = []
    events1 = []
    allEvents = []
    maxEvents = 10
    
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
                                          maxResults=maxEvents, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    output = 'Events coming up: ';

    #Output
    if not events:
        print('You have no upcoming events!')
        output = output + 'No events!'
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        
        print(start, event['summary'])
        splitter = str(event['start'].get('dateTime')).split('T')
        date = splitter[0]
        time = splitter[1].split('-')
        
        startTime = time[0]
        endTime = time[1]
        
        dates.append(date)
        startTimes.append(startTime)
        endTimes.append(endTime)
        events1.append(event['summary'])

        newEvent = cshEvent(event['summary'], 1, date, startTime, endTime)
        allEvents.append(newEvent)
    print(allEvents[5].date)
    return render_template('calendar.html', events=events1, startTimes=startTimes, endTimes=endTimes, dates=dates, allEvents=allEvents, struct=calendarStruct)

if __name__ == "__main__":
    application.run()
