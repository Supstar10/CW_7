from django.urls import path, include
from rest_framework.routers import DefaultRouter
from tracker.apps import TrackerConfig
from tracker.views import HabitViewSet, PublicHabitListView

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')

app_name = TrackerConfig.name

urlpatterns = [
    path('', include(router.urls)),
    path('habits/create/', HabitViewSet.as_view({'post': 'create'}), name='habit-create'),
    path('public-habits/', PublicHabitListView.as_view(), name='public-habits-list'),
]
