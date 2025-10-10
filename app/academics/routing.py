from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/journal/(?P<group_id>\d+)/(?P<subject_id>\d+)/$",
        consumers.GradeJournalConsumer.as_asgi()
    ),
]
