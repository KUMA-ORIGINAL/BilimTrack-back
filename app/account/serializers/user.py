from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.db.models.functions import TruncDate
from rest_framework import serializers

from academics.models import Grade
from academics.serializers import PerformanceChartSerializer
from .achievement_and_rarity import AchievementSerializer

User = get_user_model()

class MeSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True)
    group = serializers.StringRelatedField()
    performance = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'photo', 'role', 'group', 'achievements_count', 'points', 'rating',
                  'achievements', 'performance')

    def get_performance(self, obj):
        grades = Grade.objects.filter(user=obj) \
            .annotate(date=TruncDate('created_at')) \
            .values('date') \
            .annotate(total_score=Sum('grade')) \
            .order_by('date')

        chart_data = []
        for grade in grades:
            chart_data.append({
                'date': grade['date'].strftime('%Y-%m-%d'),
                'score': grade['total_score'],
            })

        serialized_data = PerformanceChartSerializer(chart_data, many=True).data

        return serialized_data

class MeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'photo')


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photo', 'points', 'rating')
