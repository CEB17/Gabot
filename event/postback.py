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
import pytz


class PostbackHandler():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        self.asia = pytz.timezone('Asia/Jakarta')

        arr = []
        q = event.postback.data
        q = q.split('&')
        for data in q:
            arr.append(data.split('='))
        self.query = CIMultiDict(arr)

        if self.query['action'] == "set-reminder":
            self.setReminder()
        elif self.query['action'] == "delete-reminder":
            self.deleteReminder(self.event.source.user_id, self.query['id'])

    def setReminder(self):

        if self.isOlder(self.event.postback.params['datetime']):
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [
                    StickerSendMessage(
                        package_id="11538",
                        sticker_id="51626508"
                    ),
                    TextSendMessage(
                        text="Duh, do you think I'm Dr.Strange? Don't make me laugh"
                    )
                ]
            )
            return

        if self.query['type'] == "event":
            self.mongo = db.reminder
            
            self.mongo.find_one_and_update({"userId":self.event.source.user_id, "datetime":"unset", "eventId":int(self.query['id'])},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})

            msg = self.mongo.find_one({"userId":self.event.source.user_id, "datetime":self.event.postback.params['datetime']},{"text"})

            if msg is None:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        text="Sorry, I couldn't find your message. Maybe you already set it or it's already expired"
                    )
                )
                return

            thread = Thread(target=self.sendReminder, args=[self.event.source.user_id, msg['text'], self.event.postback.params['datetime']])
        elif self.query['type'] == "todo":
            thread = Thread(target=self.sendReminder, args=[self.event.source.user_id, self.query['text'], self.event.postback.params['datetime']])

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

    def sendReminder(self, destination, message, time):        
        while 1:
            now = datetime.now(self.asia)
            now = now.strftime("%Y-%m-%dT%H:%M")

            if now == time:
                self.line_bot_api.push_message(
                    destination,
                    TextSendMessage(
                        text=message
                    )
                )
                self.mongo.delete_one({"userId":destination, "datetime":now})
                break

    def deleteReminder(self, userId, eventId):
        amount = self.mongo.find_one({"userId": userId, "eventId": int(eventId)}, {"eventId"})

        if amount is None:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text="Ah, sorry. I couldn't forget non-existent message."
                )
            )
            return

        self.mongo.delete_one({"userId": userId, "eventId": int(eventId)})
        
    def isOlder(self, t):
        t = t.split('T')
        date = t[0].split('-')
        time = t[1].split(':')
        now = datetime.now(self.asia)
        now = datetime(now.year,now.month,now.day,now.hour,now.minute)

        if now > datetime(int(date[0]),int(date[1]),int(date[2]),int(time[0]),int(time[1])):
            return True

        return False