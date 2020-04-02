# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    StickerSendMessage,
    TemplateSendMessage,
    ConfirmTemplate,
    PostbackAction,
    DatetimePickerAction
)
# Module for delay
from time import sleep
# Module for datetime format
from datetime import datetime, timedelta
# Module for DB related stuff
from controllers.db import *
# Utilities
import pytz, re, uuid, hashlib, os

class Reminder():
    # Constructor
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        # Set timezone
        region = pytz.timezone("Asia/Jakarta")
        # Get current time based on timezone
        self.now = datetime.now(region)
        # Change datetime format
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")
        # Get date on 60 days later
        self.until = datetime.now(region) + timedelta(60)
        # Change datetime format
        self.until = self.until.strftime("%Y-%m-%dt%H:%M")
        # Get user data
        self.user = line_bot_api.get_profile(event.source.user_id)
        # If message from personal chat
        if event.source.type == "user":
            self.source_id = event.source.user_id
        # If message from group chat
        elif event.source.type == "group":
            self.source_id = event.source.group_id
        # Create random unique ID
        self.uuid = str(uuid.uuid4())

        # If message match with regex pattern
        if re.match("(.+[\s\n]*)+\s#([Rr][Ee][Mm][Ii][Nn][Dd][Ee][Rr]|[Tt][Oo][Dd][Oo])$", event.message.text):
            # Trim excessive whitespace
            msg = self.event.message.text.strip()
            # Tokenizing
            msg = re.split("#([Rr][Ee][Mm][Ii][Nn][Dd][Ee][Rr]|[Tt][Oo][Dd][Oo])", msg)
            # Detect length of message
            length = len(msg[0].strip())
            # Convert to lowercase
            msg[1] = msg[1].lower()
            # Set default maximum character
            maxchar = 260
            # Set maximum character for reminder in group
            if msg[1] == "reminder" and event.source.type == "group":
                maxchar = 1000
            # Search alphabet in message
            if re.search("[a-zA-Z]+", msg[0]) is None or length < 5:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002763"
                    )
                )
                return
            # If text message content is more than maximum character
            elif length > maxchar:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    TextSendMessage(
                        text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
                    )
                )
                return
            self.addReminder(msg, msg[1])
        # Get list of existed reminder
        elif re.match("\?[Rr]eminder$", event.message.text) and event.source.type == "group":
            self.listReminder()

    def addReminder(self, msg, category):
        # Create/Use reminder collection from DB
        self.mongo = db.reminder

        if category == "reminder" and self.event.source.type == "group":
            count = 0
            # Find data that match with parameter
            for data in self.mongo.find({"userId":self.event.source.user_id, "type":category},{"userId"}):
                count = count + 1
            # All member can only set up to 3 reminders
            if count > 3:
                self.warning(category, "limit")
                return
            # Data model
            data = {
                "userId" : self.event.source.user_id,
                "type" : category,
                "uuid" : self.uuid,
                "created" : self.now,
                "text" : msg[0].strip(),
                "datetime" : "unset"
            }
            # Insert to DB
            self.mongo.insert_one(data)
            # Postback data
            # https://developers.line.biz/en/reference/messaging-api/#postback-action
            query = f"action=set-reminder&type={category}&id={self.uuid}"
            forget = f"action=delete-reminder&type={category}&id={self.uuid}"

        elif category == "todo" and self.event.source.type == "user":
            # Use SHA1
            h = hashlib.sha1()
            # Concate string
            m = self.source_id + msg[0].strip()
            # Hash message
            h.update(m.encode('utf-8'))
            # Convert hash to string
            self.uuid = h.hexdigest()
            # Data model
            data = {
                "uuid" : self.uuid,
                "type" : category,
                "created" : self.now,
                "datetime": "unset"
            }
            # Insert to DB
            self.mongo.insert_one(data)
            # Postback data
            # https://developers.line.biz/en/reference/messaging-api/#postback-action
            query = f"action=set-reminder&type={category}&text={msg[0].strip()}"
            forget = f"action=delete-reminder&type={category}&text={msg[0].strip()}"

        try:
            # Show option
            prompt = TemplateSendMessage(
                alt_text="Please set the date and time",
                template=ConfirmTemplate(
                    text=f"Please set the date and time",
                    actions=[
                        DatetimePickerAction(
                            label="Set date",
                            data=query,
                            mode="datetime",initial=self.now, min=self.now, max=self.until
                        ),
                        PostbackAction(
                            label="Forget it",
                            data=forget,
                            text="Nah, forget it."
                        )
                    ]
                )
            )
        except UnboundLocalError:
            return
        # Reply chat
        self.line_bot_api.reply_message(
            self.event.reply_token,
            prompt
        )
        # Alert user if reminder has not been set
        self.alert(self.uuid, self.source_id)

    def listReminder(self):
        # Create/Use reminder collection from DB
        self.mongo = db.reminder
        # Find data that match parameter
        data = self.mongo.find({"type": "reminder"}, {"userId","text","datetime"})
        str = ""
        # Iterate data
        for i in data:
            # Get user data
            user = self.line_bot_api.get_profile(i['userId'])
            # Show username
            str += f"From {user.display_name}\n"
            # Change datetime format
            if i['datetime'] != "unset":
                t = i['datetime'].split('T')
                date = t[0].split('-')
                i['datetime'] = f"{date[2]}-{date[1]}-{date[0]}T{t[1]}"
            str += f"Due {i['datetime']}\n"
            # Show reminder
            str += f"{i['text']}\n\n"
        # If data not found
        if len(str) == 0:
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                [
                    StickerSendMessage(
                        package_id="11539",
                        sticker_id="52114121"
                    ),
                    TextSendMessage(
                        text=f"There is no reminder yet."
                    )
                ]
            )
            return
        # Send reminder list
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                str.strip()
            )
        )

    def warning(self, category, error):
        if error == "format":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"[Incorrect format]\nPlease put \"#{category}\" on newline at the end of your message"
                )
            )

        elif error == "limit":
            user = self.line_bot_api.get_profile(self.event.source.user_id)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"@{self.user.display_name} can only set up to 3 reminders to group, ask another member to set it"
                )
            )

    def alert(self, eventId, userId):
        tick = 0
        while 1:
            # Find data that match parameter
            amount = self.mongo.find_one({"datetime": "unset", "uuid":eventId}, {"uuid"})
            if amount is None:
                break
            # Count second
            tick += 1
            # If already 20 seconds
            if tick == 20:
                # Notice user
                self.line_bot_api.push_message(
                    userId,
                    [
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002753"
                    ),
                    TextSendMessage(
                        text=f"Sorry @{self.user.display_name} , you haven't set the date and time yet."
                    )
                    ]
                )
            # If already 40 seconds
            elif tick == 40:
                # Notice user
                self.line_bot_api.push_message(
                    userId,
                    [
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002744"
                    ),
                    TextSendMessage(
                        text="Ain't you gonna set it, mate?"
                    )
                    ]
                )
            # If already 60 seconds
            elif tick == 60:
                # Delete message
                self.mongo.delete_one({"datetime": "unset", "uuid":eventId})
                # Notice user
                self.line_bot_api.push_message(
                    userId,
                    [
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002739"
                    ),
                    TextSendMessage(
                        text="Your message has expired, try resend again."
                    )
                    ]
                )
            # Delay 1 second
            sleep(1)