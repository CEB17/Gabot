# Module for Line SDK
from linebot.models import (
    TextMessage,
    ImageMessage,
    ImageSendMessage
)
# Module for text message handler
from res.text import *
# Module for regex and system
import sys, re

class MessageHandler():
    # Constructor
    def __init__(self, event, line_bot_api):
        # Get specified botname
        botname = os.getenv('BOTNAME', None)
        # Handler if botname is not specified
        if botname is None:
            print('Specify BOTNAME as environment variable.')
            sys.exit(1)

        # Text Message handler
        if isinstance(event.message, TextMessage):
            # If message comes from group chat
            if event.source.type == "group" and event.source.group_id == os.getenv('GROUP_ID', None):
                # If bot mentioned
                if botname in event.message.text:
                    Greet(event, line_bot_api, botname)
                else:
                    Member(event, line_bot_api)
                    Reminder(event, line_bot_api)
                    Schedule(event, line_bot_api)
            # If message comes from personal chat
            elif event.source.type == "user":
                Greet(event, line_bot_api)
                Reminder(event, line_bot_api)
        # Image message handler --TBD--
        elif isinstance(event.message, ImageMessage):
            message_id = event.message.id
            img = line_bot_api.get_message_content(message_id)