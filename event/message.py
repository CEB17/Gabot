from linebot.models import (
    TextMessage,
    ImageMessage,
    ImageSendMessage
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
            if event.source.type == "group" and event.source.group_id == os.getenv('GROUP_ID', None):
                if "@Gabot" in event.message.text:
                    Greet(event, line_bot_api, botname)
                elif "@all" in event.message.text:
                    Mention(event,line_bot_api)
                else:
                    Member(event, line_bot_api)

            elif event.source.type == "user":
                Greet(event, line_bot_api)
                Reminder(event, line_bot_api)
        elif isinstance(event.message, ImageMessage):
            message_id = event.message.id
            img = line_bot_api.get_message_content(message_id)

            with open("image.jpg", 'wb') as fd:
                for chunk in img.iter_content():
                    fd.write(chunk)
            
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='image.jpg',
                    preview_image_url='image.jpg'
                )
            )
