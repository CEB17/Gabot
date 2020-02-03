from linebot.models import (
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction,
)
from time import sleep
from datetime import datetime
import pytz, re

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        self.prompt()

    def prompt(self):
        if re.match("[Ss]et\sreminder || [Rr]emind\sme", self.event.message.text):
            timezone = pytz.timezone("Asia/Jakarta")
            now = datetime.now(timezone)
            now = now.strftime("%Y-%m-%dt00:00")

            msg = TemplateSendMessage(
                alt_text="What is it about?",
                template=ButtonsTemplate(
                    thumbnail_image_url="https://image.flaticon.com/teams/slug/freepik.jpg",
                    title="Tell me what is it about?",
                    text="Choose what kind of reminder you are going to set",
                    actions=[
                        PostbackAction(
                            label="Event",
                            data="action=set-reminder&type=event"
                            ),
                        PostbackAction(
                            label="Assignment",
                            data="action=set-reminder&type=assignment"
                        ),
                        PostbackAction(
                            label="Something else",
                            data="action=set-reminder&type=something"
                        )
                    ]
                )
            )

            self.line_bot_api.reply_message(
                self.event.reply_token,
                msg
            )

