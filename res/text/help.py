# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageAction,
)
# Module for regex
import re

class Help():
    # Constructor
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        # Check if text message content match with regex pattern
        if re.match("\?help$", event.message.text):
            self.showHelp()
        elif re.match("\?help command$", event.message.text):
            self.showCommand()
        elif re.match("\?help member$", event.message.text) and event.source.type == "group":
            self.memberHelp()
        elif re.match("\?help reminder$", event.message.text):
            self.reminderHelp()
        elif re.match("\?help schedule$", event.message.text) and event.source.type == "group":
            self.scheduleHelp()

    def showHelp(self):
        buttons_template_message = None
        if self.event.source.type == "user":
            # Create button template
            buttons_template_message = TemplateSendMessage(
                alt_text='Show help',
                template=ButtonsTemplate(
                    title='List of Command',
                    text='What do you want to know?',
                    actions=[
                        MessageAction(
                            label='Show all command',
                            text='?help command'
                        ),
                        MessageAction(
                            label='Reminder',
                            text='?help reminder'
                        ),
                    ]
                )
            )
        elif self.event.source.type == "group":
            # Create button template
            buttons_template_message = TemplateSendMessage(
                alt_text='Show help',
                template=ButtonsTemplate(
                    title='List of Command',
                    text='What do you want to know?',
                    actions=[
                        MessageAction(
                            label='Show all command',
                            text='?help command'
                        ),
                        MessageAction(
                            label='Reminder',
                            text='?help reminder'
                        ),
                        MessageAction(
                            label='Member',
                            text='?help member'
                        ),
                        MessageAction(
                            label='Schedule',
                            text='?help schedule'
                        ),
                    ]
                )
            )

        if buttons_template_message is None:
            return
        # Send button template
        self.line_bot_api.reply_message(
            self.event.reply_token,
            buttons_template_message
        )

    def showCommand(self):
        msg = None
        if self.event.source.type == "user":
            msg = self.reminderHelp(True)
        elif self.event.source.type == "group":
            msg = self.reminderHelp(True) + '\n\n'
            msg += self.memberHelp(True) + '\n\n'
            msg += self.scheduleHelp(True)
            
        if msg is None:
            return
        # Reply chat and trim whitespace
        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(msg.strip())
        )
    def memberHelp(self, textonly=None):
        msg = '''[Member Commands]
* Find NRP
command: ?nrp --nickname--
example: ?nrp john
response: "2210171000"

* Find name based on NRP
command: ?nrp --number--
example 1: ?nrp 00
example 2: ?nrp 1700
example 3: ?nrp 2210171000
response: "John Doe"

* Find fullname member
command: ?fullname --nickname--
example: ?fullname john
response: "John Doe"
'''
        if textonly:
            return msg.strip()

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(msg.strip())
        )
    def reminderHelp(self, textonly=None):
        if self.event.source.type == "user":
            msg = '''[Reminder Commands]
* Create reminder
command: --your reminder-- #todo
example: Meetup at 7PM #todo
response: (You will be asked to set the date and time)

#Note:
You can only set reminder up to 260 characters
'''
        elif self.event.source.type == "group":
            msg = '''[Reminder Commands]
* Create reminder
command: --your reminder-- #reminder
example: Class would be postponed until 11AM #reminder
response: (You will be asked to set the date and time)

#Note:
You can only set reminder up to 1000 characters
'''
        if textonly:
            return msg.strip()

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                msg.strip()
            )
        )
    def scheduleHelp(self, textonly=None):
        msg = '''[Schedule Commands]
* Create/Update Schedule
command:
/set jadwal
[day]
--Schedule--

example:
/set jadwal
[selasa]
Teori
Praktikum

response:
[SELASA]
Teori
Praktikum

Last updated on --datetime--
by --username--

#Note:
Can only set 1 schedule per message,
You need to send 5 messages to set schedule for 5 different days

* Delete Schedule
command: "/unset jadwal --day--"
example: "/unset jadwal rabu"
response:
[RABU]
Teori
Praktikum

Removed by --username--

* Show schedule
command 1: ?jadwal
response:
[SENIN]
--schedule--

[SELASA]
--schedule--

....

command 2: ?jadwal --day--
example: ?jadwal kamis
response:
[KAMIS]
Teori
Workshop

Last updated on --datetime--
by --username--
'''
        if textonly:
            return msg.strip()

        self.line_bot_api.reply_message(
            self.event.reply_token,
            TextSendMessage(
                msg.strip()
            )
        )