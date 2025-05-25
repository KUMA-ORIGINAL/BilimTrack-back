from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins
from academics.models import Group
from schedule.serializers import GroupSerializer


@extend_schema(tags=['schedule'])
class GroupViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin):
    """
    ViewSet для получения списка учебных групп.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
