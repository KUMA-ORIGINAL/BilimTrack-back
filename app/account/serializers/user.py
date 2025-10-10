from django.contrib.auth import get_user_model
from django.db.models import Sum
from rest_framework import serializers

from academics.models import Grade
from academics.serializers import PerformanceChartSerializer, OrganizationSerializer, GroupShortSerializer
from .education import EducationSerializer
from .skill import SkillSerializer
from .tool import ToolSerializer
from .achievement import AchievementSerializer
from .work_experience import WorkExperienceSerializer
from ..models import WorkExperience, Education

User = get_user_model()


class MeSerializer(serializers.ModelSerializer):
    achievements = AchievementSerializer(many=True)
    group = GroupShortSerializer()
    performance = serializers.SerializerMethodField()

    skills = SkillSerializer(many=True)
    tools = ToolSerializer(many=True)
    work_experiences = WorkExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.role == 'student':
            allowed_fields = (
                'id', 'email', 'username', 'first_name', 'last_name',
                'photo', 'role', 'group', 'organization', 'achievements_count', 'points', 'rating',
                'achievements', 'performance')
        elif instance.role == 'mentor':
            allowed_fields = (
                'role',
                'username',
                'first_name',
                'last_name',
                'email',
                'phone_number',
                'photo',
                'google_meet_link',
                'organization',
                'skills',
                'mentor_achievements',
                'instagram',
                'telegram',
                'whatsapp',
                'facebook',
                'educations',
                'work_experiences',
            )
        else:
            allowed_fields = ('username', 'first_name', 'last_name', 'role')

        return {field: representation[field] for field in allowed_fields if field in representation}

    def get_performance(self, obj):
        grades = Grade.objects.filter(user=obj) \
            .values('session__date') \
            .annotate(total_score=Sum('grade')) \
            .order_by('session__date')

        chart_data = []
        for grade in grades:
            chart_data.append({
                'date': grade['session__date'].strftime('%Y-%m-%d') if grade['session__date'] else None,
                'score': grade['total_score'],
            })

        serialized_data = PerformanceChartSerializer(chart_data, many=True).data
        return serialized_data


class MeUpdateSerializer(serializers.ModelSerializer):
    # skills = serializers.PrimaryKeyRelatedField(
    #     queryset=Skill.objects.all(), many=True, required=False
    # )
    work_experiences = WorkExperienceSerializer(many=True, required=False)
    educations = EducationSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'photo',
            'google_meet_link',
            'skills',
            'mentor_achievements',
            'instagram',
            'telegram',
            'whatsapp',
            'facebook',
            'educations',
            'work_experiences',
        )

    def update(self, instance, validated_data):
        # Обрабатываем skills как M2M
        skills = validated_data.pop('skills', None)
        if skills is not None:
            instance.skills.set(skills)

        # Обрабатываем work_experiences как вложенную связь
        work_experiences_data = validated_data.pop('work_experiences', None)
        if work_experiences_data is not None:
            instance.work_experiences.all().delete()
            for work_data in work_experiences_data:
                WorkExperience.objects.create(user=instance, **work_data)

        # Обрабатываем educations как вложенную связь
        educations_data = validated_data.pop('educations', None)
        if educations_data is not None:
            instance.educations.all().delete()
            for education_data in educations_data:
                Education.objects.create(user=instance, **education_data)

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class UserListSerializer(serializers.ModelSerializer):
    group = GroupShortSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'photo', 'points', 'rating', 'group')
