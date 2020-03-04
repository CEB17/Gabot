from linebot.models import (
    TextMessage,
    ImageMessage,
    ImageSendMessage
)
from res.text import *
import sys, re

class MessageHandler():
    def __init__(self, event, line_bot_api):
        botname = os.getenv('BOTNAME', None)

        if botname is None:
            print('Specify BOTNAME as environment variable.')
            sys.exit(1)

        import logging
        if isinstance(event.message, TextMessage):
            if event.source.type == "group" and event.source.group_id == os.getenv('GROUP_ID', None):
                if botname in event.message.text:
                    logging.info("Enter BOTNAME")
                    Greet(event, line_bot_api, botname)
                elif "@all" in event.message.text:
                    logging.info("Enter MENTION")
                    Mention(event,line_bot_api)
                else:
                    logging.info("Enter MEMBER")
                    Member(event, line_bot_api)
                    logging.info("Enter REMINDER")
                    Reminder(event, line_bot_api)
                    logging.info("Enter SCHEDULE")
                    Schedule(event, line_bot_api)
                    logging.info("Enter TASK")
                    Task(event,line_bot_api)

            elif event.source.type == "user":
                Greet(event, line_bot_api)
                Reminder(event, line_bot_api)
        elif isinstance(event.message, ImageMessage):
            message_id = event.message.id
            img = line_bot_api.get_message_content(message_id)