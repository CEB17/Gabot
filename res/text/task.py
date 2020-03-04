from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    PostbackAction,
    DatetimePickerAction
)
from time import sleep
from datetime import datetime, timedelta
from controllers.db import *
import pytz, re, uuid, hashlib, os

class Task():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")
        self.until = datetime.now(region) + timedelta(60)
        self.until = self.until.strftime("%Y-%m-%dt%H:%M")
        self.user = line_bot_api.get_profile(event.source.user_id)

        if re.match("(.+[\s\n]*)+\s#([Tt][Uu][Gg][Aa][Ss])$", self.event.message.text.strip()):
            msg = self.event.message.text.strip()
            msg = re.split("#([Tt][Uu][Gg][Aa][Ss])", msg)
            length = len(msg[0].strip())
            msg[1] = msg[1].lower()
            maxchar = 500

            if re.search("[a-zA-Z]+", msg[0]) is None or length < 5:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002763"
                    )
                )
                return
            elif length > maxchar:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
                    )
                )
                return