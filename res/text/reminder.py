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

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")
        self.until = datetime.now(region) + timedelta(60)
        self.until = self.until.strftime("%Y-%m-%dt%H:%M")
        self.user = line_bot_api.get_profile(event.source.user_id)
        if event.source.type == "user":
            self.source_id = event.source.user_id
        elif event.source.type == "group":
            self.source_id = event.source.group_id
        self.uuid = str(uuid.uuid4())

        msg = self.event.message.text.strip()

        if re.match(".+\s[\n]*#([Rr][Ee][Mm][Ii][Nn][Dd][Ee][Rr]|[Tt][Oo][Dd][Oo])$", msg):
            msg = re.split("#([Rr][Ee][Mm][Ii][Nn][Dd][Ee][Rr]|[Tt][Oo][Dd][Oo])", msg)
            length = len(msg[0].strip())
            msg[1] = msg[1].lower()
            maxchar = 260
            if msg[1] == "reminder" and event.source.type == "group":
                maxchar = 1000

            if re.search("[a-zA-Z]+", msg[0]) is None or length < 5:
                self.line_bot_api.reply_message(
                    self.event.reply_token,
                    StickerSendMessage(
                        package_id=11537
                        sticker_id=52002763
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
            self.addReminder(msg, msg[1])
        # elif re.match(".+\s[\n]*#([Tt][Oo][Dd][Oo])$", msg):
        #     length = len(self.event.message.text.strip())
        #     maxchar = 260
        #     if length - 15 > maxchar:
        #         self.line_bot_api.reply_message(
        #             self.event.reply_token,
        #             TextSendMessage(
        #                 text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
        #             )
        #         )
        #         return
        #     self.addReminder("#[Tt]odo", "todo")

    def addReminder(self, msg, category):
        self.mongo = db.reminder

        if category == "reminder" and self.event.source.type == "group":
            count = 0

            for data in self.mongo.find({"userId":self.source_id, "type":category},{"userId"}):
                count = count + 1

            if count > 3:
                self.warning(category, "limit")
                return

            data = {
                "userId" : self.source_id,
                "type" : category,
                "uuid" : self.uuid,
                "created" : self.now,
                "text" : msg[0].strip(),
                "datetime" : "unset"
            }

            self.mongo.insert_one(data)
            query = f"action=set-reminder&type={category}&id={self.uuid}"
            forget = f"action=delete-reminder&type={category}&id={self.uuid}"

        elif category == "todo" and self.event.source.type == "user":
            h = hashlib.sha1()
            m = self.source_id + msg[0].strip()
            h.update(m.encode('utf-8'))
            self.uuid = h.hexdigest()
            data = {
                "uuid" : self.uuid,
                "type" : category,
                "created" : self.now,
                "datetime": "unset"
            }

            self.mongo.insert_one(data)

            query = f"action=set-reminder&type={category}&text={msg[0].strip()}"
            forget = f"action=delete-reminder&type={category}&text={msg[0].strip()}"

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

        self.line_bot_api.reply_message(
            self.event.reply_token,
            prompt
        )

        self.alert(self.uuid, self.source_id)

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
            amount = self.mongo.find_one({"datetime": "unset", "uuid":eventId}, {"uuid"})
            if amount is None:
                break

            tick = tick + 1
            if tick == 20:
                self.line_bot_api.push_message(
                    userId,
                    [
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002753"
                    ),
                    TextSendMessage(
                        text=f"Sorry @{self.user.display_name}, you haven't set the date and time yet."
                    )
                    ]
                )

            elif tick == 40:
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

            elif tick == 60:
                self.mongo.delete_one({"datetime": "unset", "uuid":eventId})
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
            sleep(1)