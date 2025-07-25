from django.urls import path, include
from rest_framework.routers import DefaultRouter

from schedule import views

router = DefaultRouter()
router.register(r'lesson-types', views.LessonTypeViewSet, basename='lessontype')
router.register(r'rooms', views.RoomViewSet, basename='room')
router.register(r'lesson-times', views.LessonTimeViewSet, basename='lessontime')
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'groups', views.GroupViewSet, basename='group')
router.register(r'courses', views.CourseViewSet, basename='course')
router.register('', views.ScheduleViewSet)

urlpatterns = [
    path('schedules/', include(router.urls)),
]
