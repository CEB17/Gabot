# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage
)
# Module for create multidict
from multidict import CIMultiDict
# Module for Database related stuff
from controllers.db import *
# Module for multi-threading
from threading import Thread
# Module for delay
from time import sleep
# Module for setup date time
from datetime import datetime
# Module for timezone and hashing
import pytz, hashlib

class PostbackHandler():
    # Constructor
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        # Set timezone
        self.asia = pytz.timezone('Asia/Jakarta')
        # Get user detail
        self.user = line_bot_api.get_profile(event.source.user_id)
        # If message from personal chat
        if event.source.type == "user":
            # Get user ID
            self.source_id = event.source.user_id
        # If message from group chat
        elif event.source.type == "group":
            # Get group ID
            self.source_id = event.source.group_id

        arr = []
        # Get postback data
        # https://developers.line.biz/en/reference/messaging-api/#postback-event
        q = event.postback.data
        q = q.split('&')
        for data in q:
            arr.append(data.split('='))
        # Create multi dictionary (JSON like)
        self.query = CIMultiDict(arr)

        if self.query['action'] == "set-reminder":
            self.setReminder()
        elif self.query['action'] == "delete-reminder":
            self.deleteReminder()

    def setReminder(self):
        # Create/Use reminder collection
        self.mongo = db.reminder
        # Check if specified datetime is valid
        if self.isOlder(self.event.postback.params['datetime']):
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [
                    StickerSendMessage(
                        package_id="11538",
                        sticker_id="51626508"
                    ),
                    TextSendMessage(
                        text=f"Duh, do you think I'm Doctor Strange? Don't make me laugh @{self.user.display_name}"
                    )
                ]
            )
            return
        # If message content #reminder
        if self.query['type'] == "reminder":
            # Find one data that match parameter
            msg = self.mongo.find_one({"uuid":self.query['id']},{"userId"})
            # Empty data handler and prevent intervention
            if msg is None or self.event.source.user_id != msg['userId']:
                return
            # Find one data from DB and update it
            msg = self.mongo.find_one_and_update({"userId":self.event.source.user_id, "datetime":"unset", "uuid":self.query['id']},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})
            # If data not found
            if msg is None:
                # Update datetime
                self.updateReminder()
                return
            # Create thread
            thread = Thread(target=self.sendReminder, args=[self.source_id, msg['text'], self.event.postback.params['datetime'], self.query['id']])
        # If message content #todo
        elif self.query['type'] == "todo":
            # Use SHA1
            h = hashlib.sha1()
            m = self.event.source.user_id + self.query['text']
            # Hash data
            h.update(m.encode('utf-8'))
            # Find one data that match parameter
            data = self.mongo.find_one_and_update({"uuid":h.hexdigest(), "datetime":"unset"},
            {"$unset" : {"datetime":""}})
            if data is None:
                # Reply chat
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    [
                        TextSendMessage(
                            text="Sorry, I couldn't find your message. Maybe it's already set or expired"
                        ),
                        StickerSendMessage(
                            package_id="11538",
                            sticker_id="51626523"
                        ),
                        TextSendMessage(
                            text="FYI, currently I can't update todo reminder date&time. You need to 'forget' and then create a new one."
                        ),
                        TextSendMessage(
                            text="Pardon my foolishness"
                        )
                    ]
                )

                return
            # Create thread
            thread = Thread(target=self.sendReminder, args=[self.source_id, self.query['text'], self.event.postback.params['datetime'], data['uuid']])
        # Start created thread
        thread.start()

        t = self.event.postback.params['datetime'].split('T')
        # Reply chat
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [
                StickerSendMessage(
                package_id="11538",
                sticker_id="51626520"
               ),
                TextSendMessage(
                    text=f"Reminder has been set to {t[0]} {t[1]}"
                )
            ]
        )

    def sendReminder(self, destination, message, time, id):
        # Countdown to send message
        while 1:
            # Get current time
            now = datetime.now(self.asia)
            # Convert current time format
            now = now.strftime("%Y-%m-%dT%H:%M")
            # Check if current time match with specified time
            if now == time:
                # Get reminder data
                data = self.mongo.find_one({"uuid":id})
                if data is None:
                    return

                try:
                    # If specified time doesn't match with data
                    if time != data['datetime']:
                        return
                except KeyError:
                    pass
                # Send message
                self.line_bot_api.push_message(
                    destination,
                    TextSendMessage(
                        text=message
                    )
                )
                # Delete data
                self.mongo.delete_one({"uuid": id})
                break

    def updateReminder(self):
        if self.query['type'] == "reminder":
            # Find one data and update it
            msg = self.mongo.find_one_and_update({"userId":self.event.source.user_id, "uuid":self.query['id']},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})
            # If data not found
            if msg is None:
                # Reply chat
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        text=f"Sorry @{self.user.display_name} , I couldn't find your message. Maybe it's already expired"
                    )
                )
                return
            # Create thread
            thread = Thread(target=self.sendReminder, args=[self.source_id, msg['text'], self.event.postback.params['datetime'], self.query['id']])
        
        # Currently not support update Todo Reminder
        # elif self.query['type'] == "todo":
        #    return

        # Run thread
        thread.start()
        # Tokenizing
        t = self.event.postback.params['datetime'].split('T')
        # Reply chat
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [
                TextSendMessage(
                    text=f"Reminder has been set to {t[0]} {t[1]}"
                )
            ]
        )

    def deleteReminder(self):
        if self.query['type'] == "todo":
            # Use SHA1
            h = hashlib.sha1()
            m = self.event.source.user_id + self.query['text']
            # Hash data
            h.update(m.encode('utf-8'))
            # Convert hash to string and save to variable
            id = h.hexdigest()

        elif self.query['type'] == "reminder":
            id = self.query['id']
        
        # Create/Use reminder collection
        self.mongo = db.reminder
        # Find one data that match parameter
        data = self.mongo.find_one({"uuid": id}, {"uuid","userId"})
        # If source doesn't match with data
        if self.event.source.type == "group":
            if self.event.source.user_id != data['userId']:
                return
        # If data is not found
        elif data is None:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text="Ah, sorry. I couldn't forget non-existent message."
                )
            )
            return
        # Delete data
        self.mongo.delete_one({"uuid": id})
        # Reply chat
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                text="Alright, then."
            )
        )

    def isOlder(self, t):
        # Tokenizing
        t = t.split('T')
        date = t[0].split('-')
        time = t[1].split(':')
        # Get current time on specified timezone
        now = datetime.now(self.asia)
        now = datetime(now.year,now.month,now.day,now.hour,now.minute)
        # Check whether specified time is later than current time
        if now > datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1])):
            return True

        return False