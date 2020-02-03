from flask import request, abort
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, JoinEvent,
    MemberJoinedEvent, MemberLeftEvent,
    UnfollowEvent, FollowEvent,PostbackEvent
    )
from event import (message,join,postback)
from time import sleep
import logging
import threading

def index():
    return "<h1> Apa? </h1>"

def handler(app,parser,line_bot_api):
    signature = request.headers['X-Line-Signature']
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    sleep(0.01)
    thread = threading.Thread(target=eventHandler, args=[events,line_bot_api])
    thread.start()

    return 'OK'

def eventHandler(events, line_bot_api):
    for event in events:
        logging.debug(event)
        if isinstance(event, MessageEvent):
            message.MessageHandler(event, line_bot_api)
        elif isinstance(event, JoinEvent):
            join.JoinHandler(event, line_bot_api)
        elif isinstance(event, PostbackEvent):
            postback.PostbackHandler(event, line_bot_api)