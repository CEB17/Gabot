from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    MessageAction,
)
from controllers.db import *

import re

class Member():

    def __init__(self,event,line_bot_api):
        self.event = event
        self.mongo = db.member
        self.line_bot_api = line_bot_api
        self.message = event.message.text.split(" ")

        if re.match("\?[Nn][Rr][Pp]\s[a-zA-Z']+$", event.message.text):
            self.findNRP()
        elif re.match("\?[Nn][Rr][Pp]\s[\d]+$", event.message.text):
            self.findName()
        elif re.match("\?[Ff]ullname\s[a-zA-Z']+$", event.message.text):
            self.findFullname()

    def findName(self):
        nrp = ""
        if len(self.message[1]) == 2:
            if "40" in self.message[1]:
                self.prompt("40")
                return
            nrp = "22101710" + self.message[1]
        elif len(self.message[1]) == 4:
            if self.message[1][:2] == "17":
                nrp = "22101710" + self.message[1][2:]
            elif self.message[1][:2] == "16":
                nrp = "22101610" + self.message[1][2:]
        elif len(self.message[1]) == 10:
            nrp = self.message[1]
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

    def findNRP(self):
        match = False
        for data in self.mongo.find({}):
            for name in data['alias']:
                if re.match(name, self.message[1]):
                    match = True
                    break
            if match:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        data['nrp']
                    )
                )
                return

    def findFullname(self):
        match = False
        for data in self.mongo.find({}):
            for name in data['alias']:
                if re.match(name, self.message[1]):
                    match = True
                    break
            if match:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        data['name']
                    )
                )
                return

    def prompt(self, nrp):
        confirm_template = TemplateSendMessage(
            alt_text="Which?",
            template=ConfirmTemplate(
                text="Which?",
                actions=[
                    MessageAction(
                        label=f"22101610{nrp}",
                        text=f"?nrp 16{nrp}"
                    ),
                    MessageAction(
                        label=f"22101710{nrp}",
                        text=f"?nrp 17{nrp}"
                    )
                ]
            )
        )
        self.line_bot_api.reply_message(
            self.event.reply_token,
            [
                StickerSendMessage(
                    package_id= "11539",
                    sticker_id= "52114129"
                ),
                confirm_template
            ]
        )
        return