import json
from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)


class GradeJournalConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = parse_qs(self.scope["query_string"].decode())
        group_id = query_params.get("group_id", [None])[0]
        subject_id = query_params.get("subject_id", [None])[0]

        if not group_id or not subject_id:
            await self.close(code=4001)
            return

        self.group_id = group_id
        self.subject_id = subject_id
        self.room_group_name = f"grades_{group_id}_{subject_id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        logger.info("WS connected -> group=%s subject=%s", group_id, subject_id)

    async def disconnect(self, close_code):
        if hasattr(self, "room_group_name"):
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        logger.info("WS disconnected -> code=%s", close_code)

    # Получение события
    async def grade_marked(self, event):
        await self.send(text_data=json.dumps(event["data"]))
