from linebot.models import (
    TextSendMessage,
)
import re,random,os

class Greet():
    def __init__(self, event, line_bot_api, botname=None):
        self.event = event
        self.line_bot_api = line_bot_api
        self.botname = botname

        self.greeting()

    def greeting(self):
        word = {
            "hi" : "(([Hh]+[Aa]*|[Hh]+[Ee]*)[Ii]+|[Ee][Hh])",
            "halo" : "(([Hh]+[Ee]+|[Hh]+[Aa]+)[Ll]+[Oo]+)",
            "oi" : "(([Oo]+[Ii]+|[Oo]+[Yy]+)[Tt]*|[Uu]+[Yy]+|[Pp])",
            "slang" : "([Cc]+[Uu]+[Yy]+)|([Dd][Uu]+[Dd][Ee])|([Mm][Aa][Tt][Ee])|([Bb][Oo][Tt])|([Bb][Rr][Oo])"
        }

        pattern = ""
        for regex in word.values():
            pattern = pattern + '^' + regex + '$ |'
        pattern = '(' + pattern + '(' + word["hi"] + '|' + word["halo"] + ')\s' + word["slang"] + ')[!]*'

        if self.botname is not None:
            if  self.botname in self.event.message.text:
                pattern = '^' + self.botname + '\s' + pattern + '|' + pattern + '\s' + self.botname + '$'

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
                msg = "Iya?"
            elif i == 8:
                msg = "dalem?"
            elif i == 9:
                msg = "napa?"
            print(self.event.source)
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=msg)
            )
        else:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=self.event.message.text)
            )