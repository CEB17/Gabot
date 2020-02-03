from linebot.models import (
    TemplateSendMessage
)
from res.postback import *
from multidict import CIMultiDict

class PostbackHandler():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        arr = []
        data = event.postback.data
        data  = data.split('&')
        for q in data:
            arr.append(q.split('='))
        query = CIMultiDict(arr)
        print(query)

        if query['action'] == "set-reminder":
            Reminder = SetReminder(query, event, line_bot_api)