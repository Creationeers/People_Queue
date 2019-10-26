from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

SchemaView = get_schema_view(
   openapi.Info(
      title="People Queue",
      default_version='v1',
      description="The API Documentation",
      terms_of_service="",
      contact=openapi.Contact(email="enzo@creatineers.tech"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)