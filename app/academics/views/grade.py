from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, permissions, mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Grade, Session
from ..permissions import IsMentorOrReadOnly
from ..serializers import GradeSerializer, StudentGradeSerializer, GradeCreateSerializer, SessionShortSerializer, \
    UserShortSerializer, GradeShortSerializer, AttendanceMarkRequestSerializer, AttendanceMarkSerializer

User = get_user_model()


@extend_schema(
    tags=['Grade Mentor'],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получить оценки студентов по subject id',
        parameters = [
            OpenApiParameter(
                name='subject_id',
                description='ID of the subject for filtering grades',
                required=True,
                type=OpenApiTypes.INT,  # Тип параметра - целое число
                location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
            ),
            OpenApiParameter(
                name='group_id',
                description='ID of the group for filtering grades',
                required=True,
                type=OpenApiTypes.INT,  # Тип параметра - целое число
                location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
            )
        ]
    ),
    create=extend_schema(
        summary='Создание оценки для студента'
    ),
    update=extend_schema(
        summary='Изменение оценки для студента'
    ),
    partial_update=extend_schema(
        summary='Частичное изменение оценки для студента'
    ),
)
class MentorGradeViewSet(viewsets.GenericViewSet,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.ListModelMixin):
    permission_classes = [IsMentorOrReadOnly]

    def get_queryset(self):
        return Grade.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return GradeCreateSerializer
        elif self.action == 'list':
            return StudentGradeSerializer
        return GradeSerializer

    def list(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id')
        subject_id = request.query_params.get('subject_id')
        if not group_id or not subject_id:
            return Response({"error": "group_id and subject_id are required"}, status=400)

        sessions = Session.objects.filter(subject_id=subject_id).order_by('date')
        sessions_data = SessionShortSerializer(sessions, many=True).data

        users = User.objects.filter(group_id=group_id)

        grades_list = []
        for user in users:
            grades = Grade.objects.filter(user=user, session__in=sessions)
            user_data = {
                "user": UserShortSerializer(user).data,
                "scores": GradeShortSerializer(grades, many=True).data
            }
            grades_list.append(user_data)

        return Response({
            "sessions": sessions_data,
            "grades": grades_list
        })


@extend_schema(
    tags=['Grade student me'],
    parameters = [
        OpenApiParameter(
            name='subject_id',
            description='ID of the subject for filtering grades',
            required=False,
            type=OpenApiTypes.INT,  # Тип параметра - целое число
            location=OpenApiParameter.QUERY  # Указание того, что параметр находится в строке запроса
        )
    ]
)
class StudentGradeAPIView(generics.RetrieveAPIView):
    serializer_class = StudentGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        subject_id = int(request.query_params.get('subject_id'))
        grades = Grade.objects.filter(user=user, subject_id=subject_id)
        data = {
            'user': user,
            'scores': grades
        }
        serializer = self.get_serializer(data)
        return Response(serializer.data)


class MarkAttendanceAPIView(APIView):
    """
    POST {"session_id": "..."}
    Отмечает присутствие (grade=5) текущего пользователя на занятии.
    Если отметка уже стоит — ничего не меняет.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=AttendanceMarkRequestSerializer,
        responses={
            200: OpenApiResponse(response=AttendanceMarkSerializer, description="Уже отмечено"),
            201: OpenApiResponse(response=AttendanceMarkSerializer, description="Отметка создана"),
            400: OpenApiResponse(description="Нет session_id"),
        }
    )
    def post(self, request):
        serializer = AttendanceMarkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data['session_id']
        user = request.user

        session = get_object_or_404(Session, id=session_id)
        grade = Grade.objects.filter(user=user, session=session, grade=5).first()
        already_marked = False

        if grade:
            already_marked = True
        else:
            grade = Grade.objects.create(
                user=user,
                session=session,
                grade=5
            )

        response_serializer = AttendanceMarkSerializer(grade)
        return Response({
            'marked': True,
            'already_marked': already_marked,
            **response_serializer.data
        }, status=status.HTTP_200_OK if already_marked else status.HTTP_201_CREATED)