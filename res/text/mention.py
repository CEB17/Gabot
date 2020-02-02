from linebot.models import (
    TextSendMessage
)

import re

class Mention():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api