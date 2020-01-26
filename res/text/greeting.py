from linebot.models import (
    TextSendMessage,
)

def greet(event, line_bot_api):
    if event.message.text == "Cuy!":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Apa cuy???")
        )
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )