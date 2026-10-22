import datetime
import json

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
        while True:
            eventFreq = input("How frequent? Daily (D), Weekly (W), Bi-Weekly (BW), Monthly (M)").strip().upper()

            if eventFreq in {"D","W","BW","M"}:
                break
            print('Please enter D,W,BW,M')
        if eventFreq == "D":
            for i in range(1,365):
                newEvent[eventNum] = {
                    'type':eventType,
                    'freq':eventFreq,
                    'date':startDate + datetime.timedelta(days = i),
                    'time':eventTime,
                    'mod':eventMod,
                    'desc':eventDesc
                }
                eventNum += 1
        elif eventFreq == "W":
            for i in range(7,365,7):
                newEvent[eventNum] = {
                    'type':eventType,
                    'freq':eventFreq,
                    'date':startDate + datetime.timedelta(days = i),
                    'time':eventTime,
                    'mod':eventMod,
                    'desc':eventDesc
                }
                eventNum += 1
        elif eventFreq == "BW":
            for i in range(14,365,14):
                newEvent[eventNum] = {
                    'type':eventType,
                    'freq':eventFreq,
                    'date':startDate + datetime.timedelta(days = i),
                    'time':eventTime,
                    'mod':eventMod,
                    'desc':eventDesc
                }
                eventNum += 1
        else:
            for i in range(30,365,30):
                newEvent[eventNum] = {
                    'type':eventType,
                    'freq':eventFreq,
                    'date':startDate + datetime.timedelta(days = i),
                    'time':eventTime,
                    'mod':eventMod,
                    'desc':eventDesc
                } 
                eventNum += 1

    else:
        eventFreq = None
    
    newEvent[eventNum] = {
        'type':eventType,
        'freq':eventFreq,
        'date':startDate,
        'time':eventTime,
        'mod':eventMod,
        'desc':eventDesc
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

    


def viewEvent(eventNum):
    print()
    print('Record',eventNum)
    print("Module: ",events[eventNum]['mod'])
    print("Date: ", events[eventNum]['date'].strftime("%d %B %Y"))  
    print("Description: ",events[eventNum]['desc'])
    print()

while True:
    event = int(input("What would you like to do? \n 1. View all events \n 2. Add a new event \n 3. View upcoming event \n 4. Delete an event \n Answer :"))
    if event == 1:
        viewAllEvents()
    elif event == 2:
        addEvent()
    elif event == 3:
        viewUpcomingEvent()
    elif event == 4:
        deleteEvent()