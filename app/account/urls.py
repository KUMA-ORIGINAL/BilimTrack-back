from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RarityViewSet, AchievementViewSet, UserRatingViewSet, UserViewSet, MeViewSet

router = DefaultRouter()
router.register(r'rarities', RarityViewSet)
router.register(r'achievements', AchievementViewSet)
router.register(r'users', UserRatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', MeViewSet.as_view()),
    path('users/<str:username>/', UserViewSet.as_view(), name='user-profile'),
    path('', include('djoser.urls.jwt')),
]
