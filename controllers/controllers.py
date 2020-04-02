# Module for server
from flask import request, abort
# Module for Line SDK
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent,
    MemberJoinedEvent, MemberLeftEvent,
    UnfollowEvent, FollowEvent,PostbackEvent
    )
# Module for event handler
from event import (message,join,postback)
# Module for delay
from time import sleep
# Module for logging
import logging
# Module for multi-threading
import threading
# Homepage content
def index():
    return "<h1> Apa? </h1>"
# Line bot handler
def handler(app,parser,line_bot_api):
    # Header for Line application
    signature = request.headers['X-Line-Signature']
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)
    # Multi threading
    sleep(0.01)
    thread = threading.Thread(target=eventHandler, args=[app, events,line_bot_api])
    thread.start()

    return 'OK'

def eventHandler(app, events, line_bot_api):
    for event in events:
        if isinstance(event, MessageEvent):
            message.MessageHandler(event, line_bot_api)
        elif isinstance(event, JoinEvent):
            join.JoinHandler(event, line_bot_api)
        elif isinstance(event, PostbackEvent):
            postback.PostbackHandler(event, line_bot_api)
