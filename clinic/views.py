from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from clinic.filters import DicomFilter, FrameFilter
from labeler.rest_framework import viewsets

from .models import Dicom, Frame, Media, Study
from .serializers import (
    DicomRetrieveSerializer,
    DicomSerializer,
    FrameSerializer,
    MediaSerializer,
    StudySerializer,
)


class DicomViewSet(viewsets.CamelCaseModelViewSet):
    queryset = (
        Dicom.objects.filter(study__isnull=False)
        .select_related("study")
        .prefetch_related("media__frames")
        .order_by("study", "index")
    )
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]
    filter_backends = [
        DicomFilter,
    ]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DicomRetrieveSerializer
        return DicomSerializer


class StudyViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = ["get"]
    serializer_class = StudySerializer
    queryset = (
        Study.objects.all()
        .order_by("-created_at")
        .prefetch_related("dicoms")
        .annotate(_number_of_dicoms=Count("dicoms", distinct=True))
    )
    filterset_fields = {
        "designation": ["exact"],
    }


class FrameViewSet(viewsets.CamelCaseModelViewSet):
    queryset = (
        Frame.objects.all()
        .order_by("media__dicom", "index")
        .select_related("media__dicom")
    )
    serializer_class = FrameSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter, FrameFilter]
    filterset_fields = {
        "media__dicom__study__uuid": ["exact"],
    }
    search_fields = ["media__dicom__uuid"]
    ordering_fields = ["index", "media__dicom"]
    http_method_names = ["get"]


class MediaViewSet(viewsets.CamelCaseModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
