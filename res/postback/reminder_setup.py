from linebot.models import (
    TextSendMessage,
    TemplateSendMessage
)

class SetReminder():
    def __init__(self, event, line_bot_api):
        self.line_bot_api = line_bot_api

    def addEvent(self):
        print('oi')
