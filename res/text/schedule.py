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
        self.current = self.now.strftime("%d-%m-%Y %H:%M")
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")

        if re.match("/[Ss]et [Jj]adwal\n+\[[A-Za-z']{4,}\](\n)+", self.event.message.text):
            self.setSchedule()
        elif re.match("\?[Jj]adwal($|\s[a-zA-Z]{4,}$)", self.event.message.text):
            self.getSchedule()

    def setSchedule(self):
        dayPattern = "([Ss][Ee][Nn][Ii][Nn]|[Ss][Ee][Ll][Aa][Ss][Aa]|[Rr][Aa][Bb][Uu]|[Kk][Aa][Mm][Ii][Ss]|[Jj][Uu][Mm][']?[Aa][Tt])$"
        msg = ""
        if re.match(".*\n+\[[A-Za-z']+\]\n+.*", self.event.message.text):
            day = re.findall("\n\[[A-Za-z']+\]\n", self.event.message.text)
            schedule = re.split("\n\[[A-Za-z']+\]\n", self.event.message.text)
            i = 1
            end = len(day)
            for d in day:
                Days = d[2:len(d)-2]
                if re.match(dayPattern, Days) is None:
                    break
                if i == 1:
                    d = d.lstrip()
                sc = schedule[i].strip()
                msg += d + sc
                if i != end:
                    msg += '\n'
                self.updateSchedule(Days, sc)
                i += 1
            msg += f"\n\nLast updated {self.current}\nby {self.user.display_name}"
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(msg)
            )
    
    def updateSchedule(self, day, schedule):
        mongo = db.schedule
        Day = self.normalize(day)
        mongo.find_one_and_update(
            {'day': Day['day']}, {'$set':{'id': Day['id'],'subject': schedule,'last_update': self.now, 'user': self.event.source.user_id}}, upsert=True
        )

    def getSchedule(self, day = None):
        mongo = db.schedule
        if day == None:
            schedule = mongo.find({})


    def normalize(self, day):
        if re.match("[Ss][Ee][Nn][Ii][Nn]$",day):
            return {id: 0,"day": day.upper()}
        elif re.match("[Ss][Ee][Ll][Aa][Ss][Aa]$",day):
            return {id: 1,"day": day.upper()}
        elif re.match("[Rr][Aa][Bb][Uu]$",day):
            return {id: 2,"day": day.upper()}
        elif re.match("[Kk][Aa][Mm][Ii][Ss]$",day):
            return {id: 3,"day": day.upper()}
        elif re.match("[Jj][Uu][Mm][']?[Aa][Tt]$",day):
            return {id: 4,"day": "JUM'AT"}
