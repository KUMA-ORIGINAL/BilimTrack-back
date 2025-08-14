from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, permissions
from ..models import LessonTopic
from ..serializers import LessonTopicSerializer


@extend_schema(
    tags=["Mentor"],
    summary="Список и создание тем уроков",
    description="Ментор может получать список и создавать темы только для своих предметов.",
    parameters=[
        OpenApiParameter(
            name="subject",
            type=str,
            location=OpenApiParameter.QUERY,
            description="ID предмета для фильтрации тем",
            required=False
        )
    ],
    responses={200: LessonTopicSerializer(many=True)}
)
class LessonTopicListCreateView(generics.ListCreateAPIView):
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
