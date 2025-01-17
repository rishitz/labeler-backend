from django_filters.rest_framework import DjangoFilterBackend
from djangorestframework_camel_case.parser import CamelCaseJSONParser
from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet


class CamelCaseModelViewSet(ModelViewSet):
    parser_classes = [
        CamelCaseJSONParser,
    ]
    renderer_classes = [
        CamelCaseJSONRenderer,
    ]
    filter_backends = [
        DjangoFilterBackend,
    ]

    def get_queryset(self):
        """
        Override this method in your subclasses to return the correct queryset.
        """
        raise NotImplementedError("Subclasses must define get_queryset")

    def get_permissions(self):
        """
        Override this method in your subclasses to set specific permissions.
        """
        return [AllowAny()]
