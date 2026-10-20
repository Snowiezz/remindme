import datetime

events = {
    1: {
        'type': 'O',
        'freq': None,
        'date': '191026',
        'time': '14:00',
        'mod': 'CS101',
        'desc': 'Programming worksheet due today'
    },
    2: {
        'type': 'O',
        'freq': None,
        'date': '221026',
        'time': '17:00',
        'mod': 'CS102',
        'desc': 'Submit maths problem sheet'
    },
    3: {
        'type': 'R',
        'freq': 'W',
        'date': '241026',
        'time': '09:00',
        'mod': '',
        'desc': 'Work shift'
    },
    4: {
        'type': 'O',
        'freq': None,
        'date': '261026',
        'time': '12:00',
        'mod': 'CS103',
        'desc': 'Deadline exactly seven days away'
    },
    5: {
        'type': 'R',
        'freq': 'BW',
        'date': '021126',
        'time': '11:00',
        'mod': 'CS101',
        'desc': 'Fortnightly programming tutorial'
    },
    6: {
        'type': 'O',
        'freq': None,
        'date': '181126',
        'time': '15:00',
        'mod': 'CS102',
        'desc': 'Deadline exactly thirty days away'
    },
    7: {
        'type': 'O',
        'freq': None,
        'date': '011226',
        'time': '10:00',
        'mod': 'CS103',
        'desc': 'Project presentation beyond thirty days'
    },
    8: {
        'type': 'O',
        'freq': None,
        'date': '181026',
        'time': '16:00',
        'mod': 'CS101',
        'desc': 'Past deadline'
    }
}

eventNum = max(events, default=0) + 1



def viewAllEvents():
    print("--------")
    for eventNum, details in events.items():
        print('Record',eventNum)
        for record,value in details.items():
            print(record,value)
        print("\n")
    print("--------")




    

def addEvent():
    global eventNum
    eventType = input("Is the event recurring (R) or one-time (O)?")
    if eventType == 'R':
        while True:
            eventFreq = input("How frequent? Daily (D), Weekly (W), Bi-Weekly (BW), Monthly (M)").strip().upper()

            if eventFreq in {"D","W","BW","M"}:
                break
            print('Please enter D,W,BW,M')
    else:
        eventFreq = None

    eventDate = input("When is the date? (DDMMYY)")
    eventTime = input("When is the time? (24hrs)")
    eventMod = input("Module code?")
    eventDesc = input("What is the description?")
    events[eventNum] = {
        'type':eventType,
        'freq':eventFreq,
        'date':eventDate,
        'time':eventTime,
        'mod':eventMod,
        'desc':eventDesc
    }
    eventNum += 1
    print("Event added.")
def viewUpcomingEvent():
    currentDate = datetime.date.today()
    week = []
    month = []
    year = []
    for eventNum, details in events.items():
        eventDate = datetime.datetime.strptime(details['date'], "%d%m%y").date()
        diff = (eventDate - currentDate).days
        if diff < 7:
            week.append(eventNum)
        elif 7 < diff < 30:
            month.append(eventNum)  
        else:
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
    


def viewEvent(eventNum):
    print()
    print('Record',eventNum)
    print("Module: ",events[eventNum]['mod'])
    eventDate = datetime.datetime.strptime(events[eventNum]['date'], "%d%m%y")
    print("Date: ",eventDate.strftime("%d %B %Y"))
    print("Description: ",events[eventNum]['desc'])
    print()

while True:
    event = int(input("What would you like to do? \n 1. View all events \n 2. Add a new event \n 3. View upcoming event"))
    if event == 1:
        viewAllEvents()
    elif event == 2:
        addEvent()
    elif event == 3:
        viewUpcomingEvent()