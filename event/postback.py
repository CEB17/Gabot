from linebot.models import (
    TemplateSendMessage
)
from flask import request
from res.postback import *

class PostbackHandler():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        print(request.args)
        if request.args['action'] == "set-reminder":
            Reminder = SetReminder(event, line_bot_api)