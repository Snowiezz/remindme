import datetime
import json
import caldav
from getpass import getpass
from zoneinfo import ZoneInfo
import uuid

with open('events.json','r') as f:
    rawevents = json.load(f)

events = {}

for eventId, details in rawevents.items():
    details['date'] = datetime.date.fromisoformat(details['date'])
    events[int(eventId)] = details
eventNum = max(events, default=0) + 1



def viewAllEvents():
    print("--------")
    for eventNum, details in events.items():
        print('Record',eventNum)
        for record,value in details.items():
            print(record,value)
        print("\n")
    print("--------")


def saveEvents():
    eventsToSave = {}
    for eventId, details in events.items():
        savedDetails = details.copy()
        savedDetails['date'] = details['date'].isoformat()
        eventsToSave[eventId] = savedDetails

    with open('events.json', 'w') as f:
        json.dump(eventsToSave, f, indent=4)

    

def addEvent():
    global eventNum
    newEvent = {}
    while True:
        try:
            eventDate = input("When is the date? (DDMMYY)")
            startDate = datetime.datetime.strptime(eventDate, "%d%m%y").date()
            break
        except ValueError:
            print("Please enter a valid date in DDMMYY format.")
    while True:
        eventTime = input("When is the time? (24hrs)")
        if 0 <= int(eventTime) < 2400:
            break
        print("Enter 0000-2400")
    eventMod = input("Module code?")
    eventDesc = input("What is the description?")
    while True:
        eventType = input("Is the event recurring (R) or one-time (O)?").strip().upper()
        if eventType in {'R','O'}:
            break
    if eventType == 'R':
        eventTypes = {
            'D':'DAILY',
            'W':'WEEKLY',
            'M':'MONTHLY'
        }
        while True:
            eventFreq = input("How frequent? Daily (D), Weekly (W), Monthly (M)").strip().upper()

            if eventFreq in {"D","W","M"}:
                break
            print('Please enter D,W,M')
        eventFreq = eventTypes[eventFreq]

    else:
        eventFreq = None
    
    newEvent[eventNum] = {
        'type':eventType,
        'freq':eventFreq,
        'date':startDate,
        'time':eventTime,
        'mod':eventMod,
        'desc':eventDesc,
        'uid': str(uuid.uuid4()),
        'needsUpdating' : False
    }
    eventNum += 1
    events.update(newEvent)

    saveEvents()
    print("Event added.")
def viewUpcomingEvent():
    currentDate = datetime.date.today()
    week = []
    month = []
    year = []
    for eventNum, details in sorted(events.items(), key=lambda item: item[1]['date']):
        eventDate = details['date']
        diff = (eventDate - currentDate).days
        if 0 <= diff <= 7:
            week.append(eventNum)
        elif 7 < diff <= 30:
            month.append(eventNum)  
        elif 30 < diff <= 365:
            year.append(eventNum)
    if week:
        print('-----')
        print('Next 7 days')
        for event in week:
            viewEvent(event)
    if month:
        print('-----')
        print('Next 30 days')
        for event in month:
            viewEvent(event)
    if year:
        print('-----')
        print("Next 365 days")
        for event in year:
            viewEvent(event)

def deleteEvent():
    id = int(input("What is the record number?: "))
    removedEvent = events.pop(id,None)
    if removedEvent is None:
        print('Event not found')
    else:
        print(f'Record {id} has been deleted.')
        saveEvents()

def editEvent():
    id = int(input("What is the record number?: "))
    if id not in events:
        print("Invalid record number")
        return
    edit = input("What do you want to edit?: (date,time,mod,desc)").strip().lower()
    newentry = input("What do you want to change the field to?")
    if edit in {'date','time','mod','desc'}:
        if edit == 'time':
            try:
                newentry = datetime.datetime.strptime(newentry,'%H%M').strftime('%H%M')
            except ValueError:
                print("Not a valid time! 0000-2359")
                return
        if edit == 'date':
            newentry = datetime.datetime.strptime(newentry,'%d%m%y').date()
        events[id][edit] = newentry
    else:
        print("Error, record not found")
    events[id]['needsUpdating'] = True
    saveEvents()
    print("Event edited.")


def syncEvents():
    email = input("Email: ")
    password = getpass("Password: ")
    with caldav.DAVClient(
        url="https://caldav.icloud.com/",
        username=email,
        password=password
    ) as client:
        calendars = client.get_calendars()
        calendarName = 'RemindMeNEW'

        matches = [
            calendar for calendar in calendars
            if calendar.get_display_name() == calendarName
        ]

        if not matches:
            print('Error, no calendar found')
            return
        
        calendar = matches[0]

        currentEvents = calendar.get_events()



        existing = []
        for event in currentEvents:
            existing.append(str(event.get_icalendar_component()['UID']))

        for id,detail in events.items():
            title = detail['desc']
            startTime = datetime.datetime.strptime(detail['time'], "%H%M").time()

            start = datetime.datetime.combine(detail['date'],startTime,tzinfo=ZoneInfo("Europe/London"))



            eventUID = detail.get('uid')

            needsUpdating = detail.get('needsUpdating',False)

            if eventUID is None:
                detail['uid'] = str(uuid.uuid4())
                eventUID = detail.get('uid')
                saveEvents()
            if eventUID in existing and needsUpdating == False:
                print('event already in')
            elif eventUID in existing and needsUpdating:
                remoteEvent = calendar.event_by_uid(eventUID)
                comp = remoteEvent.icalendar_component

                for field in ('summary','dtstart','dtend'):
                    comp.pop(field,None)
                comp.add('summary', title)
                comp.add('dtstart',start)
                comp.add('dtend',start + datetime.timedelta(minutes=30))
                remoteEvent.save()
                detail['needsUpdating'] = False
                print('Event updated')
            else:
                calendar.add_event(
                    dtstart=start,
                    dtend=start + datetime.timedelta(minutes=30),
                    summary=title,
                    uid=eventUID
                )
                existing.append(eventUID)
                print("event added")




    


def viewEvent(eventNum):
    print()
    print('Record',eventNum)
    print("Module: ",events[eventNum]['mod'])
    print("Date: ", events[eventNum]['date'].strftime("%d %B %Y"))  
    print("Description: ",events[eventNum]['desc'])
    print()

while True:
    event = int(input("What would you like to do? \n 1. View all events \n 2. Add a new event \n 3. View upcoming event \n 4. Delete an event \n 5. Edit an event \n 6. Sync events \n Answer :"))
    if event == 1:
        viewAllEvents()
    elif event == 2:
        addEvent()
    elif event == 3:
        viewUpcomingEvent()
    elif event == 4:
        deleteEvent()
    elif event == 5:
        editEvent()
    elif event == 6:
        syncEvents()