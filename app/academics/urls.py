from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GroupViewSet, SubjectViewSet, GradeMentorViewSet, StudentGradeAPIView,
                    RatingViewSet,
                    PerformanceChartView, GradeMentor2ViewSet)

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'mentor-grades', GradeMentorViewSet , basename='grades-mentor')
router.register(r'mentor-grades', GradeMentor2ViewSet, basename='grades-mentor-2')
router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('student-grades/me/',StudentGradeAPIView.as_view()),
    path('performance-chart/me/', PerformanceChartView.as_view()),
]
