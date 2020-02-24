from linebot.models import (
    TextSendMessage,
)

class JoinHandler():
    def __init__(self, event, line_bot_api):
        self.event = event
        self.line_bot_api = line_bot_api
        member = self.line_bot_api.get_group_member_ids(event.source.group_id)
        print(member.member_ids)
        print(member.next)