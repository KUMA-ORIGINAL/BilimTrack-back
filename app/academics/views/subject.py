from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, mixins, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..models import Subject, GroupSubjectMentor, GroupSubjectMentorSubject
from ..serializers import SubjectSerializer, SubjectListSerializer, SubjectMentorSerializer


@extend_schema(tags=['Subject'])
class SubjectViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return SubjectListSerializer
        return SubjectSerializer

    @action(detail=False, methods=['get'], url_path='me', url_name='me')
    def me(self, request):
        """
        Получить список предметов для текущего студента
        """
        user = request.user
        group = getattr(user, "group", None)  # предполагается, что у User есть поле group
        if not group:
            return Response(
                {"detail": "Пользователь не состоит ни в одной группе."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Найдём все предметы для этой группы через «наставник–группа–предмет»
        subjects = Subject.objects.filter(
            mentor_links__group=group  # mentor_links мы добавляли в GroupSubjectMentor через ManyToMany
        ).distinct()

        serializer = self.get_serializer(subjects, many=True)
        return Response(serializer.data)


@extend_schema(tags=['Subject Mentor'])
class SubjectMentorViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Subject.objects.all()
    serializer_class = SubjectMentorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Предметы, где текущий пользователь является наставником
        subject_ids = GroupSubjectMentorSubject.objects.filter(
            group_subject_mentor__mentor=self.request.user
        ).values_list('subject_id', flat=True).distinct()

        return Subject.objects.filter(id__in=subject_ids)
