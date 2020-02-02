from linebot.models import (
    TemplateSendMessage,
    ConfirmTemplate,
    MessageAction,
    URIAction,
    PostbackAction,
    DatetimePickerAction
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
                        URIAction(
                            label="medium",
                            uri="https://medium.com/"
                        ),
                        PostbackAction(
                            label="postback",
                            data="action=buy"
                        ),
                        URIAction(
                            label="Google",
                            uri="https://Google.com/"
                        ),
                        DatetimePickerAction(
                            label="date",
                            data="time=7",
                            mode="datetime",
                            initial="2020-02-2t00:00"
                        )

                    ]
                )
            )
            self.line_bot_api.reply_message(
                self.event.reply_token,
                msg
            )

