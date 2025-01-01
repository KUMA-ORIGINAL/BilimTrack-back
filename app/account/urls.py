from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RarityViewSet, AchievementViewSet

router = DefaultRouter()
router.register(r'rarities', RarityViewSet)
router.register(r'achievements', AchievementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
