from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.apps import TrackerConfig
from tracker.views import HabitViewSet

router = DefaultRouter()
router.register(r'', HabitViewSet, basename='habit')

app_name = TrackerConfig.name

urlpatterns = [
    path('', include(router.urls)),
]