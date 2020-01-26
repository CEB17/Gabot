from linebot.models import (
    TextMessage
)
from res import (text)

class MessageHandler():
    def __init__(self, event, line_bot_api):
        if isinstance(event.message, TextMessage):
            text.greeting.greet(event, line_bot_api)