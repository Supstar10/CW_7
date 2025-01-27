from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.apps import TrackerConfig
from tracker.views import HabitViewSet, PublicHabitViewSet

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

router.register(r'public-habits', PublicHabitViewSet, basename='public-habit')

app_name = TrackerConfig.name

urlpatterns = [
    path('', include(router.urls)),
]