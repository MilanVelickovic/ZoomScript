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

def classInProgress(day, date):
    for _class in todays_classes:
        if _class["appointment"]["day"] == day:
            for i in _class['appointment']['time']:
                if date.hour == int(i[0:2]) and date.minute > int(i[3:]):
                    print(f"[INFO]  {_class['code']} {_class['mark']} in progress..\n\tHost: {_class['host']}\n\tDo you want to join? [y/n]")
                    ans = input()
                    if ans.lower() == 'y':
                        web.open(_class["link"])
                    
while True:
    wait_time = 60
    date = datetime.now()
    time = f"{date.hour}:{date.minute}"

    classInProgress(day, date)
    
    for _class in todays_classes:
        if time in _class["appointment"]["time"]:
            if day == "Thursday" and _class["code"] == "IT335" and (int(date.strftime("%V")) % 2 != 0):
                print(f"[{time}]: {_class['code']} {_class['mark1']} meeting started!\n\t Host: {_class['host1']}")
                web.open(_class["link1"])
            else:
                print(f"[{time}]: {_class['code']} {_class['mark']} meeting started!\n\t Host: {_class['host']}")
                web.open(_class["link"])

            wait_time = 60 * 40

    if time == "19:05":
        break
    else:
        sleep(wait_time)
