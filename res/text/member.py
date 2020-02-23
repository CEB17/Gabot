from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
)
from controllers.db import *

import re

class Member():

    def __init__(self,event,line_bot_api):
        self.event = event
        self.mongo = db.member
        self.line_bot_api = line_bot_api
        self.message = event.message.text.split(" ")

        if re.match("\?[Nn][Rr][Pp]\s[a-zA-Z]+$", event.message.text):
            if len(self.message) == 2:
                return
        elif re.match("\?[Nn][Rr][Pp]\s[\d]+", event.message.text):
            if len(self.message) == 2):
                self.findNRP()

    def findNRP(self):
        if len(self.message[0]) == 2:
            nrp = "22101710" + self.message[0]
        elif len(self.message[0]) == 4:
            if self.message[0][:2] == "17":
                nrp = "22101710" + self.message[0][2:]
            elif self.message[0][:2] == "16":
                nrp = "22101610" + self.message[0][2:]
        elif len(self.message[0]) == 10:
            nrp = self.message[0]
        data = self.mongo.find_one({"nrp" : nrp},{"name"})

        if data is None:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    "ntah"
                )
            )
            return

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                data['name']
            )
        )