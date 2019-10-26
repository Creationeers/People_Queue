from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
import django_rq
from .views import (RegisterUserView)

AUTH_PATTERNS = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh')
]

urlpatterns = [
    path('auth/', include(AUTH_PATTERNS)),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('django-rq/', include('django_rq.urls'))
]
