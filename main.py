import datetime
import json
import caldav
from getpass import getpass
from zoneinfo import ZoneInfo
import uuid
from icalendar import Alarm
import argparse
import sys
from caldav.lib.error import AuthorizationError
from pathlib import Path



DATA_DIR = Path(__file__).parent
EVENTS_FILE = DATA_DIR / 'events.json'
DELETED_FILE = DATA_DIR / 'deleted_events.json'



def loadJson(path,default):
    try:
        with open(path,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default
rawevents = loadJson(EVENTS_FILE,{})
pendingDeletes = loadJson(DELETED_FILE,[])
events = {}

for eventId, details in rawevents.items():
    details['date'] = datetime.date.fromisoformat(details['date'])
    events[int(eventId)] = details
eventNum = max(events, default=0) + 1



#parse
def parseDate(text):
    return datetime.datetime.strptime(text,'%d%m%y').date()
def parseTime(text):
    return datetime.datetime.strptime(text,'%H%M').strftime('%H%M')


def makeAlarm(title,minutesBefore=60):
    alarm = Alarm()
    alarm.add('action','DISPLAY')
    alarm.add('description',title)
    alarm.add('trigger', datetime.timedelta(minutes=-minutesBefore))
    return alarm




def saveEvents():
    eventsToSave = {}
    for eventId, details in events.items():
        savedDetails = details.copy()
        savedDetails['date'] = details['date'].isoformat()
        eventsToSave[eventId] = savedDetails

    with open(EVENTS_FILE, 'w') as f:
        json.dump(eventsToSave, f, indent=4)
    with open(DELETED_FILE,'w') as f:
        json.dump(pendingDeletes,f,indent=4)

    

def addEvent(desc,date,time,mod,freq):
    global eventNum

    
    events[eventNum] = {
        'type':'R' if freq else 'O',
        'freq':freq,
        'date':date,
        'time':time,
        'mod':mod,
        'desc':desc,
        'uid': str(uuid.uuid4()),
        'needsUpdating' : False
    }
    eventNum += 1

    saveEvents()
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




def deleteEvent(id):
    removedEvent = events.pop(id,None)
    if removedEvent is None:
        print('Event not found')
        return
    if removedEvent.get('uid'):
        pendingDeletes.append(removedEvent['uid'])
    print(f'Record {id} has been deleted.')
    saveEvents()
    

def editEvent(id,field,value):
    if id not in events:
        sys.exit('Invalid record number')
    if field == 'date':
        try:
            value = parseDate(value)
        except ValueError:
            sys.exit(f'{value} is an invalid date')
    elif field == 'time':
        try:
            value = parseTime(value)
        except ValueError:
            sys.exit(f'{value} is an invalid time')
    events[id][field] = value
    events[id]['needsUpdating'] = True
    saveEvents()
    print("Event edited.")


def syncEvents():
    email = input("Email: ")
    password = getpass("Password: ")
    try:
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
                sys.exit('No calendar found, check README to create a calendar.')
            
            calendar = matches[0]

            currentEvents = calendar.get_events()


    




            existing = {}
            for event in currentEvents:
                existing[str(event.get_icalendar_component()['UID'])] = event

            # deleted events

            for uid in pendingDeletes:
                if uid in existing:
                    existing[uid].delete()
                    del existing[uid]
                    print('Event deleted')
            pendingDeletes.clear()

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
                    remoteEvent = existing[eventUID]
                    comp = remoteEvent.icalendar_component

                    for field in ('summary','dtstart','dtend'):
                        comp.pop(field,None)
                    comp.add('summary', title)
                    comp.add('dtstart',start)
                    comp.add('dtend',start + datetime.timedelta(minutes=30))
                    comp.subcomponents = [c for c in comp.subcomponents if c.name != 'VALARM']
                    comp.add_component(makeAlarm(title))
                    remoteEvent.save()
                    detail['needsUpdating'] = False
                    print('Event updated')
                else:
                    if detail['freq'] is None:
                        calendar.add_event(
                            dtstart=start,
                            dtend=start + datetime.timedelta(minutes=30),
                            summary=title,
                            uid=eventUID,
                            alarm_trigger=datetime.timedelta(minutes=-60),
                            alarm_action='DISPLAY',
                            alarm_description=title
                        )
                    else:
                        calendar.add_event(
                            dtstart=start,
                            dtend=start + datetime.timedelta(minutes=30),
                            summary=title,
                            uid=eventUID,
                            rrule={'FREQ': detail['freq']},
                            alarm_trigger=datetime.timedelta(minutes=-60),
                            alarm_action='DISPLAY',
                            alarm_description=title
                        )
                    print("event added")
            saveEvents()
    except AuthorizationError:
        sys.exit('Login failed, check your email and app-specific password')

def dateArg(text):
    try:
        return parseDate(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f'{text} is not a valid date, use DDMMYY')
def timeArg(text):
    try:
        return parseTime(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f'{text} is not a valid time, use HHMM 24 Hours')
def viewEvent(eventNum):
    print('Record',eventNum)
    if events[eventNum]['mod']:
        print("Module: ",events[eventNum]['mod'])
    print("Date: ", events[eventNum]['date'].strftime("%d %B %Y"))
    print('Time: ',datetime.datetime.strptime(events[eventNum]['time'],'%H%M').strftime('%H:%M'))  
    print("Description: ",events[eventNum]['desc'])

    print()

def viewAllEvents():
    if not events:
        print('No events created')
        return
    print("--------")
    for eventNum, _ in sorted(events.items(), key=lambda item: item[1]['date']):
        viewEvent(eventNum)
    print("--------")



def buildParser():
    parser = argparse.ArgumentParser(description = 'Manage events and sync then to iCloud calendar. --help for help')
    commands = parser.add_subparsers(dest='command')

    add = commands.add_parser('add', help='Add a new event')
    add.add_argument('desc',help='What the event is')
    add.add_argument('date',type=dateArg,help='Date of event as DDMMYY')
    add.add_argument('time',type=timeArg,help='Time of event as HHMM 24hours')
    add.add_argument('--mod',help='Module (if applicable)',default='')
    add.add_argument('--repeat',help='How often?',choices=['daily','weekly','monthly'])

    commands.add_parser('list', help='Show all events')
    commands.add_parser('upcoming',help='View upcoming events')

    delete = commands.add_parser('delete',help='Delete an event')
    delete.add_argument('id',type=int,help='record number')

    edit = commands.add_parser('edit',help='Edit an event')
    edit.add_argument('id',type=int,help='Record number')
    edit.add_argument('field',choices=['date','time','mod','desc'])
    edit.add_argument('value',help='New value')

    commands.add_parser('sync', help='sync events to iCloud')
    return parser

def runCommand(args):
    if args.command == 'add':
        if args.repeat:
            eventFreq = args.repeat.upper()
        else:
            eventFreq = None
        addEvent(args.desc,args.date,args.time,args.mod,eventFreq)
        print('Event added successfully')
    elif args.command == 'edit':
        editEvent(args.id,args.field,args.value)
    elif args.command == 'delete':
        deleteEvent(args.id)
    elif args.command == 'upcoming':
        viewUpcomingEvent()
    elif args.command == 'list':
        viewAllEvents()
    elif args.command == 'sync':
        syncEvents()
    else:
        parser.
    
if __name__ == '__main__':
    parser = buildParser()
    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
    else:
        runCommand(args)