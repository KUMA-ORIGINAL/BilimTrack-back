from django.urls import path, include
from drf_spectacular.utils import extend_schema
from rest_framework.routers import DefaultRouter
from .views import RarityViewSet, AchievementViewSet, UserViewSet, MeViewSet

router = DefaultRouter()
router.register(r'rarities', RarityViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', MeViewSet.as_view()),
    path('', include('djoser.urls.jwt')),
]
