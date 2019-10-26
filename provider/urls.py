from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
import django_rq

from .views import (RegisterUserView, CreateVenueView, SchemaView)

SWAGGER_PATTERNS = [
   path('swagger(?<format>\.json|\.yaml)$', SchemaView.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/$', SchemaView.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/$', SchemaView.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


AUTH_PATTERNS = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token-obtain'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh')
]

CREATE_PATTERNS = [
    path('venue/', CreateVenueView.as_view(), name='create-venue')
]

urlpatterns = [
    path('auth/', include(AUTH_PATTERNS)),
    path('create/', include(CREATE_PATTERNS)),
    path('api_doc/', include(SWAGGER_PATTERNS)),
    path('register/', RegisterUserView.as_view(), name='register-user'),
    path('django-rq/', include('django_rq.urls'))
]
