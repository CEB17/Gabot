from linebot.models import (
    TextSendMessage,
)
import os

class JoinHandler():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api

        if event.source.group_id != os.getenv('GROUP_ID', None):
            line_bot_api.push_message(
                os.getenv('ADMIN', None),
                TextSendMessage(
                    f"Help!!0x10001C I almost got kidnapped on {event.source.group_id}"
                )
            )
            line_bot_api.leave_group(event.source.group_id)
            return
        elif event.source.type == "room":
            line_bot_api.push_message(
                os.getenv('ADMIN', None),
                TextSendMessage(
                    f"Help!!0x10001C I almost got kidnapped on {event.source.room_id}"
                )
            )
            line_bot_api.leave_room(event.source.room_id)
            return

        line_bot_api.push_message(
            os.getenv('ADMIN', None),
            TextSendMessage(
                f"I'm joining group {event.source.group_id}"
            )
        )