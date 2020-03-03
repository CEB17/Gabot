from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    PostbackAction,
    DatetimePickerAction
)
from controllers.db import *
from datetime import datetime
import re,pytz

class Task():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)

        if re.match("(.+[\s\n]*)+\s#[Tt][Uu][Gg][Aa][Ss]$", self.event.message.text.strip()):
            length = len(event.message.text.strip())
            maxchar = 500
            if length - 10 > maxchar:
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                        StickerSendMessage(
                            package_id="11538",
                            sticker_id="51626525"
                        ),
                        TextSendMessage(
                            text=f"H-Hold on!!! You have {length} characters, I couldn't receive more than {maxchar} characters."
                        )
                    ]
                )
                return
            self.addMemo()

    def addMemo(self):
        msg = re.split("#([Tt][Uu][Gg][Aa][Ss])", self.event.message.text.strip())
        if re.search("[a-zA-Z]+", msg[0]) is None or len(msg[0].strip()) < 5:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                StickerSendMessage(
                    package_id="11537",
                    sticker_id="52002763"
                )
            )
            return