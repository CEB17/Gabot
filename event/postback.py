from linebot.models import (
    TextSendMessage,
    TemplateSendMessage
)

from multidict import CIMultiDict
from controllers.db import *
from threading import Thread
from time import sleep


class PostbackHandler():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        arr = []
        q = event.postback.data
        q = q.split('&')
        for data in q:
            arr.append(data.split('='))
        self.query = CIMultiDict(arr)

        if self.query['action'] == "set-reminder":
            self.setReminder()

    def setReminder(self):

        if self.query['type'] == "event":
            self.mongo = db.reminder
            
            self.mongo.find_one_and_update({"userId":self.event.source.user_id, "datetime":"unset", "eventId":self.query['id']},
            {"$set" : {"datetime":self.event.postback.params['datetime']}})

            msg = self.mongo.find_one({"userId":self.event.source.user_id, "datetime":self.event.postback.params['datetime']},{"text"})

            if msg is None:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    text="Sorry, I couldn't find your message. Maybe you already set it or it's already expired"
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
        from datetime import datetime
        import pytz
        
        while 1:

            asia = pytz.timezone('Asia/Jakarta')
            now = datetime.now(asia)
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
        
