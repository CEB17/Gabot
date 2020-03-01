from linebot.models import (
    TextSendMessage,
    StickerSendMessage
)
import os, re

class JoinHandler():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        if event.source.type == "group":
            if re.match(os.getenv('GROUP_ID', None), event.source.group_id) == None:
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
                
                line_bot_api.reply_message(
                    event.reply_token,
                    StickerSendMessage(
                        package_id="11537",
                        sticker_id="52002758"
                    )
                )

                line_bot_api.leave_group(event.source.group_id)
                return

            line_bot_api.push_message(
                os.getenv('ADMIN', None),
                TextSendMessage(
                    f"I'm joining group {event.source.group_id}"
                )
            )
        elif event.source.type == "room":
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

            line_bot_api.reply_message(
                event.reply_token,
                StickerSendMessage(
                    package_id="11537",
                    sticker_id="52002758"
                )
            )

            line_bot_api.leave_room(event.source.room_id)
            return
