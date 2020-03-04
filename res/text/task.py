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

        if re.match("(.+[\s\n]*)+\s#([Tt][Uu][Gg][Aa][Ss])$", self.event.message.text.strip()):
            msg = self.event.message.text.strip()
            msg = re.split("#([Tt][Uu][Gg][Aa][Ss])", msg)
            length = len(msg[0].strip())
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
                import logging
                logging.info("length > maxchar")
                logging.info(f"{length > maxchar}")
                logging.info(f"{length}")
                return
            import logging
            logging.info("length > maxchar")
            logging.info(f"{length > maxchar}")
            logging.info(f"{length}")
            self.addMemo(msg)

    def addMemo(self, msg):
        pass