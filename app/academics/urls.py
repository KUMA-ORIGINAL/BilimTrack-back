from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, SubjectViewSet, GradeViewSet, RatingViewSet

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'grades', GradeViewSet)
router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
]
