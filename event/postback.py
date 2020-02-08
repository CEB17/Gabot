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
        data = {
            "userId" : self.event.source.user_id,
            "source" : self.event.source.type,
            "type" : self.query['type'],
            "datetime" : self.event.postback.params['datetime'],
        }

        mongo = db.reminder
        mongo.insert_one(data)

        t = self.event.postback.params['datetime'].split('T')

        self.line_bot_api.reply_message(
            self.event.reply_token,
            [
                TextSendMessage(
                    text=f"Reminder has been set to {t[0]} {t[1]}"
                )
            ]
        )



        thread = Thread(target=self.sendReminder, args=[self.event.source.user_id, self.query['text'], self.event.postback.params['datetime']])
        thread.start()

    def sendReminder(self, user, message, time):
        from datetime import datetime
        import pytz
        
        while 1:

            asia = pytz.timezone('Asia/Jakarta')
            now = datetime.now(asia)
            now = now.strftime("%Y-%m-%dT%H:%M")

            if now == self.event.postback.params['datetime']:
                self.line_bot_api.push_message(
                    self.event.source.user_id,
                    TextSendMessage(
                        text=self.query['text']
                    )
                )
                break
        
