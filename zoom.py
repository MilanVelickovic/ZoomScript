import json
import webbrowser as web
from datetime import datetime
from time import sleep

print("Program running...")

todays_classes = []
date = datetime.now()
day = date.strftime("%A")

with open("./classes.json", 'r', encoding="UTF-8") as file:
    classes = json.load(file)
    for _class in classes:
        if _class["appointment"]["day"] == day:
            todays_classes.append(_class)

def changeTime(current_time, addMinutes):
    minutes = int(current_time[3:]) + addMinutes
    if minutes >= 60:
        new_hours = int(current_time[0:2]) + 1
        new_minutes = minutes - 60
        return f"{str(new_hours)}:{new_minutes}"
    else:
        new_minutes = int(current_time[3:]) + minutes
        return f"{current_time[0:2]}:{str(new_minutes)}"

def getDifference(current_time, start_time):
    if current_time[0:2] == start_time[0:2]:
        return int(current_time[3:]) - int(start_time[3:])
    else:
        return (60 - int(start_time[3:])) + int(current_time[3:])

def classInProgress(day, time):
    for _class in todays_classes:
        if _class["appointment"]["day"] == day:
            for i in _class['appointment']['time']:
                if time > i and time < changeTime(i, 40):
                    showAndRun(day, time, _class, True, i)
                        
def showAndRun(day, time, _class, inProgress, start_time):
    params = ["mark", "host", "link"]
    if day == "Thursday" and _class["code"] == "IT335" and (int(date.strftime("%V")) % 2 != 0):
        params = ["mark1", "host1", "link1"]
            
    if inProgress:
        print(f"[INFO]  {_class['code']} {_class[params[0]]} in progress..\n\tHost: {_class[params[1]]}\n\tDo you want to join? [y/n]")
        ans = input()
        if ans.lower() == 'y':
            web.open(_class[params[2]])
            sleep(60 * 40)
        else:
            sleep(60 * (40 - getDifference(time, start_time)))

    else: 
        print(f"[{time}]: {_class['code']} {_class[params[0]]} meeting started!\n\t Host: {_class[params[1]]}")
        web.open(_class[params[2]])
        sleep(60 * 40) 

def main():
    while True:
        wait_time = 60
        date = datetime.now()
        time = f"{date.strftime('%H')}:{date.minute}"

        classInProgress(day, time)
        
        for _class in todays_classes:
            if time in _class["appointment"]["time"]:
                showAndRun(day, time, _class, False, time)

        if time == "19:05":
            break
        else:
            sleep(wait_time)

main()
