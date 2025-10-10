from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import permissions

from academics.models import Grade
from ..serializers import PerformanceChartSerializer


@extend_schema(tags=['Performance Chart'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить график успеваемости студента',
        parameters=[
            OpenApiParameter(
                name="subject_id",
                type=int,
                location=OpenApiParameter.QUERY,
                required=False,
                description="ID предмета для фильтрации графика"
            ),
        ],
        responses=PerformanceChartSerializer,
    )
)
class PerformanceChartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        subject_id = request.query_params.get("subject_id")

        grades_qs = Grade.objects.filter(
            user=user,
            session__is_active=True,
            session__groups=user.group,
        ).select_related('session', 'session__subject')

        if subject_id:
            grades_qs = grades_qs.filter(session__subject_id=subject_id)

        chart_data = []
        for g in grades_qs:
            chart_data.append({
                "date": g.session.date.strftime("%Y-%m-%d"),
                "subject": g.session.subject.name,
                "session_id": g.session.id,
                "score": g.total_score,
            })

        chart_data.sort(key=lambda x: (x["date"], x["session_id"]))

        serialized_data = PerformanceChartSerializer(chart_data, many=True).data
        return Response(serialized_data)