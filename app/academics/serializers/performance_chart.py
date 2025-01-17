from rest_framework import serializers


class PerformanceChartSerializer(serializers.Serializer):
    date = serializers.DateField()
    score = serializers.IntegerField()
