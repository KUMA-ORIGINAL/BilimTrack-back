from django.contrib.auth import get_user_model
from django.db.models import Max, Sum
from django.db.models.functions import Coalesce
from django.utils.dateparse import parse_date
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from academics.models import Group
from academics.serializers import GroupListSerializer
from account.serializers import UserListSerializer

User = get_user_model()


@extend_schema(tags=['Rating'])
@extend_schema_view(
    groups=extend_schema(
        summary='Получить список групп, отсортированных по баллам',
        responses=GroupListSerializer,
        parameters=[
            OpenApiParameter(
                name='subject_id',
                description='ID предмета для фильтрации групп',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='course_id',
                description='ID курса для фильтрации',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='group_id',
                description='ID конкретной группы',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='teacher_id',
                description='ID преподавателя (чтобы выводить группы только по его занятиям)',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='start_date',
                description='Начальная дата (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE
            ),
            OpenApiParameter(
                name='end_date',
                description='Конечная дата (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE
            ),
        ]
    ),
    users=extend_schema(
        summary='Получение студентов, отсортированных по баллам',
        responses=UserListSerializer,
        parameters=[
            OpenApiParameter(
                name='subject_id',
                description='ID предмета для фильтрации студентов',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='course_id',
                description='ID курса (через группы студентов)',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='group_id',
                description='ID конкретной группы (для фильтрации студентов)',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='teacher_id',
                description='ID преподавателя (вывод студентов по занятиям этого преподавателя)',
                required=False,
                type=OpenApiTypes.INT
            ),
            OpenApiParameter(
                name='start_date',
                description='Начальная дата (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE
            ),
            OpenApiParameter(
                name='end_date',
                description='Конечная дата (YYYY-MM-DD)',
                required=False,
                type=OpenApiTypes.DATE
            ),
        ]
    )
)
class RatingViewSet(viewsets.GenericViewSet):

    def _apply_filters(self, queryset, params, is_user=False):
        """
        Универсальная функция фильтрации
        """
        subject_id = params.get("subject_id")
        course_id = params.get("course_id")
        group_id = params.get("group_id")
        teacher_id = params.get("teacher_id")
        start_date = parse_date(params.get("start_date")) if params.get("start_date") else None
        end_date = parse_date(params.get("end_date")) if params.get("end_date") else None

        if subject_id:
            queryset = queryset.filter(
                **(
                    {"group__subjects__id": subject_id}
                    if is_user else {"subjects__id": subject_id}
                )
            )

        if course_id:
            queryset = queryset.filter(group__course__id=course_id)

        if group_id:
            queryset = queryset.filter(group__id=group_id if is_user else group_id)

        if teacher_id:
            queryset = queryset.filter(grade__session__teacher__id=teacher_id)

        if start_date and end_date:
            queryset = queryset.filter(grade__session__date__range=(start_date, end_date))

        return queryset

    # Рейтинг групп
    @action(detail=False, methods=['get'], url_path='groups', url_name='groups_rating')
    def groups(self, request):
        groups = Group.objects.all()
        groups = self._apply_filters(groups, request.query_params, is_user=False)

        groups = groups.annotate(
            # используем уже подсчитанные points
            total_points=Coalesce("points", 0),
            last_grade_date=Max("users__grade__session__date")
        ).order_by("-total_points", "-last_grade_date")

        groups_serializer = GroupListSerializer(groups, many=True)
        return Response(groups_serializer.data)

    # Рейтинг пользователей
    @action(detail=False, methods=['get'], url_path='users', url_name='users_rating')
    def users(self, request):
        users = User.objects.filter(role="student")
        users = self._apply_filters(users, request.query_params, is_user=True)

        users = users.annotate(
            total_points=Coalesce("points", 0),   # теперь берём поле points
            last_grade_date=Max("grade__session__date")
        ).order_by("-total_points", "-last_grade_date").distinct()

        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data)
