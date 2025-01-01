# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, SubjectViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'subjects', SubjectViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
