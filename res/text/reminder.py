from linebot.models import (
    TemplateSendMessage,
    ConfirmTemplate,
    MessageAction
)
from time import sleep

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        self.prompt()

    def prompt(self):
        if self.event.message.text == "remind me":
            msg = TemplateSendMessage(
                alt_text="when?",
                template=ConfirmTemplate(
                    text="Alright, when?",
                    actions=[
                        MessageAction(
                            label="later",
                            text="later"
                        ),
                        MessageAction(
                            label="Duh",
                            text="Duh"
                        )
                    ]
                )
            )
            self.line_bot_api.reply_message(
                self.event.reply_token,
                msg
            )

