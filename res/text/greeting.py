# MOdule for Line SDK
from linebot.models import (
    TextSendMessage,
)
# Module for regex, OS, and random number
import re,random,os

class Greet():
    # Constructor
    def __init__(self, event, line_bot_api, botname=None):
        self.event = event
        self.line_bot_api = line_bot_api
        self.botname = botname
        # Run greeting function
        self.greeting()

    def greeting(self):
        # Word dictionary
        word = {
            "hi" : "(([Hh]+[Aa]*|[Hh]+[Ee]*)[Ii]+|[Ee][Hh]|[Hh][Ee][Yy]*)",
            "halo" : "(([Hh]+[Ee]+|[Hh]+[Aa]+)[Ll]+[Oo]+)",
            "oi" : "(([Oo]+[Ii]+|[Oo]+[Yy]+)[Tt]*|[Uu]+[Yy]+|[Pp])",
            "slang" : "(([Cc]+[Uu]+[Yy]+)|([Dd][Uu]+[Dd][Ee])|([Mm][Aa][Tt][Ee])|([Bb][Oo][Tt])|([Bb][Rr][Oo]))"
        }

        pattern = ""
        # Word length
        index = len(word)
        count = 1
        # Iterate value of word dictionary
        for regex in word.values():
            # Break loop if 'count' equal to 'index'
            if count == index:
                pattern = pattern + regex
                break
            pattern = pattern + regex + '|'
            count = count + 1
        # Add pattern to add exclamation on each word
        pattern = '((' + pattern + ')|(' + '(' + word["hi"] + '|' + word["halo"] + ')\s' + word["slang"] + '))[!]*'
        # If botname is not defined
        if self.botname is None:
            pattern = '^' + pattern + '$'
        else:
            # If bot mentioned
            if  self.botname in self.event.message.text:
                pattern = self.botname + '\s(' + pattern + ')|(' + pattern + ')\s' + self.botname
        # If message match with regex pattern
        if re.match(pattern, self.event.message.text):
            # Greeting words
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
            # Generate random integer less than equal to length of 'msg'
            i = random.randrange(len(msg))
            # Reply chat
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=msg[i])
            )