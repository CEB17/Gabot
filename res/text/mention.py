from linebot.models import (
    TextSendMessage
)

import re

class Mention():
    def __init__(self,event,line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

    def mentionAll(self):
        members = self.line_bot_api.get_group_member_ids("Ca8f1ae3f2b72fc2da7345f4314dd57f0")
        print(members)