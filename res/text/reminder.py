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
import pytz, re, uuid, hashlib

class Reminder():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        region = pytz.timezone("Asia/Jakarta")
        self.now = datetime.now(region)
        self.now = self.now.strftime("%Y-%m-%dt%H:%M")
        self.until = datetime.now(region) + timedelta(60)
        self.until = self.until.strftime("%Y-%m-%dt%H:%M")
        self.uuid = str(uuid.uuid4())

        msg = self.event.message.text.replace('\n','')

        if re.match(".*#[Rr]eminder.*", msg):
            if re.match(".*#[Ee]vent.*", msg):
                length = len(self.event.message.text.strip())
                maxchar = 1000
                if length - 15 > maxchar:
                    self.line_bot_api.reply_message(
                        self.event.reply_token,
                        TextSendMessage(
                            text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
                        )
                    )
                    return
                self.addReminder("#[Ee]vent", "event")
            elif re.match(".*#[Tt]odo.*", msg):
                length = len(self.event.message.text.strip())
                maxchar = 260
                if length - 15 > maxchar:
                    self.line_bot_api.reply_message(
                        self.event.reply_token,
                        TextSendMessage(
                            text=f"Uh, sorry. You have {length} characters, I couldn't receive more than {maxchar} characters."
                        )
                    )
                    return
                self.addReminder("#[Tt]odo", "todo")

    def addReminder(self, regex, category):
        self.mongo = db.reminder
        msg = re.split(f"(#[Rr]eminder\s{regex})|({regex}\s#[Rr]eminder)",self.event.message.text)

        if len(msg) < 3:
            self.warning(category, "format")
            return

        elif re.search(f"(#[Rr]eminder\s{regex})|({regex}\s#[Rr]eminder)",msg[0].replace('\n','')) is not None:
            self.warning(category, "format")
            return
        
        elif re.match("^\s*$", msg[3]) is None:
            self.warning(category, "format")
            return

        if category == "event":
            count = 0

            for data in self.mongo.find({"userId":self.event.source.user_id, "type":"event"},{"userId"}):
                count = count + 1

            if count > 3:
                self.warning(category, "limit")
                return

            data = {
                "userId" : self.event.source.user_id,
                "source" : self.event.source.type,
                "type" : category,
                "uuid" : self.uuid,
                "created" : self.now,
                "text" : msg[0].strip(),
                "datetime" : "unset"
            }

            self.mongo.insert_one(data)
            query = f"action=set-reminder&type={category}&id={self.uuid}"
            forget = f"action=delete-reminder&type={category}&id={self.uuid}"

        elif category == "todo":
            h = hashlib.sha1()
            m = self.event.source.user_id + msg[0].strip()
            h.update(m.encode('utf-8'))
            data = {
                "uuid" : h.hexdigest(),
                "type" : category,
                "created" : self.now
            }

            self.mongo.insert_one(data)

            query = f"action=set-reminder&type={category}&text={msg[0].strip()}"
            forget = f"action=delete-reminder&type={category}&text={msg[0].strip()}"

        prompt = TemplateSendMessage(
            alt_text="Please choose when will it be held",
            template=ConfirmTemplate(
                text=f"Please choose when will it be held",
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

        self.alert(self.uuid, self.event.source.user_id)

    def warning(self, category, error):

        if error == "format":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"[Incorrect format] Please put \"#reminder #{category}\" at the end of your message"
                )
            )

        elif error == "limit":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(
                    text=f"You can only set up to 3 {category} reminders to group, ask KY if you need help"
                )
            )

    def alert(self, eventId, userId):
        tick = 0
        while 1:
            amount = self.mongo.find_one({"userId":userId, "datetime": "unset", "uuid":eventId}, {"uuid"})
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
                        text="Sorry, you haven't set the date and time yet."
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
                self.mongo.delete_one({"userId":userId, "datetime": "unset", "uuid":eventId})
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