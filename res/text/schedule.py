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
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")

        if re.match("/set jadwal\n+\[[A-Za-z']+\](\n)+", self.event.message.text):
             self.setSchedule()

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

            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    msg += f"\n\nUpdate by {self.user.display_name}"
                )
            )
    
    def updateSchedule(self, day, schedule):
        mongo = db.schedule
        if re.match("[Ss][Ee][Nn][Ii][Nn]$",day):
            mongo.find_one_and_update(
                {'day': "SENIN"}, {'$set':{'subject': schedule,'last_update': self.now, 'update_by': self.event.source.user_id}}, upsert=True)
        elif re.match("[Ss][Ee][Ll][Aa][Ss][Aa]$",day):
            mongo.find_one_and_update(
                {'day': "SELASA"}, {'$set':{'subject': schedule,'last_update': self.now, 'update_by': self.event.source.user_id}}, upsert=True)
        elif re.match("[Rr][Aa][Bb][Uu]$",day):
            mongo.find_one_and_update(
                {'day': "RABU"}, {'$set':{'subject': schedule,'last_update': self.now, 'update_by': self.event.source.user_id}}, upsert=True)
        elif re.match("[Kk][Aa][Mm][Ii][Ss]$",day):
            mongo.find_one_and_update(
                {'day': "KAMIS"}, {'$set':{'subject': schedule,'last_update': self.now, 'update_by': self.event.source.user_id}}, upsert=True)
        elif re.match("[Jj][Uu][Mm][']?[Aa][Tt]$",day):
            mongo.find_one_and_update(
                {'day': "JUM'AT"}, {'$set':{'subject': schedule,'last_update': self.now, 'update_by': self.event.source.user_id}}, upsert=True)