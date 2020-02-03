from linebot.models import (
    TextSendMessage,
    TemplateSendMessage
)

class SetReminder():
    def __init__(self, query, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        self.addEvent()

    def addEvent(self):
        print('oi')
