from linebot.models import (
    TextSendMessage,
)
import re,random

class Greet():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        
        self.greeting()

    def greeting(self):
        hi = "(([Hh][ie]|[OoUu]+[IiYy]+[t]*|[Dd]ude|[Mm]ate)\s?)"
        pattern = "([Cc][Uu]+[Yy]+|[Dd]ude|[Mm]ate|[Bb][Oo][Tt]|[Bb]ro)[!]*"
        if re.match(pattern, self.event.message.text):
            i = random.randrange(10)
            if i == 0:
                msg = "Apa?"
            elif i == 1:
                msg = "Hm??"
            elif i == 2:
                msg = "Oit"
            elif i == 3:
                msg = '??'
            elif i == 4:
                msg = "ha?"
            elif i == 5:
                msg = "wut?"
            elif i == 6:
                msg = "'sup?"
            elif i == 7:
                msg = "Haihai"
            elif i == 8:
                msg = "dalem?"
            elif i == 9:
                msg = "napa?"
            
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=msg)
            )
        else:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=self.event.message.text)
            )