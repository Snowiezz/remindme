events = {}
eventNum = 1

def viewEvents():
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

while True:
    event = int(input("What would you like to do? \n 1. View calendar \n 2. Add a new event \n"))
    if event == 1:
        viewEvents()
    elif event == 2:
        addEvent()
