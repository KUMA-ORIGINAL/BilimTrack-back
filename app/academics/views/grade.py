from django.contrib.auth import get_user_model
from django.db.models import Count, OuterRef, Exists
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiResponse
from rest_framework import viewsets, permissions, mixins, generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Grade, Session, Payment
from ..permissions import IsMentorOrReadOnly
from ..serializers import GradeUpdateSerializer, GradeCreateSerializer, SessionShortSerializer, \
    UserShortSerializer, GradeShortSerializer, AttendanceMarkRequestSerializer, AttendanceMarkSerializer, \
    SessionAndGradeSerializer

User = get_user_model()


@extend_schema(
    tags=['Grade Mentor'],
)
@extend_schema_view(
    list=extend_schema(
        summary='Получить оценки студентов по subject id',
        responses={200: SessionAndGradeSerializer(read_only=True)},
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
            return SessionAndGradeSerializer
        return GradeUpdateSerializer

    def list(self, request, *args, **kwargs):
        group_id = request.query_params.get('group_id')
        subject_id = request.query_params.get('subject_id')
        if not group_id or not subject_id:
            return Response({"error": "group_id and subject_id are required"}, status=400)

        # Загружаем все нужные сессии с учетом групп
        sessions = (
            Session.objects.filter(
                is_active=True,
                subject_id=subject_id,
                groups__id=group_id
            )
            .order_by('date')
            .distinct()
        )

        sessions_data = SessionShortSerializer(sessions, many=True).data

        # Пользователи группы
        users = User.objects.filter(group_id=group_id).order_by('last_name', 'first_name')

        # Сегодняшняя дата
        today = timezone.localdate()
        today_str = today.strftime("%d-%m-%Y")

        # Сессии за сегодня (по дате)
        today_sessions = sessions.filter(date=today)
        today_session_ids = list(today_sessions.values_list('id', flat=True))

        # Один запрос на подсчет посещений
        attendance_count_query = (
            Grade.objects.filter(
                session_id__in=today_session_ids,
                attendance__in=['A', 'C']
            )
            .values('session_id')
            .annotate(count=Count('id'))
        )
        attendance_count_dict = {
            str(item['session_id']): item['count']
            for item in attendance_count_query
        }

        for s in sessions_data:
            session_id_str = s['id']
            if session_id_str in attendance_count_dict:
                s['attendance_count'] = attendance_count_dict[session_id_str]
            elif s['date'] == today_str:
                s['attendance_count'] = 0
            else:
                s['attendance_count'] = None

        paid_subquery = Payment.objects.filter(
            user=OuterRef('user'),
            grade=OuterRef('pk'),
            status=Payment.Status.PAID
        )

        grades = (
            Grade.objects.filter(session__in=sessions, user__in=users)
            .select_related('session', 'user')
            .annotate(has_paid=Exists(paid_subquery))
        )

        # Группируем оценки по пользователям (в Python)
        grades_by_user = {}
        for grade in grades:
            grades_by_user.setdefault(grade.user_id, []).append(grade)

        # Собираем итоговую структуру
        grades_list = []
        for user in users:
            user_grades = grades_by_user.get(user.id, [])
            user_data = {
                "user": UserShortSerializer(user).data,
                "scores": GradeShortSerializer(user_grades, many=True).data
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
    serializer_class = SessionAndGradeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = request.user
        subject_id = request.query_params.get('subject_id')
        if not subject_id:
            return Response({'error': 'subject_id is required'}, status=400)

        sessions = Session.objects.filter(
            is_active=True,
            subject_id=subject_id,
            groups=user.group
        ).order_by('date')
        sessions_data = SessionShortSerializer(sessions, many=True).data

        grades = Grade.objects.filter(user=user, session__in=sessions)
        user_data = {
            "user": UserShortSerializer(user).data,
            "scores": GradeShortSerializer(grades, many=True).data
        }

        return Response({
            "sessions": sessions_data,
            "grades": [user_data]
        })


class MarkAttendanceAPIView(APIView):
    """
    POST {"session_id": "..."}
    Отмечает присутствие (attendance="A", grade=5) текущего пользователя на занятии.
    Если отметка уже стоит — ничего не меняет.
    """
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        request=AttendanceMarkRequestSerializer,
        responses={
            200: OpenApiResponse(response=AttendanceMarkSerializer, description="Уже отмечено"),
            201: OpenApiResponse(response=AttendanceMarkSerializer, description="Отметка создана"),
            400: OpenApiResponse(description="Нет session_id или студент не в группе занятия"),
        }
    )
    def post(self, request):
        serializer = AttendanceMarkRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session_id = serializer.validated_data['session_id']
        user = request.user

        session = get_object_or_404(Session, id=session_id)

        if not hasattr(user, "group") or not session.groups.filter(id=user.group_id).exists():
            return Response(
                {"detail": "Вы не можете отмечаться на занятии другой группы."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # --- Создание или повторное получение отметки ---
        grade, created = Grade.objects.get_or_create(
            user=user,
            session=session,
            defaults={'attendance': "A",}
        )

        already_marked = not created

        response_serializer = AttendanceMarkSerializer(grade)
        return Response(
            {
                "marked": True,
                "already_marked": already_marked,
                **response_serializer.data
            },
            status=status.HTTP_200_OK if already_marked else status.HTTP_201_CREATED
        )
