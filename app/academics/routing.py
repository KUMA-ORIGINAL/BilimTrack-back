from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"^ws/journal/$", consumers.GradeJournalConsumer.as_asgi()),
]
