from linebot.models import (
    TextSendMessage,
)

class Greet():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        
        self.greet()

    def greet(self):
        if self.event.message.text == "Cuy!":
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text="Apa cuy???")
            )
        else:
            self.line_bot_api.reply_message(
                self.event.reply_token,
                TextSendMessage(text=self.event.message.text)
            )