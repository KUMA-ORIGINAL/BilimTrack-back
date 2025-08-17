from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter

from ..models import LessonTopic
from ..serializers import LessonTopicSerializer


@extend_schema(
    tags=["Mentor Lesson Topics"],
    parameters=[
        OpenApiParameter(
            name="subject",
            type=str,
            location=OpenApiParameter.QUERY,
            description="ID предмета для фильтрации тем",
            required=False
        )
    ],
)
class LessonTopicViewSet(viewsets.ModelViewSet):
    serializer_class = LessonTopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = LessonTopic.objects.filter(mentor=self.request.user)
        subject_id = self.request.query_params.get('subject')
        if subject_id:
            qs = qs.filter(subject_id=subject_id)
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context