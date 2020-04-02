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
        # elif re.match("\?help member$", event.message.text) and event.source.type == "group":
        #     self.memberHelp()
        # elif re.match("\?help reminder$", event.message.text):
        #     self.reminderHelp()
        # elif re.match("\?help schedule$", event.message.text) and event.source.type == "group":
        #     self.scheduleHelp()

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
            msg = '''You need help?
Sure, I'll help
'''
        elif self.event.source.type == "group":
            msg = '''You need help?
Sure, I'll help your group
'''            
        if msg is None:
            return
        self.line_bot_api.reply_message(
            self.event.reply_token,
            msg
        )            
    # def memberHelp(self):
    #     self.line_bot_api.reply_message(
    #         self.event.reply_token,
    #         TextSendMessage(
    #             str.strip()
    #         )
    #     )
    # def reminderHelp(self):
    #     if self.event.source.type == "user":
    #     elif self.event.source.type == "group":

    #     self.line_bot_api.reply_message(
    #         self.event.reply_token,
    #         TextSendMessage(
    #             str.strip()
    #         )
    #     )
    # def scheduleHelp(self):
    #     self.line_bot_api.reply_message(
    #         self.event.reply_token,
    #         TextSendMessage(
    #             str.strip()
    #         )
    #     )