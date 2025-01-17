from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions


class LabelerSchemaGenerator(OpenAPISchemaGenerator):
    def get_endpoints(self, request):
        endpoints = super().get_endpoints(request)
        return {path: val for path, val in endpoints.items() if path.startswith("/api")}


# set the schema view for api dosc:
schema_view = get_schema_view(
    openapi.Info(
        title="iCardio.ai",
        default_version="v1",
        description="Labeler API",
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated,),
    generator_class=LabelerSchemaGenerator,
)
