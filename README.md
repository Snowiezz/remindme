This is a command-line calendar manager written in python that stores events locally and syncs them to iCloud calendar using CalDAV.

I built this to keep track of university deadlines, lectures and work shifts, with everything showing up on my calendar via iCloud.

## Features

- Add, edit, view and delete events from a terminal menu
- Allows both one-off and recurring events (Daily,weekly,monthly)
- Upcoming view which shows all events in the next 7,30,365 days
- Icloud sync over CalDAV
 - New events uploaded
 - Edited events are updated, matched by their UID
 - Deleted events are queued locally and removed on iCloud on the next sync
 - Input validation for dates and times
 - Local JSON storage


## Project Structure

main.py             # the whole app: menu, event handling etc
events.json         # saved events
deleted_events.json # UID's waiting to be deleted from iCloud
