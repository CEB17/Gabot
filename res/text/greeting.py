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
            "hi" : "(([Hh]+[Aa]*|[Hh]+[Ee]*)[Ii]+|[Ee][Hh]|[Hh][Ee][Yy]*)",
            "halo" : "(([Hh]+[Ee]+|[Hh]+[Aa]+)[Ll]+[Oo]+)",
            "oi" : "(([Oo]+[Ii]+|[Oo]+[Yy]+)[Tt]*|[Uu]+[Yy]+|[Pp])",
            "slang" : "(([Cc]+[Uu]+[Yy]+)|([Dd][Uu]+[Dd][Ee])|([Mm][Aa][Tt][Ee])|([Bb][Oo][Tt])|([Bb][Rr][Oo]))"
        }

        pattern = ""
        index = len(word)
        count = 1
        for regex in word.values():
            if count == index:
                pattern = pattern + regex
                break
            pattern = pattern + regex + '|'
            count = count + 1
        
        pattern = '((' + pattern + ')|(' + '(' + word["hi"] + '|' + word["halo"] + ')\s' + word["slang"] + '))[!]*'
        if self.botname is None:
            pattern = '^' + pattern + '$'
        else:
            if  self.botname in self.event.message.text:
                pattern = self.botname + '\s(' + pattern + ')|(' + pattern + ')\s' + self.botname

        if re.match(pattern, self.event.message.text):
            msg = [
                "Apa?",
                "Hm??",
                "Oit",
                "??",
                "ha?",
                "wut?",
                "'sup?",
                "Iya?",
                "dalem?",
                "napa?"
            ]

            i = random.randrange(len(msg))
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=msg[i])
            )
        # else:
        #     self.line_bot_api.reply_message(
        #         self.event.reply_token,
        #         TextSendMessage(text=self.event.message.text)
        #     )