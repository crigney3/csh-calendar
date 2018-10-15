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
    def __init__(self, titleE, wDay, dayM, sTime, monthId, descr=None):
        self.title = titleE
        self.day = wDay
        self.date = dayM
        self.sTime = sTime
        self.month = monthId
        self.desc = descr
class cshCalendar:
    def __init__(self, year, month):
        self.year = year
        self.month = month
    def getDays(self):
        return newCalendar.monthdays2calendar(self.year, self.month)
class driver:
    def setMonthArray():
        arrayBase = []
        days = 31
        i = 0
        month = int(datetime.datetime.today().month)
        year = int(datetime.datetime.today().year)
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            days = 31
        elif month == 2:
            days = 28
        elif month == 4 or month == 6 or month == 9 or month == 11:
            days = 30
        elif month == 2 and (year % 4) == 0:
            days = 29
        days+=1
        while(i < days):
            arrayBase.append([i])
            i+=1
        return arrayBase
    def setFirstOfMonth():
        month = str(datetime.datetime.today().month)
        year = str(datetime.datetime.today().year)
        day = 1
        firstOfMonth = year + "-" + month + "-" + str(day) + "T" + "00:00:00.000000Z"
        print(firstOfMonth)
        return firstOfMonth
    def setLastOfMonth():
        month = int(datetime.datetime.today().month) + 1
        year = int(datetime.datetime.today().year)
        if month is 13:
            month = 1
            year+=1
        day = 1
        lastOfMonth = str(year) + "-" + str(month) + "-" + str(day) + "T" + "00:00:00.000000Z"
        print(lastOfMonth)
        return lastOfMonth


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
    daysOfWeek = []
    allEvents = []
    sortedArray = driver.setMonthArray()
    firstOfMonth = driver.setFirstOfMonth()
    lastOfMonth = driver.setLastOfMonth()
    maxEvents = 50
    
    #Authorize with credentials.json
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES);
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    #Call some API functions
    now = datetime.datetime.utcnow().isoformat() + 'Z';
    print(now)
    print("Fetching the upcoming ten events")
    events_result = service.events().list(calendarId='primary', timeMin=firstOfMonth, timeMax=lastOfMonth,
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
        eventDayTemp = date.split('-')
        eventDay = int(eventDayTemp[2])
        eventMonth = int(eventDayTemp[1])
        time = splitter[1].split('-')

        #Get which week the event is in
        weekArrayInUse = 0;
        if(eventDay <= 7):
            weekArrayInUse = 0;
        elif(eventDay <= 14 and eventDay >= 8):
            weekArrayInUse = 1;
        elif(eventDay <= 21 and eventDay >= 15):
            weekArrayInUse = 2;
        elif(eventDay <= 28 and eventDay >= 22):
            weekArrayInUse = 3;
        else:
            weekArrayInUse = 4;
        #Get what day the event is
        dow = eventDay % 7;
        dayOfWeek = calendarStruct[weekArrayInUse][dow][1]

        numberOfWeeks = len(calendarStruct)
        startTime = time[0]
        endTime = time[1]
        
        dates.append(date)
        daysOfWeek.append(dayOfWeek)
        startTimes.append(startTime)
        endTimes.append(endTime)
        events1.append(event['summary'])

        newEvent = cshEvent(event['summary'], dayOfWeek, eventDay, startTime, eventMonth)
        allEvents.append(newEvent)
    for event in allEvents:
        if event.month == int(datetime.datetime.today().month):
            sortedArray[event.date].append(event)
    print(sortedArray)
    def sortEvents():
        for event in allEvents:
            iter = 0
            for event in allEvents:
                iter = iter + 1
                tempEvents = []
                if event.date < allEvents[iter]:
                    tempEvents[0] = event
                    event = allEvents[iter]
                    allEvents[iter] = tempEvents[0]

    print(allEvents)
    return render_template('calendar.html', events=events1, dayOfWeek=daysOfWeek, startTimes=startTimes, endTimes=endTimes, dates=dates, allEvents=sortedArray, struct=calendarStruct, weeks=numberOfWeeks)

if __name__ == "__main__":
    application.run()
