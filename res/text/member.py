# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    MessageAction,
)
# Module for DB related stuff
from controllers.db import *
# Module for regex
import re

class Member():
    # Constructor
    def __init__(self,event,line_bot_api):
        self.event = event
        # Create/Use member collection
        self.mongo = db.member
        self.line_bot_api = line_bot_api
        # Tokenizing
        self.message = event.message.text.split(" ")
        # Matching with regex pattern
        if re.match("\?[Nn][Rr][Pp]\s[a-zA-Z']+$", event.message.text):
            self.findNRP()
        elif re.match("\?[Nn][Rr][Pp]\s[\d]+$", event.message.text):
            self.findName()
        elif re.match("\?[Ff]ullname\s[a-zA-Z']+$", event.message.text):
            self.findFullname()

    def findName(self):
        nrp = ""
        # Read message after keyword
        # For example '?nrp 40' becomes ['?nrp', '40']
        # So self.message[1] is 40
        if len(self.message[1]) == 2:
            if "40" in self.message[1]:
                # Check whether member from 2017 or 2016
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
        # Find matching data on DB
        data = self.mongo.find_one({"nrp" : nrp},{"name"})
        # If not found
        if data is None:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    "ntah"
                )
            )
            return
        # Send member data
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                data['name']
            )
        )

    def findNRP(self):
        match = False
        # Get all member data
        for data in self.mongo.find({}):
            for name in data['alias']:
                # If match with parameter
                if re.match(name, self.message[1]):
                    match = True
                    break
            if match:
                # Send member data
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        data['nrp']
                    )
                )
                return

        if not match:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    "ntah"
                )
            )
            return

    def findFullname(self):
        match = False
        # Get all member data
        for data in self.mongo.find({}):
            for name in data['alias']:
                # If match with parameter
                if re.match(name, self.message[1]):
                    match = True
                    break
            if match:
                # Send member data
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        data['name']
                    )
                )
                return

        if not match:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    "ntah"
                )
            )
            return
            
    def prompt(self, nrp):
        # Show option
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
        # Send chat
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