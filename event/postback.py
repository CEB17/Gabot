from linebot.models import (
    TemplateSendMessage
)
from res.postback import *

class PostbackHandler():
    def __init__(self, request, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        Reminder = SetReminder(request, event, line_bot_api)