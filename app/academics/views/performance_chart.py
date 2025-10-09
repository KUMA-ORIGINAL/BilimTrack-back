from django.db.models import Sum
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

        grades_qs = Grade.objects.filter(user=user)
        if subject_id:
            grades_qs = grades_qs.filter(session__subject_id=subject_id)

        # Получаем данные в Python, чтобы использовать property total_score
        chart_dict = {}
        for g in grades_qs.select_related("session"):
            date = g.session.date.strftime("%Y-%m-%d")
            chart_dict.setdefault(date, 0)
            chart_dict[date] += g.total_score

        chart_data = [
            {"date": date, "score": score}
            for date, score in sorted(chart_dict.items())
        ]

        serialized_data = PerformanceChartSerializer(chart_data, many=True).data
        return Response(serialized_data)
