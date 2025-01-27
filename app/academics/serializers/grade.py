from rest_framework import serializers

from ..models import Grade
from collections import defaultdict


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'


class StudentGradeSerializer(serializers.Serializer):
    name = serializers.CharField(source='user.get_full_name')
    username = serializers.CharField(source='user.username')
    scores = serializers.SerializerMethodField()

    def get_scores(self, obj):
        # Собираем все оценки для текущего пользователя
        scores = {}
        grades = Grade.objects.filter(user=obj.user, subject=obj.subject)  # Получаем все оценки для
        # пользователя
        for grade in grades:
            date_str = grade.date.strftime('%d.%m')  # Форматируем дату в нужный формат
            scores[date_str] = grade.grade
        return scores