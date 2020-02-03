from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    PostbackAction,
    MessageAction,
    DatetimePickerAction
)
from time import sleep
from datetime import datetime
import pytz, re

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")

        length = len(self.event.message.text)
        maxchar = 260
        if length > maxchar:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"Uh, sorry. You have {length} characters,\
                        I couldn't receive more than {maxchar} characters."
                )
            )
            return

        if re.match(".*#[Rr]eminder.*", self.event.message.text):
            if re.match(".*#[Ee]vent.*", self.event.message.text):
                self.addEvent()

    def addEvent(self):
        prompt = TemplateSendMessage(
            alt_text="Please choose when will it be held",
            template=ConfirmTemplate(
                text=f"Please choose when will it be held",
                actions=[
                    DatetimePickerAction(
                        label="Set date",
                        data=f"action=set-reminder&type=event&text={self.event.message.text}",
                        mode="datetime",initial=self.now
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
