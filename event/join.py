# Module for Line SDK
from linebot.models import (
    TextSendMessage,
    StickerSendMessage
)
# Module for OS and Regex stuff
import os, re

class JoinHandler():
    # Constructor
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        if event.source.type == "group":
            # Matching specified group ID with source
            if re.match(os.getenv('GROUP_ID', None), event.source.group_id) == None:
                # Notice admin
                line_bot_api.push_message(
                    os.getenv('ADMIN', None),
                    [
                        StickerSendMessage(
                            package_id="11539",
                            sticker_id="52114140"
                        ),
                        TextSendMessage(
                            f"Help!! I almost got kidnapped on group {event.source.group_id}"
                        )
                    ]
                )
                # Send message to joined group
                line_bot_api.reply_message(
                    event.reply_token,
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002758"
                    )
                )
                # Leave current group
                line_bot_api.leave_group(event.source.group_id)
                return
            # Notice admin
            line_bot_api.push_message(
                os.getenv('ADMIN', None),
                TextSendMessage(
                    f"I'm joining group {event.source.group_id}"
                )
            )
        # If source is room chat
        elif event.source.type == "room":
            # Notice admin
            line_bot_api.push_message(
                os.getenv('ADMIN', None),
                [
                    StickerSendMessage(
                        package_id="11539",
                        sticker_id="52114140"
                    ),
                    TextSendMessage(
                    f"Help!! I almost got kidnapped on room {event.source.room_id}"
                    )
                ]
            )
            # Send message to current room
            line_bot_api.reply_message(
                event.reply_token,
                StickerSendMessage(
                    package_id="11537",
                    sticker_id="52002758"
                )
            )
            # Leave current room
            line_bot_api.leave_room(event.source.room_id)
            return
