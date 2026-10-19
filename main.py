events = {}
eventNum = 1

def viewCalendar():
    for event in events:
        print(events[event])

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

while True:
    event = int(input("What would you like to do? \n 1. View calendar \n 2. Add a new event \n"))
    if event == 1:
        viewCalendar()
    elif event == 2:
        addEvent()
