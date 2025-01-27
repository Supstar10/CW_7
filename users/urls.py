from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from users.apps import UsersConfig
from users.views import RegisterAPIView, UserViewSet

app_name = UsersConfig.name

urlpatterns = [
    path('', UserViewSet.as_view({'get': 'list'}), name='list'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]