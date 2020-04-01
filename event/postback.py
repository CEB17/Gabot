from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage
)

from multidict import CIMultiDict
from controllers.db import *
from threading import Thread
from time import sleep
from datetime import datetime
import pytz, hashlib

class PostbackHandler():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        self.asia = pytz.timezone('Asia/Jakarta')
        self.user = line_bot_api.get_profile(event.source.user_id)
        if event.source.type == "user":
            self.source_id = event.source.user_id
        elif event.source.type == "group":
            self.source_id = event.source.group_id

        arr = []
        q = event.postback.data
        q = q.split('&')
        for data in q:
            arr.append(data.split('='))
        self.query = CIMultiDict(arr)

        if self.query['action'] == "set-reminder":
            self.setReminder()
        elif self.query['action'] == "delete-reminder":
            self.deleteReminder()

    def setReminder(self):
        self.mongo = db.reminder
        if self.isOlder(self.event.postback.params['datetime']):
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

        if self.query['type'] == "reminder":
            msg = self.mongo.find_one({"uuid":self.query['id']},{"userId"})

            if msg is None or self.event.source.user_id != msg['userId']:
                return

            msg = self.mongo.find_one_and_update({"userId":self.event.source.user_id, "datetime":"unset", "uuid":self.query['id']},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})

            if msg is None:
                self.updateReminder()
                return

            thread = Thread(target=self.sendReminder, args=[self.source_id, msg['text'], self.event.postback.params['datetime'], self.query['id']])
        elif self.query['type'] == "todo":
            h = hashlib.sha1()
            m = self.event.source.user_id + self.query['text']
            h.update(m.encode('utf-8'))
            data = self.mongo.find_one_and_update({"uuid":h.hexdigest(), "datetime":"unset"},
            {"$unset" : {"datetime":""}})
            if data is None:
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
            thread = Thread(target=self.sendReminder, args=[self.source_id, self.query['text'], self.event.postback.params['datetime'], data['uuid']])

        thread.start()

        t = self.event.postback.params['datetime'].split('T')

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
        while 1:
            now = datetime.now(self.asia)
            now = now.strftime("%Y-%m-%dT%H:%M")

            if now == time:
                data = self.mongo.find_one({"uuid":id})
                if data is None:
                    return

                try:
                    if time != data['datetime']:
                        return
                except KeyError:
                    pass

                self.line_bot_api.push_message(
                    destination,
                    TextSendMessage(
                        text=message
                    )
                )
                self.mongo.delete_one({"uuid": id})
                break

    def updateReminder(self):
        if self.query['type'] == "reminder":            
            msg = self.mongo.find_one_and_update({"userId":self.event.source.user_id, "uuid":self.query['id']},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})

            if msg is None:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        text=f"Sorry @{self.user.display_name} , I couldn't find your message. Maybe it's already expired"
                    )
                )
                return

            thread = Thread(target=self.sendReminder, args=[self.source_id, msg['text'], self.event.postback.params['datetime'], self.query['id']])
        
        # Currently not support update Todo Reminder
        # elif self.query['type'] == "todo":
        #    return
        thread.start()

        t = self.event.postback.params['datetime'].split('T')

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
            h = hashlib.sha1()
            m = self.event.source.user_id + self.query['text']
            h.update(m.encode('utf-8'))
            id = h.hexdigest()

        elif self.query['type'] == "reminder":
            id = self.query['id']
            
        self.mongo = db.reminder
        data = self.mongo.find_one({"uuid": id}, {"uuid","userId"})

        if self.event.source.user_id != data['userId']:
            return
        elif data is None:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text="Ah, sorry. I couldn't forget non-existent message."
                )
            )
            return

        self.mongo.delete_one({"uuid": id})
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                text="Alright, then."
            )
        )

    def isOlder(self, t):
        t = t.split('T')
        date = t[0].split('-')
        time = t[1].split(':')
        now = datetime.now(self.asia)
        now = datetime(now.year,now.month,now.day,now.hour,now.minute)

        if now > datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1])):
            return True

        return False