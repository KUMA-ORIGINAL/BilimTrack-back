import json
from channels.generic.websocket import AsyncWebsocketConsumer


class GradeJournalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """
        Ожидаем query string ?group_id=...&subject_id=...
        Чтобы все преподаватели одной группы / предмета сидели в общем канале.
        """
        self.group_id = self.scope["url_route"]["kwargs"]["group_id"]
        self.subject_id = self.scope["url_route"]["kwargs"]["subject_id"]
        self.room_group_name = f"grades_{self.group_id}_{self.subject_id}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def grade_marked(self, event):
        await self.send(text_data=json.dumps(event["data"]))
