# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    StickerSendMessage
)
# Module for DB related stuff
from controllers.db import *
# Module for datetime
from datetime import datetime
# Module for regex and timezone
import re, pytz

class Schedule():
    # Constructor
    def __init__(self, event, line_bot_api):
        self.event = event
        # Get user data
        self.user = line_bot_api.get_profile(event.source.user_id)
        self.line_bot_api = line_bot_api
        # Set timezone
        region = pytz.timezone("Asia/Jakarta")
        # Get current time based on timezone
        self.now = datetime.now(region)
        # Change datetime format
        self.current = self.now.strftime("%d/%m/%Y")
        # Time format to save on DB
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")

        # If text message content match with regex pattern
        if re.match("/[Ss]et ([Jj]adwal|[Ss]chedule)\n+\[[A-Za-z']{4,10}\](\n)+", self.event.message.text):
            self.setSchedule()
        elif re.match("/[Uu]nset ([Jj]adwal|[Ss]chedule) [A-Za-z']{4,10}$", self.event.message.text):
            self.deleteSchedule()
        elif re.match("\?([Jj]adwal|[Ss]chedule)($|\s[a-zA-Z]{4,10}$)", self.event.message.text):
            self.getSchedule()

    def setSchedule(self):
        msg = ""
        if re.match(".*\n+\[[A-Za-z']+\]\n+.*", self.event.message.text):
            # Find matched day
            day = re.findall("\n\[[A-Za-z']+\]\n?", self.event.message.text)
            # Tokenizing
            schedule = re.split("\n\[[A-Za-z']+\]\n?", self.event.message.text)
            i = 1
            # Count matched day
            end = len(day)
            # Iterate day
            for d in day:
                # Trim excessive whitespace
                sc = schedule[i].strip()
                # Remove unnecessary symbol
                Days = d[2:len(d)-2]
                # Check if day is valid
                Days = self.normalize(Days)
                # If not match
                if Days is None or re.match("([a-zA-Z'\-]+(\s)?)+", sc) is None:
                    return
                # Trim excessive whitespace
                if i == 1:
                    d = d.lstrip()
                # Concate string
                msg += d + sc
                # Add newline if it's not last line
                if i != end:
                    msg += '\n'
                # Create/Update schedule
                self.updateSchedule(Days['day'], sc)
                i += 1
            # Respond
            msg += f"\n\nLast updated on {self.current}\nby {self.user.display_name}"
            # Send respond
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(msg)
            )
    
    def updateSchedule(self, day, schedule):
        # Create/Use schedule collection from DB
        mongo = db.schedule
        # Check if day is valid
        Day = self.normalize(day)
        # If not valid
        if Day is None:
            return
        # Create/Update schedule
        mongo.update_one(
            {'day': Day['day']}, {'$set':{'id': Day['id'],'subject': schedule,'last_update': self.now, 'user': self.event.source.user_id}}, upsert=True
        )

    def getSchedule(self):
        day = None
        # If tokenizing result is more than 1 array
        if len(self.event.message.text.split(" ")) > 1:
            # Get second array which is 'day'
            day = self.event.message.text.split(" ")[1]
        # Create/Use schedule collection from DB
        mongo = db.schedule
        i = 0
        msg = ""
        recent = None
        # Iterate data and sort by ID ascending
        for data in mongo.find({}).sort("id",1):
            # Tokenizing
            t = data['last_update'].split('t')
            date = t[0].split('-')
            time = t[1].split(':')
            # Set datetime format
            last_update = datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1]))
            
            if day is not None:
                exist = False
                # Check if day is valid
                d = self.normalize(day)
                if d is None:
                    return
                # if day match with data
                elif d['day'] == data['day']:
                    exist = True
                    # Get user ID
                    user = data['user']
                    recent = last_update
                    # Get schedule
                    msg = f"[{data['day']}]\n" + f"{data['subject']}\n\n"
                    break
            # If first iteration
            elif i == 0:
                # Save current update time to compare later
                recent = last_update
            # Comparing update time to show the latest update time
            elif last_update > recent:
                recent = last_update
                user = data['user']
            # Get schedule
            msg += f"[{data['day']}]\n" + f"{data['subject']}\n\n"
            i += 1

        try:
            if day is not None and not exist:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    [
                        StickerSendMessage(
                            package_id=11537,
                            sticker_id=52002754
                        ),
                        TextSendMessage(
                          "Umm... sorry, couldn't find it."
                        )
                    ]
                )
                return
            # Change format data
            recent = recent.strftime("%d/%m/%Y")
            # Get user data
            user = self.line_bot_api.get_profile(user)
            msg += f"Last updated on {recent}\nby {user.display_name}"
        except NameError:
            return
        # Send list of schedule
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(msg)
        )

    def deleteSchedule(self):
        # Create/Use schedule collection from DB
        mongo = db.schedule
        # Get day
        day = self.event.message.text.split(" ")[2]
        # Check if day is valid
        day = self.normalize(day)
        if day is None:
            return
        # Find data that match then delete
        data = mongo.find_one_and_delete({'day': day['day']})
        # If data not found
        if data is None:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage("No data")
            )
            return
        # Reply chat
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                f"[{data['day']}]\n{data['subject']}\n\nRemoved by {self.user.display_name}"
            )
        )

    # Function for checking if day is valid then normalize character
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
