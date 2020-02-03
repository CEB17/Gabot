from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    PostbackAction,
    MessageAction
)
from time import sleep
from datetime import datetime
import pytz, re
from controllers.db import *

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        if re.match(".*#[Rr]eminder.*", self.event.message.text):
            if re.match(".*#[Ee]vent.*", self.event.message.text):
                self.addEvent()

    def addEvent(self):
        time = re.split("{}", self.event.message.text)
        print("time is",time)
        datetime = re.split("[Tt]", time[0])
        print("datetime is", datetime)
        date = datetime[0][1:]
        time = datetime[1][:5]

        prompt = TemplateSendMessage(
            alt_text="Are you sure?",
            template=ConfirmTemplate(
                text=f"Your event would be held on {date} at {time}",
                actions=[
                    PostbackAction(
                        label="Yes",
                        data=f"action=reminder&text={self.event.message.text}",
                        display_text="Wokay, I'll remember it",
                    ),
                    MessageAction(
                        label="Forget it",
                        text="Nah, forget it."
                    )
                ]
            )
        )

        self.line_bot_api.reply_message(
            self.event.reply_token,
            prompt            
        )
            