from linebot.models import (
    TextSendMessage,
)
import re,random,os

class Greet():
    def __init__(self, event, line_bot_api, botname):
        self.event = event
        self.line_bot_api = line_bot_api
        self.botname = botname

        self.greeting()

    def greeting(self):
        hi = "(([Hh]+[a]*[ie]+|[OoUu]+[IiYy]+[t]*)[!]*\s?)"
        pattern = "(([Cc][Uu]+[Yy]+|[Dd]ude|[Mm]ate|[Bb][Oo][Tt]|[Bb]ro|[Pp]+)[!]*)"
        pattern = '^' + hi + '$' +'|' + hi + '?' + pattern + '$' + '|' + '^' + pattern + '$'
        if self.botname in self.event.message.text:
            pattern = self.botname + '\s' + '(' + pattern + ')'

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