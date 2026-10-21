import datetime

events = {
    1: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 10, 23),
        'time': '14:00',
        'mod': 'CS101',
        'desc': 'Programming worksheet due today'
    },
    2: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 10, 22),
        'time': '17:00',
        'mod': 'CS102',
        'desc': 'Submit maths problem sheet'
    },
    3: {
        'type': 'R',
        'freq': 'W',
        'date': datetime.date(2026, 10, 24),
        'time': '09:00',
        'mod': '',
        'desc': 'Work shift'
    },
    4: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 10, 26),
        'time': '12:00',
        'mod': 'CS103',
        'desc': 'Deadline exactly seven days away'
    },
    5: {
        'type': 'R',
        'freq': 'BW',
        'date': datetime.date(2026, 11, 2),
        'time': '11:00',
        'mod': 'CS101',
        'desc': 'Fortnightly programming tutorial'
    },
    6: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 11, 18),
        'time': '15:00',
        'mod': 'CS102',
        'desc': 'Deadline exactly thirty days away'
    },
    7: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 12, 1),
        'time': '10:00',
        'mod': 'CS103',
        'desc': 'Project presentation beyond thirty days'
    },
    8: {
        'type': 'O',
        'freq': None,
        'date': datetime.date(2026, 10, 18),
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
    while True:
        try:
            eventDate = input("When is the date? (DDMMYY)")
            startDate = datetime.datetime.strptime(eventDate, "%d%m%y").date()
            break
        except ValueError:
            print("Please enter a valid date in DDMMYY format.")
    while True:
        eventTime = input("When is the time? (24hrs)")
        if 0 <= eventTime < 2400:
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
                events[eventNum] = {
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
                events[eventNum] = {
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
                events[eventNum] = {
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
                events[eventNum] = {
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
    
    events[eventNum] = {
        'type':eventType,
        'freq':eventFreq,
        'date':startDate,
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
    


def viewEvent(eventNum):
    print()
    print('Record',eventNum)
    print("Module: ",events[eventNum]['mod'])
    print("Date: ", events[eventNum]['date'].strftime("%d %B %Y"))  
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