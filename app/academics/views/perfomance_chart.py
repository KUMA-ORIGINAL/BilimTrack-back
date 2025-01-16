from django.db.models import Sum
from django.db.models.functions import TruncDate
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import permissions

from academics.models import Grade
from ..serializers import PerformanceChartSerializer

@extend_schema(tags=['Performance Chart'])
@extend_schema_view(
    get=extend_schema(
        summary='Получить график успеваемости студента',
        responses=PerformanceChartSerializer
    )
)
class PerformanceChartView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        # Aggregate grades by date (truncating time) and sum the grades for each day
        grades = Grade.objects.filter(user=user) \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(total_score=Sum('grade')) \
            .order_by('date')

        # Prepare chart data
        chart_data = []
        for grade in grades:
            chart_data.append({
                'date': grade['date'].strftime('%d-%m'),
                'score': grade['total_score'],
            })

        return Response(chart_data)