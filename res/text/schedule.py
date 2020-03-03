from linebot.models import (
    TextSendMessage
)
from controllers.db import *
from datetime import datetime
import re, pytz

class Schedule():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.user = line_bot_api.get_profile(event.source.user_id)
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)
        self.current = self.now.strftime("%D")
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")

        if re.match("/[Ss]et ([Jj]adwal|[Ss]chedule)\n+\[[A-Za-z']{4,10}\](\n)+", self.event.message.text):
            self.setSchedule()
        elif re.match("/[Uu]nset ([Jj]adwal|[Ss]chedule) [A-Za-z']{4,10}$", self.event.message.text):
            self.deleteSchedule()
        elif re.match("\?([Jj]adwal|[Ss]chedule)($|\s[a-zA-Z]{4,10}$)", self.event.message.text):
            self.getSchedule()

    def setSchedule(self):
        msg = ""
        if re.match(".*\n+\[[A-Za-z']+\]\n+.*", self.event.message.text):
            day = re.findall("\n\[[A-Za-z']+\]\n?", self.event.message.text)
            schedule = re.split("\n\[[A-Za-z']+\]\n?", self.event.message.text)
            i = 1
            end = len(day)
            for d in day:
                sc = schedule[i].strip()
                Days = d[2:len(d)-2]
                Days = self.normalize(Days)

                if Days is None or re.match("([a-zA-Z'\-]+(\s)?)+", sc) is None:
                    return
                if i == 1:
                    d = d.lstrip()
                msg += d + sc
                if i != end:
                    msg += '\n'
                self.updateSchedule(Days['day'], sc)
                i += 1
            msg += f"\n\nLast updated on {self.current}\nby {self.user.display_name}"
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(msg)
            )
    
    def updateSchedule(self, day, schedule):
        mongo = db.schedule
        Day = self.normalize(day)
        if Day is None:
            return
        mongo.update_one(
            {'day': Day['day']}, {'$set':{'id': Day['id'],'subject': schedule,'last_update': self.now, 'user': self.event.source.user_id}}, upsert=True
        )

    def getSchedule(self):
        day = None
        if len(self.event.message.text.split(" ")) > 1:
            day = self.event.message.text.split(" ")[1]

        mongo = db.schedule
        i = 0
        msg = ""
        recent = None
        for data in mongo.find({}).sort("id",1):
            t = data['last_update'].split('t')
            date = t[0].split('-')
            time = t[1].split(':')
            last_update = datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            
            if day is not None:
                exist = False
                d = self.normalize(day)
                if d is None:
                    return
                elif d['day'] == data['day']:
                    exist = True
                    user = data['user']
                    recent = last_update
                    msg = f"[{data['day']}]\n" + f"{data['subject']}\n\n"
                    break
            elif i == 0:
                recent = last_update
            elif last_update > recent:
                recent = last_update
                user = data['user']
            msg += f"[{data['day']}]\n" + f"{data['subject']}\n\n"
            i += 1

        try:
            if day is not None and not exist:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        "Umm... sorry, couldn't find it."
                    )
                )
                return
            recent = recent.strftime("%D")
            user = self.line_bot_api.get_profile(user)
            msg += f"Last updated on {recent}\nby {user.display_name}"
        except NameError:
            return

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(msg)
        )

    def deleteSchedule(self):
        mongo = db.schedule
        day = self.event.message.text.split(" ")[2]
        day = self.normalize(day)
        if day is None:
            return
        data = mongo.find_one_and_delete({'day': day['day']})
        if data is None:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage("No data")
            )
            return
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                f"[{data['day']}]\n{data['subject']}\n\nRemoved by {self.user.display_name}"
            )
        )

    def normalize(self, day):
        if re.match("([Ss][Ee][Nn][Ii][Nn]|[Mm][Oo][Nn][Dd][Aa][Yy])$",day):
            return {'id': 0,"day": day.upper()}
        elif re.match("([Ss][Ee][Ll][Aa][Ss][Aa]|[Tt][Uu][Ee][Ss][Dd][Aa][Yy])$",day):
            return {'id': 1,"day": day.upper()}
        elif re.match("([Rr][Aa][Bb][Uu]|[Ww][Ee][Dd][Nn][Ee][Ss][Dd][Aa][Yy])$",day):
            return {'id': 2,"day": day.upper()}
        elif re.match("([Kk][Aa][Mm][Ii][Ss]|[Tt][Hh][Uu][Rr][Ss][Dd][Aa][Yy])$",day):
            return {'id': 3,"day": day.upper()}
        elif re.match("([Jj][Uu][Mm][']?[Aa][Tt]|[Ff][Rr][Ii][Dd][Aa][Yy])$",day):
            return {'id': 4,"day": "JUM'AT"}
