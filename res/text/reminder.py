from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction
)
from time import sleep
from datetime import datetime
import pytz

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        self.prompt()

    def prompt(self):
        if self.event.message.text == "remind me":
            timezone = pytz.timezone("Asia/Jakarta")
            now = datetime.now(timezone)
            now = now.strftime("%Y-%m-%dt00:00")

            msg = TemplateSendMessage(
                alt_text="when?",
                template=ButtonsTemplate(
                    thumbnail_image_url="https://image.flaticon.com/teams/slug/freepik.jpg",
                    image_background_color="#00e676",
                    title="Alright, when?",
                    text="You can set reminder by date n hours",
                    actions=[
                        DatetimePickerAction(
                            label="date",
                            data="action=reminder",
                            mode="datetime",
                            initial=now
                        )
                    ]
                )
            )

            self.line_bot_api.reply_message(
                self.event.reply_token,
                msg
            )

