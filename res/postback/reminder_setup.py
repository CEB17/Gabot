from linebot.models import (
    TextSendMessage,
    TemplateSendMessage
)

class SetReminder():
    def __init__(self, request, event, line_bot_api):
        self.line_bot_api = line_bot_api
        print("Query is",request.args)

        if request.args['action'] == "set-reminder":
            self.addEvent()

    def addEvent(self):
        print('oi')
