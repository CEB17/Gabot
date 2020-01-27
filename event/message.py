from linebot.models import (
    TextMessage
)
from res.text import *
import sys

class MessageHandler():
    def __init__(self, event, line_bot_api):
        botname = os.getenv('BOTNAME', None)

        if botname is None:
            print('Specify BOTNAME as environment variable.')
            sys.exit(1)

        if isinstance(event.message, TextMessage):
            if event.source.type == "group":
                if "@Gabot" in event.message.text:
                    Greet(event, line_bot_api, botname)

                elif "@all" in event.message.text:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text="who are you calling?")
                    )
            
            elif event.source.type == "user":
                Greet(event, line_bot_api)
