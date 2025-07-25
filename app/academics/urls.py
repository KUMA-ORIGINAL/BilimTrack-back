from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (GroupViewSet,
                    SubjectViewSet,
                    StudentGradeAPIView,
                    RatingViewSet,
                    PerformanceChartView,
                    MentorGradeViewSet, MarkAttendanceAPIView, SubjectMentorViewSet)

router = DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'mentor/subjects/me', SubjectMentorViewSet, basename='mentor-subject')
router.register(r'mentor-grades', MentorGradeViewSet, basename='mentor-grades')
router.register(r'rating', RatingViewSet, basename='rating')

urlpatterns = [
    path('', include(router.urls)),
    path('student-grades/me/',StudentGradeAPIView.as_view()),
    path('performance-chart/me/', PerformanceChartView.as_view()),
    path('attendance/mark/', MarkAttendanceAPIView.as_view(), name='mark-attendance'),
]
