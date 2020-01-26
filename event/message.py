from linebot.models import (
    TextMessage
)
from res.text import *

class MessageHandler():
    def __init__(self, event, line_bot_api):
        if isinstance(event.message, TextMessage):
            Greet(event, line_bot_api)