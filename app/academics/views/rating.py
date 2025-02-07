from django.contrib.auth import get_user_model
from django.db.models import Max
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from academics.models import Group
from academics.serializers import GroupListSerializer
from account.serializers import UserListSerializer

User = get_user_model()

@extend_schema(tags=['Rating'])
@extend_schema_view(
    groups=extend_schema(
        summary='Получить список групп отсортированных по баллам',
        responses=GroupListSerializer,
        parameters=[
            OpenApiParameter(
                name='subject_id',
                description='ID предмета для фильтрации групп',
                required=False,
        )]
    ),
    users=extend_schema(
        summary='Получение студентов отсортированных по баллам',
        responses=UserListSerializer,
        parameters=[
            OpenApiParameter(
                name='subject_id',
                description='ID предмета для фильтрации студентов',
                required=False,
            )
        ]
    )
)
class RatingViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='groups', url_name='groups_rating')
    def groups(self, request):
        subject_id = request.query_params.get('subject_id')

        if subject_id:
            groups = Group.objects.filter(subjects__id=subject_id) \
                .annotate(last_grade_date=Max('users__grade__date')) \
                .order_by('-points', '-last_grade_date')
        else:
            groups = Group.objects.annotate(last_grade_date=Max('users__grade__date')) \
                .order_by('-points', '-last_grade_date')

        groups_serializer = GroupListSerializer(groups, many=True)
        return Response(groups_serializer.data)

    @action(detail=False, methods=['get'], url_path='users', url_name='user_rating')
    def users(self, request):
        subject_id = request.query_params.get('subject_id')

        if subject_id:
            users = User.objects.filter(role='student', group__subjects__id=subject_id) \
                .annotate(last_grade_date=Max('grade__date')) \
                .order_by('-points', '-last_grade_date').distinct()
        else:
            users = User.objects.filter(role='student') \
                .annotate(last_grade_date=Max('grade__date')) \
                .order_by('-points', '-last_grade_date')

        users_serializer = UserListSerializer(users, many=True)
        return Response(users_serializer.data)
