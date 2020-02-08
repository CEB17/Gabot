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
                    text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
                )
            )
            return

        if re.match(".*#[Rr]eminder.*", self.event.message.text):
            if re.match(".*#[Ee]vent.*", self.event.message.text):
                self.addReminder("#[Ee]vent", "event")
            elif re.match(".*#[Tt]odo.*", self.event.message.text):
                self.addReminder("#[Tt]odo", "todo")

    def addReminder(self, regex, category):
        
        msg = re.split(f"(#[Rr]eminder\s{regex})|({regex}\s#[Rr]eminder)",self.event.message.text)

        if len(msg) < 3:
            self.warning(category)
            return

        elif re.search(f"(#[Rr]eminder\s{regex})|({regex}\s#[Rr]eminder)",msg[0]) is not None:
            self.warning(category)
            return
        
        elif re.match("^\s*$", msg[3]) is None:
            self.warning(category)
            return

        prompt = TemplateSendMessage(
            alt_text="Please choose when will it be held",
            template=ConfirmTemplate(
                text=f"Please choose when will it be held",
                actions=[
                    DatetimePickerAction(
                        label="Set date",
                        data=f"action=set-reminder&type={category}&text={msg[0]}",
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

    def warning(self, category):
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"[Incorrect format] Please put \"#reminder #{category}\" at the end of your message"
                )
            )