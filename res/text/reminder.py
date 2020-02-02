from linebot.models import (
    TextSendMessage,
)
from time import sleep

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        self.setReminder()

    def setReminder(self):
        if self.event.message.text == "remind me":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage("Alright, when?")
            )
            while True:
                if self.event.message.text == "later":
                    sleep(3)
                    self.line_bot_api.reply_message(
                        self.event.reply_token,
                        TextSendMessage("Hey, Just want to remind you")
                    )
                    break


