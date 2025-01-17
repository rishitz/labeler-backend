from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from labeler.rest_framework import viewsets

from .models import DicomLabelingJob, FullStudyAnnotationSet, StudyLabelingJob
from .serializers import (
    DicomLabelingJobSerializer,
    FullStudyAnnotationSetSerializer,
    StudyLabelingJobSerializer,
)


class FullStudyAnnotationSetViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = ["get"]
    queryset = FullStudyAnnotationSet.objects.all()
    serializer_class = FullStudyAnnotationSetSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["user"]
    search_fields = ["name"]
    ordering_fields = ["name"]


class StudyLabelingJobViewSet(viewsets.CamelCaseModelViewSet):
    queryset = StudyLabelingJob.objects.all()
    serializer_class = StudyLabelingJobSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["study", "user", "annotation_set"]
    search_fields = ["study__foreign_id"]


class DicomLabelingJobViewSet(viewsets.CamelCaseModelViewSet):
    http_method_names = ["get", "post"]
    permission_classes = [IsAuthenticated]
    serializer_class = DicomLabelingJobSerializer
    queryset = (
        DicomLabelingJob.objects.all()
        .select_related("annotation_set", "dicom", "user", "study_labeling_job")
        .order_by("-id")
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "annotation_set", "dicom"]
