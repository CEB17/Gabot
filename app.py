from __future__ import unicode_literals #backward compatibility for python2
# Module for os or system related stuff
import os, sys, threading
# Module for HTTP GET
import urllib.request
# Module for delay
from time import sleep
# Module for building server
from flask import Flask, request, abort
from router.router import *
# Module for Line SDK
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

# Prevent heroku from idling
def keepAlive():
    while 1:
        with urllib.request.urlopen(os.getenv('HOST_URL', None)) as response:
            html = response.read()
            print('PING')
            sleep(1)

# Create application server
app = Flask(__name__)

# Start thread to ping server
thread = threading.Thread(target=keepAlive)
thread.start()

# Environment variabel
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None) 
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# Handler
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# Init API and Webhook
line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

# Router
router(app, parser, line_bot_api)

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=os.getenv('PORT', None))