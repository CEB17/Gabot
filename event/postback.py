from linebot.models import (
    TextSendMessage
)

from multidict import CIMultiDict
from controllers.db import *


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
            "datetime" : self.event.postback.params['datetime']
        }

        mongo = db.reminder
        mongo.insert_one(data)

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                text="Reminder has been set"
            )
        )

        
