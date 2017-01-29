import datetime, requests, time

API = "3a4b7ae58164f10427e30818404d25"
words = ["swift", "node", "dart", "java"]
country = "us"
state = "ca"
city = "Boston"
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def loadEvents():
    result = requests.get("https://api.meetup.com/2/open_events",
                    { "time": nextWeek(),
                      "limited_events": "false",
                      "key": API,
                      "country": country,
                      "text": ', '.join(map(str, words)),
                      "state": state,
                      "city": city, }).json()
    return result["results"]

def createHTMLDocumentForEvents(events):
    with open("index.html", "w") as file:
        for i in range(7):
            eventsOfDay = filterEventsByDay(i, events)
            day = days[i]
            file.write("<h2>" + day +  "(" + str(len(eventsOfDay)) + " events)" +"</h2>")

            if len(eventsOfDay) > 0:
                file.write("<ul>")
            else:
                continue

            currentEvent = 0
            for event in eventsOfDay:
                currentEvent = currentEvent + 1
                file.write("<li>")
                file.write("<h3>" + str(currentEvent) + ") " + event["name"] + "</h3>")
                file.write("<h4>" + "Address: "  + createAddressForEvent(event) + "</h4>")
                file.write("<h4>" + "Date: " + createDateFromEvent(event).strftime("%Y-%m-%d %H:%M:%S") + "</h4>")
                file.write("<h4>Description:</h4>")
                file.write("<div>")
                if 'description' in event.keys():
                    file.write(event["description"])
                file.write("</div>")
                file.write("</li>")
            file.write("</ul>")

def createAddressForEvent(event):
    if ("venue" in event.keys()):
        address = event["venue"]
        return address["name"] + " (" + address["address_1"] + ", " + address["city"] + ")"
    else:
        return "Disable address"

def createDateFromEvent(event):
    event_time = int(event["time"])
    timezone_offset = int(event["utc_offset"])
    day = datetime.datetime.fromtimestamp(event_time / 1e3)
    time = event_time + localTime() * 60000
    return datetime.datetime.fromtimestamp((event_time + timezone_offset) / 1e3)

def filterEventsByDay(day, events):
    filter = []
    for event in events:
        eventDay = createDateFromEvent(event).weekday()
        if eventDay == day :
            filter.append(event)
    return filter

def nextWeek():
    now = datetime.datetime.today().weekday()
    nextMonday = 0
    if (now == 0):
        nextMonday = 1
    else:
        nextMonday = 7 - now
    nextSunday = nextMonday +7
    return str(nextMonday) + "d," + str(nextSunday) + "d"

def localTime():
    is_dst = time.daylight and time.localtime().tm_isdst > 0
    utc_offset = - (time.altzone if is_dst else time.timezone)
    return utc_offset

if __name__ == '__main__':
    events = loadEvents()
    createHTMLDocumentForEvents(events)

